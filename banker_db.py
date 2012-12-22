import getpass
import os
import os.path
import sqlite3

config_filename = ".banker"

def get_db_path():
    user = getpass.getuser()
    home_dir = os.path.expanduser("~" + user)
    config_path = os.path.join(home_dir, config_filename)
    try:
        config_file = open(config_path)
        db_path = config_file.readline().strip()
        return db_path
    except:
        raise RuntimeError("Failed to read database path")

def init_db(path):
    if os.path.isfile(path):
        os.remove(path)
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("create table transactions(\
id INTEGER PRIMARY KEY,\
year INTEGER,\
month INTEGER,\
day INTEGER,\
name TEXT(50),\
amount INTEGER)")
    conn.close()

def open_db():
    path = get_db_path()
    if not os.path.isfile(path):
        init_db(path)
    conn = sqlite3.connect(path)
    return conn

def close_db(conn):
    conn.close()

def add_transaction(conn, year, month, day, name, amount):
    cursor = conn.cursor()
    cursor.execute("insert into transactions\
(year, month, day, name, amount) values (?, ?, ?, ?, ?)", 
        (year, month, day, name, amount))
    conn.commit()

# Get the list of all years for which we have transactions.
def get_years(conn):
    cursor = conn.cursor()
    cursor.execute("select distinct year from transactions order by year")
    years = []
    for row in cursor:
        years.append(row[0])
    return years

# Get the list of all months for which we have transactions for a given year.
def get_months(conn, year):
    cursor = conn.cursor()
    cursor.execute("select distinct month from transactions where year=?\
order by month", (year,))
    months = []
    for row in cursor:
        months.append(row[0])
    return months
