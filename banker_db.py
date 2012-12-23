import getpass
import os
import os.path
import sqlite3

config_filename = ".banker"

class Transaction():
    def __init__(self, year, month, day, name, amount):
        self.year = year
        self.month = month
        self.day = day
        self.name = name
        self.amount = amount

# Find the database path from ~/.banker
def get_db_path():
    user = getpass.getuser()
    home_dir = os.path.expanduser("~" + user)
    config_path = os.path.join(home_dir, config_filename)
    try:
        config_file = open(config_path, "r")
        db_path = config_file.readline().strip()
        return db_path
    except:
        raise RuntimeError("Failed to read database path")

# Remove any existing database file, then initialise an empty database.
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

# Initialise the database if it doesn't exist,
# then open it and return the connection.
def open_db():
    path = get_db_path()
    if not os.path.isfile(path):
        init_db(path)
    conn = sqlite3.connect(path)
    return conn

def close_db(conn):
    conn.close()

def add_transaction(conn, t):
    cursor = conn.cursor()
    cursor.execute("insert into transactions\
(year, month, day, name, amount) values (?, ?, ?, ?, ?)", 
        (t.year, t.month, t.day, t.name, t.amount))
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

# Get the list of all transactions for the given year and month.
def get_transactions(conn, year, month):
    cursor = conn.cursor()
    cursor.execute("select * from transactions where year=? and month=?\
        order by day", (year, month))
    transactions = []
    for row in cursor:
        transactions.append(
            Transaction(row[1], row[2], row[3], row[4], row[5]))
    return transactions
