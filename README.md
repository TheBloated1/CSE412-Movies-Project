# CSE412 Movies Project

## Requirements

### Packages
- Flask 3.1.2 (```pip install Flask```)
- psycopg2 2.9.11 (```pip install psycopg2-binary```) or (```pip install psycopg2```)
- pandas 2.3.3 (```pip install pandas```)

### Data
- netflix_titles.csv (https://www.kaggle.com/datasets/shivamb/netflix-shows/data)
    - Already provided in repository

## Instructions

### PostgreSQL Setup

> **Why port 8888?** This project runs on port 8888 so it doesn't conflict with any existing
> PostgreSQL instance you may already have running on the default port (5432).
> This requires its own separate data directory, set up once using the steps below.

#### First-time setup (run once)

1. Make sure PostgreSQL tools are on your path:
```bash
# Linux
export PATH="/lib/postgresql/14/bin:$PATH"

# macOS (Homebrew, adjust version as needed)
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"
```

2. Initialize a new data directory for this project:
```bash
initdb /usr/local/var/postgresql@15-project
```

3. Start the new PostgreSQL instance on port 8888:
```bash
pg_ctl -D /usr/local/var/postgresql@15-project -o "-p 8888" -l /usr/local/var/postgresql@15-project/server.log start
```

4. Create the database:
```bash
createdb -h 127.0.0.1 -p 8888 -U $USER project
```

5. Verify the connection:
```bash
psql -h 127.0.0.1 -p 8888 -U $USER -d project
# you should see a project=# prompt
```

#### Every subsequent session

Start the server before working on the project:
```bash
pg_ctl -D /usr/local/var/postgresql@15-project -o "-p 8888" -l /usr/local/var/postgresql@15-project/server.log start
```

Stop the server when you're done:
```bash
pg_ctl -D /usr/local/var/postgresql@15-project stop
```

> **Tip:** Add these aliases to your `~/.zshrc` or `~/.bashrc` to save typing:
> ```bash
> alias startproject="pg_ctl -D /usr/local/var/postgresql@15-project -o '-p 8888' -l /usr/local/var/postgresql@15-project/server.log start"
> alias stopproject="pg_ctl -D /usr/local/var/postgresql@15-project stop"
> ```
> Then just run `startproject` / `stopproject` each session.

### Application
### Application
1. Clone repository into a local directory
2. Start PostgreSQL server (see above)
3. **First time only** — initialize tables and import data:
```bash
   cd app
   python3 database.py
```
4. Start app: `python run.py`
5. Access the app at: `http://localhost:5000`
6. Stop the app via CTRL+C

> **Note:** The URL is `http://` not `https://` for local development.

### Debug
- Connect to the PostgreSQL project database with psql:
```bash
psql -h 127.0.0.1 -p 8888 -U $USER -d project
```
- Test init database/import .csv/delete database optionally:
```bash
cd app
python3 database.py
```
- If the server fails to start, check the log for errors:
```bash
cat /usr/local/var/postgresql@15-project/server.log
```

## Project Todo

- Make importing .csv faster
- Frontend work