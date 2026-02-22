import psycopg2
import os

def getConnection():
    try:
        user_name = os.environ.get("USER")
        if user_name:
            print("Assume DB name/user is: ", user_name)
        else:
            print("No $USER variable found, Connection Fails")
            return False
        return psycopg2.connect(
            database = user_name,
            user = user_name,
            host = "127.0.0.1",
            port = 8888,
        )
    except psycopg2.OperationalError as e:
        print(f"OperationalError: \n")
        print(f"Message {e}\n")
        print(f"pgcode {e.pgcode}\n")
        print(f"pgerror {e.pgerror}\n")
        return False
conn = getConnection()
if conn:
    print("Connection to PostGreSQL Established Succesfully!")
else:
    print("Connection to PostGreSQL Encountered an Error!")