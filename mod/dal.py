
"""
Data Access Layer Module
"""

class DAL(object):
    """ Core Data Access Layer Object """

    def __init__(self, config, **kwargs):
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
        cmd = "SELECT name FROM sqlite_master WHERE type='table' AND name='{0}';".format(table_name)

        if self.get_first(cmd) is None:
            return False
        else:
            return True

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

    def get_none(self, cmd, **params):
        """
        Execute cmd and expect no return rows.
        Used for custom updates, inserts or other commands.

        -- Doctest --

        """
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(cmd, params)
        conn.commit()
        conn.close()
        return True

    def get_first(self, cmd, **params):
        """
        Execute cmd and return first result.

        -- Doctest --

        """
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(cmd, params)
        result = cur.fetchone()
        conn.close()
        return result

    def get_all(self, cmd, **params):
        """
        Execute cmd and return all results.

        -- Doctest --

        """
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(cmd, params)
        results = cur.fetchall()
        conn.close()
        return [dict(x) for x in results]

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

    def update_rows(self, table_name, set_dict, where_dict):
        """
        Update specified table with set_dict for where_dict.
        Assumes strict AND list. Custom updates should use get_none()
        -- Doctest --

        """
        set_str = ""
        where_str = ""
        for key, value in set_dict.items():
            set_str = "{0} {1}={2},".format(set_str, key, self.encapsulate(value))
        set_str = set_str[:-1]

        for key, value in where_dict.items():
            where_str = "{0} {1}={2} AND".format(where_str, key, self.encapsulate(value))
        where_str = where_str[:-4]

        cmd = "UPDATE {0} SET {1} WHERE {2}".format(table_name, set_str, where_str)
        return self.get_none(cmd)

    def create_table(self, table_name, fields):
        """
        Create table with fields.

        --- Doctest --

        >>> test_db = "database/test.db"
        >>> test = DAL({"db_path": test_db, "db_type": "sqlite3"})
        >>> test.create_table("test", ["test1", "test2"])
        True
        >>> assert test.table_exists('test')
        >>> import os
        >>> os.remove(test_db)
        """

        field_str = "("
        for field in fields:
            field_str = "{0}{1}, ".format(field_str, field)
        field_str = field_str[:-2] + ")"
        cmd = "CREATE TABLE IF NOT EXISTS {0} {1};".format(table_name, field_str)
        return self.get_none(cmd)

    def encapsulate(self, var):
        """
        Quick and dirty number check and encapsulation return.
        """
        try:
            complex(var) # for int, long, float and complex
        except ValueError:
            return "'{0}'".format(var)

        return "{0}".format(var)





        