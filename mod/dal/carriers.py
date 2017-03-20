
import sqlite3
""" Handle carrier database """

class Carriers(mod.dal.DAL):
    """
    Data Access for Carriers database
    """




    def load_carriers(self, carrier_file):
        """
        Build the carriers table from specified CSV file.

        -- Doctest --

        """
        import csv

        conn = sqlite3.connect(self.db_path) # :memory: is an interesting option
        cur = conn.cursor()

        # If the carriers table already exists, drop and reload
        if not self.table_exists('carriers'):
            cur.execute(
                "CREATE TABLE carriers (carrierName, accessNumber);")
            with open(carrier_file, 'rb') as csv_file:
                # csv.DictReader uses first line in file for column headings by default
                line = csv.DictReader(csv_file) # comma is default delimiter
                to_db = [(row['carrierName'], row['accessNumber']) for row in line]
            cur.executemany(
                "INSERT INTO carriers (carrierName, accessNumber) VALUES (?, ?);", to_db)
            conn.commit()
        conn.close()
        return True
