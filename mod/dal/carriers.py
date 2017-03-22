
""" Handle carrier database """

class Carriers(mod.dal.DAL):
    """
    Data Access for Carriers table

    -- Doctest --
    """


    def load_carriers(self, carrier_file):
        """
        Build the carriers table from specified CSV file.

        -- Doctest --

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
