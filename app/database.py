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
        print(f"OperationalError: \n")
        print(f"Message {e}\n")
        print(f"pgcode {e.pgcode}\n")
        print(f"pgerror {e.pgerror}\n")
        return None

#This function should hard reset the database, removing all tables that previously existed
def hardReset(user_name, conn):
    try:
        with conn.cursor() as cur:
            cur.execute("DROP SCHEMA public CASCADE;")
            cur.execute("CREATE SCHEMA public;")
            cur.execute(f"GRANT ALL ON SCHEMA public TO {user_name};")
            cur.execute("GRANT ALL ON SCHEMA public TO public;")
            cur.execute("COMMENT ON SCHEMA public IS \'standard public schema\'")
    except Exception as e:
        print("Hard reset failed:\n ", e)

#This function should set up the project database
def importDatabase(conn):
    path = os.getcwd()
    path = path + "/netflix_titles.csv"
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
    importDatabase(conn)

if __name__ == "__main__":
    main()