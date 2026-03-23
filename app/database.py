import psycopg2
import os
from pathlib import Path

# Connect to the Database with the name "project" and user $USER. 
#(NOTE: B/c server is localhost, a running PostgreSQL server with the name "project" is required for this code to work)
def getConnection(user_name):
    try:
        return psycopg2.connect(
            database = "project",
            user = user_name,
            host = "127.0.0.1",
            port = 8888,
        )
    except psycopg2.OperationalError as e:
        print(f"OperationalError:")
        print(f"Message {e}")
        print(f"pgcode {e.pgcode}")
        print(f"pgerror {e.pgerror}")
        return None

#Hard reset the database, removing all tables that previously existed
def hardReset(user_name, conn):
    print("!!!WARNING!!!\nDELETING ENTIRE DATABASE NOW\nARE YOU SURE?")
    user_input = input("Press (1) to confirm, (2) to cancel:\n")
    if user_input == 2:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("DROP SCHEMA public CASCADE;")
            cur.execute("CREATE SCHEMA public;")
            cur.execute(f"GRANT ALL ON SCHEMA public TO {user_name};")
            cur.execute("GRANT ALL ON SCHEMA public TO public;")
            cur.execute("COMMENT ON SCHEMA public IS \'standard public schema\'")
    except Exception as e:
        print("Hard reset failed: ", e)

#Init tables for database
def initDatabase(conn):
    print("Initializing Database:")
    path = os.getcwd()
    path = path + "/netflix_titles.csv"
    try:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS country (
                country_id SERIAL PRIMARY KEY,
                name VARCHAR(64)
            );
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS media (
                show_id SERIAL PRIMARY KEY,
                title VARCHAR(256),
                type VARCHAR(8),
                release_year SMALLINT,
                date_added DATE,
                duration SMALLINT,
                rating VARCHAR(8),
                m_country_id INTEGER REFERENCES country(country_id)
            );
            """)
            #User roles defined here
            cur.execute("""
            CREATE TABLE IF NOT EXISTS role (
                role_id SERIAL PRIMARY KEY,
                role_name VARCHAR(16) UNIQUE NOT NULL
            );
            """)
            cur.execute("INSERT INTO role(role_name) VALUES(\'user\');")
            cur.execute("INSERT INTO role(role_name) VALUES(\'admin\');")
            #TODO: Use argon2id for password hashing (not here, use on password input for security)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(32) NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
                role INTEGER NOT NULL REFERENCES role(role_id)
            );
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS isFavorited (
                f_user_id INTEGER REFERENCES users(user_id),
                f_show_id INTEGER REFERENCES media(show_id),
                PRIMARY KEY(f_user_id,f_show_id)
            );
            """)
            #I disagree with the schema, I'm making a person table to contain director / actor
            cur.execute("""
            CREATE TABLE IF NOT EXISTS person (
                person_id SERIAL PRIMARY KEY,
                first_name VARCHAR(64),
                last_name VARCHAR(64)
            );
            """)
            #TODO: Expand these lil baby tables (maybe with other csvs?) (Low prio, get it working first)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS actor (
                actor_id INTEGER REFERENCES person(person_id) PRIMARY KEY
            );
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS actedIn (
                ai_actor_id INTEGER REFERENCES actor(actor_id),
                ai_show_id INTEGER REFERENCES media(show_id),
                PRIMARY KEY(ai_actor_id, ai_show_id)
            );
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS director (
                dir_id INTEGER REFERENCES person(person_id) PRIMARY KEY
            );
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS directed (
                d_dir_id INTEGER REFERENCES director(dir_id),
                d_show_id INTEGER REFERENCES media(show_id),
                PRIMARY KEY(d_dir_id, d_show_id)
            );
            """)
    except psycopg2.errors.UniqueViolation as e:
        conn.rollback()
        print("WARNING: duplicate table detected!\n Is the database already initialized?")
    #TODO: import database from CSV

#Get system user 
#TODO: move all this to run.py when I am done testing
def main():
    user_name = os.environ.get("USER")
    if user_name:
        print("Assume DB user is:", user_name)
    else:
        print("No $USER variable found, Connection Fails")
    conn = getConnection(user_name)
    if conn:
        print("Connection to PostGreSQL Established Succesfully!")
        conn.autocommit = True
    else:
        print("Connection to PostGreSQL Encountered an Error!")
        return
    initDatabase(conn)
    hardReset(user_name, conn)

if __name__ == "__main__":
    main()