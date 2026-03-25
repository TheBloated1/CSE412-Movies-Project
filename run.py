import os 
import psycopg2
from app import app

if __name__ == "__main__":
    # check if postgresql server is running before starting the flask server
    user_name = os.environ.get("USER")
    if not user_name:
        print("No $USER variable found, Connection Fails")
        exit(1)
    try:
        conn = psycopg2.connect(
            database = "project",
            user = user_name,
            host = "127.0.0.1",
            port = 8888,
        )
        conn.close()
    except psycopg2.OperationalError as e:
        print("Error connecting to PostgreSQL server!!!\nError msg:", e)
        exit(1)

    # run flask server! yay
    print("Starting flask...")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)