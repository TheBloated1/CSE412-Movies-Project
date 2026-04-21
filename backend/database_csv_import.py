# Import netflix_titles.csv

import csv
import random
#import psycopg2
from psycopg2.extras import execute_values
import pandas as pd

def import_csv():
    # hardcode netflix_titles.csv for now
    df = pd.read_csv("netflix_titles.csv", dtype="string")
    df = df.astype(object).where(pd.notna(df), None) # replace NA with None for easier SQL insertion
    return df

# csv schema: 
# show_id,type,title,director,cast,country,date_added,release_year,rating,duration,listed_in,description

def get_first_get_last_name(full_name):
    names = full_name.strip().split(" ")
    if names[0] == '':
        raise ValueError("Invalid name: empty string")

    if len(names) == 1:
        return (names[0], names[0])
    elif len(names) == 2:
        return (names[0], names[-1])
    elif len(names) > 2:
        return (" ".join(names[0:-1]), names[-1])

# From netflix_titles.csv, populates tables: media, country, producedIn, genre, listedIn, person, director, directed, actor, actedIn
def import_csv_to_db(conn):
    print("Importing CSV to Database:")

    df = import_csv()

    country_country_id_map = {} # k = country name, v = country_id
    genre_genre_id_map = {} # k = genre name, v = genre_id
    people_people_id_map = {} # k = person name is a tuple (first name, last name), v = people_id
    director_id_set = set() # set of director ids to see if added in director/actor
    actor_id_set = set() # set of actor ids to see if added in director/actor

    # TODO: Add in batch insert for everything versus executing each insert statement separately...
    # so far batch inserts only for most dependent level tables

    producedIn_insert_list = []
    listedIn_insert_list = []
    directed_insert_list = []
    actedIn_insert_list = []

    try:
        cur = conn.cursor()
        dbg_idx = 0
        for row in df.itertuples(index=False):
            if dbg_idx % 100 == 0:
                print(dbg_idx)
            dbg_idx += 1
            #show_id = row["show_id"] -- actually not needed since we generate our own
            type = row.type
            title = row.title
            director = row.director
            cast = row.cast
            country = row.country
            date_added = row.date_added
            release_year = row.release_year
            rating = row.rating
            duration = row.duration
            listed_in = row.listed_in
            description = row.description

            # insert into media table
            cur.execute("""
            INSERT INTO media (type, title, release_year, date_added, duration, rating, description) 
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING show_id;""",
            (type, title, release_year, date_added, duration, rating, description))
            show_id = cur.fetchone()[0]

            # insert country tables if not already inserted
            if pd.notna(country):
                countries = country.strip().split(", ")
                for c in countries:
                    country_id = None
                    if c not in country_country_id_map:
                        # TODO: random box office placeholder, later on, when we find good
                        # database, we can update this with real box office numbers
                        random_boxoffice = random.randint(1000000, 1000000000)

                        # new country
                        cur.execute("""
                        INSERT INTO country (name, total_boxoffice) VALUES (%s, %s) ON CONFLICT (NAME) DO NOTHING RETURNING country_id;""", 
                        (c, random_boxoffice))
                        country_id = cur.fetchone()[0]
                        country_country_id_map[c] = country_id
                    else:
                        country_id = country_country_id_map[c]

                    # update producedIn
                    producedIn_insert_list.append((country_id, show_id))

            # insert genre tables if not already inserted
            if pd.notna(listed_in):
                listed_in_genres = listed_in.strip().split(", ")
                for genre in listed_in_genres:
                    genre_id = None
                    if genre not in genre_genre_id_map:
                        # new genre
                        cur.execute("""
                        INSERT INTO genre (name) VALUES (%s) ON CONFLICT (NAME) DO NOTHING RETURNING genre_id;""", 
                        (genre,))
                        genre_id = cur.fetchone()[0]
                        genre_genre_id_map[genre] = genre_id
                    else:
                        genre_id = genre_genre_id_map[genre]

                    # update listedIn
                    listedIn_insert_list.append((show_id, genre_id))

            # insert directors
            if pd.notna(director):
                directors = director.strip().split(", ")
                for d in directors:
                    director_name = get_first_get_last_name(d)
                    director_id = None
                    if director_name not in people_people_id_map:
                        # new director
                        # update person table
                        cur.execute("""
                        INSERT INTO person (first_name, last_name) VALUES (%s, %s) ON CONFLICT (first_name, last_name) DO NOTHING RETURNING person_id;""", 
                        (director_name[0], director_name[1]))
                        director_id = cur.fetchone()[0]
                        people_people_id_map[director_name] = director_id
                        # update director table
                        cur.execute("""
                        INSERT INTO director (dir_id) VALUES (%s);""",
                        (director_id,))
                        director_id_set.add(director_id)
                    else:
                        director_id = people_people_id_map[director_name]
                        if director_id not in director_id_set:
                            # update director table
                            cur.execute("""
                            INSERT INTO director (dir_id) VALUES (%s);""",
                            (director_id,))
                            director_id_set.add(director_id)

                    # updated directed table
                    directed_insert_list.append((director_id, show_id))

            # insert actors
            if pd.notna(cast):
                actors = cast.strip().split(", ")
                for a in actors:
                    actor_name = get_first_get_last_name(a)
                    actor_id = None
                    if actor_name not in people_people_id_map:
                        # new actor
                        # update person table
                        cur.execute("""
                        INSERT INTO person (first_name, last_name) VALUES (%s, %s) ON CONFLICT (first_name, last_name) DO NOTHING RETURNING person_id;""", 
                        (actor_name[0], actor_name[1]))
                        actor_id = cur.fetchone()[0]
                        people_people_id_map[actor_name] = actor_id
                        # update actor table
                        cur.execute("""
                        INSERT INTO actor (actor_id) VALUES (%s);""",
                        (actor_id,))
                        actor_id_set.add(actor_id)
                    else:
                        actor_id = people_people_id_map[actor_name]
                        if actor_id not in actor_id_set:
                            # update actor table
                            cur.execute("""
                            INSERT INTO actor (actor_id) VALUES (%s);""",
                            (actor_id,))
                            actor_id_set.add(actor_id)
                    
                    # updated acted_in table
                    actedIn_insert_list.append((actor_id, show_id))
        # handle batch inserts
        execute_values(cur, 
        "INSERT INTO producedIn (p_country_id, p_show_id) VALUES %s ON CONFLICT DO NOTHING;",
        producedIn_insert_list)

        execute_values(cur, 
        "INSERT INTO listedIn (li_show_id, li_genre_id) VALUES %s ON CONFLICT DO NOTHING;",
        listedIn_insert_list)

        execute_values(cur,
        "INSERT INTO directed (d_dir_id, d_show_id) VALUES %s ON CONFLICT DO NOTHING;",
        directed_insert_list)

        execute_values(cur,
        "INSERT INTO actedIn (ai_actor_id, ai_show_id) VALUES %s ON CONFLICT DO NOTHING;",
        actedIn_insert_list)

        conn.commit()
        print("Finished importing CSV to Database.")
    except:
        print("Error importing csv to db")
        conn.rollback()
        raise Exception("Error importing csv to db")

if __name__ == "__main__":
    # debug
    pass