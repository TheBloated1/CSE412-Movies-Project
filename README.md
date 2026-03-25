# CSE412 Movies Project

## Requirements

- Flask 3.1.2 (pip install Flask)

## Instructions

### PostgreSQL Setup
1. Make sure PostgreSQL tools on path:
```bash
export PATH="/lib/postgresql/14/bin:$PATH"
```
2. Start PostgreSQL on port 8888

3. Create database named 'project':
```bash
createdb -h 127.0.0.1 -p 8888 -U $USER project
```

### Application
1. Clone repository into a local directory
2. Start PostgreSQL server
3. Start app: ```python run.py```
4. Access the app at: ```https://localhost:5000```
5. Stop the app via CTRL+C

### Debug
- Connect to PostgreSQL project database with psql using: 
```bash
psql -h 127.0.0.1 -p 8888 -U $USER -d project
```

## Project Todo

- Add PostgreSQL (start server in run script and add psycopg2 dependency)
- Build local database from the kaggle source db