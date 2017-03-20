
"""
Data Access Layer Module
"""

class DAL(object):
    """ Core Data Access Layer Object """

    def __init__(self, config):
        self.db_path = config["db_path"]
        self.db_type = config["db_type"]
        self.db_mod = __import__(self.db_type)

    def table_exists(self, table_name):
        """
        Check if table exists in DB.

        -- Doctest --

        """

        conn = self.db_mod.connect(self.db_path) # :memory: is an interesting option
        cur = conn.cursor()
        cmd = "SELECT name FROM sqlite_master WHERE type='table' AND name='{0}';".format(table_name)
        # If the carriers table already exists, drop and reload
        if cur.execute(cmd) == 0:
            return False
        else:
            return True
        conn.close()

    def drop_table(self, table_name):
        """
        Drop specified table.

        -- Doctest --

        """

        conn = self.db_mod.connect(self.db_path) # :memory: is an interesting option
        cur = conn.cursor()
        cmd = "DROP TABLE IF EXISTS '{0}';".format(table_name)
        # If the carriers table already exists, drop and reload
        cur.execute(cmd)
        conn.commit()
        conn.close()

    def get_first(self, cmd, params):
        """
        Execute cmd and return all results.

        -- Doctest --

        """
        conn = self.db_mod.connect(self.db_path) # :memory: is an interesting option
        cur = conn.cursor()
        cur.execute(cmd, params)
        result = cur.fetchone()
        conn.close()
        return results

    def get_all(self, cmd, params):
        """
        Execute cmd and return all results.

        -- Doctest --

        """
        conn = self.db_mod.connect(self.db_path) # :memory: is an interesting option
        cur = conn.cursor()
        cur.execute(cmd, params)
        results = cur.fetchall()
        conn.close()
        return results

    def insert_rows(self, cmd, values):
        """
        Execute cmd and return all results.

        -- Doctest --

        """

        conn = self.db_mod.connect(self.db_path) # :memory: is an interesting option
        cur = conn.cursor()

        if isinstance(values, list):
            cur.executemany(cmd, values)
        else:
            cur.execute(cmd, values)

        conn.commit()
        conn.close()
        return True

    def create_table(self, table_name, fields):
        """
        Create table with fields.

        --- Doctest --
        """

        conn = self.db_mod.connect(self.db_path) # :memory: is an interesting option
        cur = conn.cursor()
        field_str = "("
        for field in fields:
            field_str = "{0}{1}, ".format(field_str, field)
        field_str = field_str[:-2] + ")"
        cmd = "CREATE TABLE IF NOT EXISTS {0} {1};".format(table_name, field_str)
        cur.execute(cmd)
        conn.close()





        