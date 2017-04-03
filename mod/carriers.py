
""" Handle carrier database """
import mod.dal

class Carriers(mod.dal.DAL):
    """
    Data Access for Carriers table

    -- Doctest --
    """
    def __init__(self, config, **kwargs):
        """
        Init new Carriers object
        """
        super(self.__class__, self).__init__(config, **kwargs)
        print self.table_exists('carriers')
        if not self.table_exists('carriers') or self.get_first("SELECT * FROM carriers") is None:
            print "Carriers table doesn't exist, loading file from config..."
            self.load_carriers(config["carrier_file"])

    def __test_csv(self):
        """
        Generate test CSV carrier file for other carrier testing.

        -- Doctest --

        """

        import csv
        import tempfile
        test_csv = tempfile.mkstemp(suffix='.csv')[1]

        with open(test_csv, 'w') as csvfile:
            fieldnames = ['carrierName', 'accessNumber']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'carrierName': 'T-Mobile', 'accessNumber': '+18056377243'})
            writer.writerow({'carrierName': 'Verizon', 'accessNumber': '+18056377243'})
            writer.writerow({'carrierName': 'Sprint', 'accessNumber': '+18056377243'})
        return test_csv


    def load_carriers(self, carrier_file):
        """
        Build the carriers table from specified CSV file.

        -- Doctest --

        >>>import os
        >>>carriers = Carriers({"db_path": ':memory:', "db_type": 'sqlite3'})
        >>>test_csv = __test_csv()
        >>>carriers.load_carriers(test_csv)
        True
        >>>os.remove(test_csv)

        """
        import csv

        if self.table_exists('carriers'):
            self.drop_table('carriers')

        self.create_table('carriers', ('carrierName', 'accessNumber'))
        with open(carrier_file, 'rb') as csv_file:
            # csv.DictReader uses first line in file for column headings by default
            reader = csv.DictReader(csv_file) # comma is default delimiter
            # to_db = [(row['carrierName'], row['accessNumber']) for row in reader]
            # for row in reader:
            #     print row
            to_db = [{"carrierName": row['carrierName'],
                      "accessNumber": row['accessNumber']} for row in reader]
        self.insert_rows('carriers', to_db)

    def get_access_number(self, carrier, number):
        """
        Get the best access number for the specified carrier and mobile number.

        -- Doctest --

        >>>import os
        >>>carriers = Carriers({"db_path": ':memory:', "db_type": 'sqlite3'})
        >>>test_csv = __test_csv()
        >>>carriers.load_carriers(test_csv)
        True
        >>>carriers.get_access_number('T-Mobile', '4805551212')
        '+18056377243'
        >>>os.remove(test_csv)
        """
        area_code = number[:3]
        cmd = """SELECT accessNumber
                FROM carriers 
                WHERE (substr(accessNumber,1,3)=:area_code 
                AND carrierName=:carrier) 
                OR carrierName=:carrier
            """
        params = {"area_code": area_code, "carrier": carrier}
        result = self.get_first(cmd, **params)
        if result is None:
            return ''
        else:
            return result[0]
