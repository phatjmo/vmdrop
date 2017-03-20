
"""
Data Access Layer Module
"""

class DAL(object):
    """ Core Data Access Layer Object """

    def __init__(self, config):
        self.db_path = config["db_path"]
        self.db_type = config["db_type"]
        self.db = __import__(self.db_type)

    def table_exists(self, table_name):
        """
        Check if table exists in DB.

        -- Doctest --

        """

        conn = self.db.connect(self.db_path) # :memory: is an interesting option
        cur = conn.cursor()
        cmd = "SELECT name FROM sqlite_master WHERE type='table' AND name='{0}';".format(table_name)
        # If the carriers table already exists, drop and reload
        if cur.execute(cmd) == 0:
            return False
        else:
            return True
        conn.close()

        