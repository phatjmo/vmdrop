
""" Handle carrier database """

class Carriers(mod.dal.DAL):
    """
    Data Access for Carriers table

    -- Doctest --
    """
    def __init__(self, *args, **kwargs):
        """
        Init new Carriers object
        """
        super(self.__class__, self).__init__(*args, **kwargs)
        

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
            to_db = [{"carrierName": row['carrierName'], "accessNumber": row['accessNumber']} for row in reader]
        self.insert_rows(to_db)
        return True

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
                AND carrier=:carrier) 
                OR carrier=:carrier
            """
        params = {"area_code": area_code, "carrier": carrier}
        return self.get_first(cmd, params)
