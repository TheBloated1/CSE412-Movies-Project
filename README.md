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
1. Make sure PostgreSQL tools on path:
```bash
export PATH="/lib/postgresql/14/bin:$PATH"
```
2. Start PostgreSQL Server on port 8888

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
- Test init database/import .csv/delete database optionally:
```bash
cd app
python3 database.py
```

## Project Todo

- Make importing .csv faster
- Frontend work
