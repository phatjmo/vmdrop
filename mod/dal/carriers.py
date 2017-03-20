
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

        if self.table_exists('carriers'):
            self.drop_table('carriers')

        self.create_table(('carrierName', 'accessNumber'))
        with open(carrier_file, 'rb') as csv_file:
            # csv.DictReader uses first line in file for column headings by default
            line = csv.DictReader(csv_file) # comma is default delimiter
            to_db = [(row['carrierName'], row['accessNumber']) for row in line]
        self.insert_rows(to_db)
        return True
