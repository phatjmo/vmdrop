
"""
Data Access Layer Module
"""

class DAL(object):
    """ Core Data Access Layer Object """

    def __init__(self, config):
        self.db_path = config["db_path"]
        self.db_type = config["db_type"]
        self.db_mod = __import__(self.db_type)

    def get_conn(self):
        """
        Build connection and return.

        -- Doctest --
        """

        conn = self.db_mod.connect(self.db_path) # :memory: is an interesting option
        conn.row_factory = self.db_mod.Row
        return conn

    def table_exists(self, table_name):
        """
        Check if table exists in DB.

        -- Doctest --

        """

        conn = self.get_conn()
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

        conn = self.get_conn()
        cur = conn.cursor()
        cmd = "DROP TABLE IF EXISTS '{0}';".format(table_name)
        # If the carriers table already exists, drop and reload
        cur.execute(cmd)
        conn.commit()
        conn.close()
        return True

    def get_first(self, cmd, params):
        """
        Execute cmd and return all results.

        -- Doctest --

        """
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(cmd, params)
        result = cur.fetchone()
        conn.close()
        return result

    def get_all(self, cmd, params):
        """
        Execute cmd and return all results.

        -- Doctest --

        """
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(cmd, params)
        results = cur.fetchall()
        conn.close()
        return results

    def insert_rows(self, table_name, row_dict):
        """
        Execute cmd and return all results.

        -- Doctest --

        """

        conn = self.get_conn()
        cur = conn.cursor()

        field_str = "("
        value_str = "("
        for field in row_dict.keys():
            field_str = field_str + field + ", "
            value_str = value_str + ":" + field + ", "
        field_str = field_str[:-2] + ")"
        value_str = value_str[:-2] + ")"

        cmd = "INSERT INTO {0} {1} VALUES {2}".format(table_name, field_str, value_str)

        if isinstance(row_dict, list):
            cur.executemany(cmd, row_dict)
        else:
            cur.execute(cmd, row_dict)

        conn.commit()
        conn.close()
        return True

    def create_table(self, table_name, fields):
        """
        Create table with fields.

        --- Doctest --
        """

        conn = self.get_conn()
        cur = conn.cursor()
        field_str = "("
        for field in fields:
            field_str = "{0}{1}, ".format(field_str, field)
        field_str = field_str[:-2] + ")"
        cmd = "CREATE TABLE IF NOT EXISTS {0} {1};".format(table_name, field_str)
        cur.execute(cmd)
        conn.close()
        return True





        