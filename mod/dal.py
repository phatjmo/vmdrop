
import sqlite3
"""
Data Access Layer Module
"""

def generate_carriers(carrier_file):
    """
    Build the carriers table from specified CSV file.
    
    -- Doctest --

    """
    import csv

    conn = sqlite3.connect("database/vmdrop.db") # :memory: is an interesting option
    cur = con.cursor()
    cur.execute("CREATE TABLE carriers (carrierName, accessNumber);")

    with open(carrier_file,'rb') as file:
        # csv.DictReader uses first line in file for column headings by default
        line = csv.DictReader(file) # comma is default delimiter
        to_db = [(row['carrierName'], row['accessNumber']) for row in line]

    cur.executemany("INSERT INTO carriers (carrierName, accessNumber) VALUES (?, ?);", to_db)
    conn.commit()
    conn.close()