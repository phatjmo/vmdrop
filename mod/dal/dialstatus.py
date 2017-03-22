""" Handle carrier database """

class Dialstatus(mod.dal.DAL):
    """
    Data Access for dialstatus table
    """

    def dialstatus_dict(self, call):
        """
        Return a dict with the basic dialstatus fields

        'campaign',
        'vmNumber',
        'accessNumber',
        'listFile',
        'vmFile',
        'jobStart',
        'schedTime',
        'callStart',
        'callEnd',
        'callFile',
        'dialStatus',
        'numberType',
        'error',
        'errorText'

        -- Doctest --
        """

    def new_dialstatus(self, dialstatus):
        """
        Create new dialstatus record.

        -- Doctest --
        """
        if not self.table_exists('dialstatus'):
            self.create_table('dialstatus',
                              ('campaign',
                               'vmNumber',
                               'accessNumber',
                               'listFile',
                               'vmFile',
                               'jobStart',
                               'schedTime',
                               'callStart',
                               'callEnd',
                               'callFile',
                               'dialStatus',
                               'numberType',
                               'error',
                               'errorText'))
        self.insert_rows('dialstatus', dialstatus)
        return True


    def update_dialstatus(self, dialstatus):
        """
        Update dialstatus record.

        -- Doctest --
        """


    def get_dialstatus(self, dialstatus):
        """
        Get dialstatus record.

        -- Doctest --
        """


    def get_summary(self, campaign, list):
        """
        Get campaign summary.

        -- Doctest --
        """