""" Handle carrier database """

class Dialstatus(mod.dal.DAL):
    """
    Data Access for dialstatus table
    """

    def __init__(self, config, **kwargs):
        """
        Init new Dialstatus object
        """
        super(self.__class__, self).__init__(config, **kwargs)

        if "dial_id" in kwargs:
            self.__dict__ = self.get_dialstatus(dial_id=kwargs["dial_id"])
        elif "vm_number" and "campaign" and "list_file" in kwargs:
            self.__dict__ = kwargs
            self.new_dialstatus()
            self.dial_id = self.get_first("SELECT max(dial_id) FROM dialstatus")

        # At this point this is a utility object
        # for key, value in kwargs.items():
        #     setattr(self, key, value)

    def new_dialstatus(self):
        """
        Create new dialstatus record.

        -- Doctest --
        """
        if not self.table_exists('dialstatus'):
            self.create_table('dialstatus',
                              ['dial_id integer primary key'
                               'campaign',
                               'vm_number',
                               'access_number',
                               'list_file',
                               'vm_file',
                               'job_start',
                               'sched_time',
                               'call_start',
                               'call_end',
                               'call_file',
                               'dial_status',
                               'number_type',
                               'error',
                               'error_text'])
        self.insert_rows('dialstatus', self.__dict__)
        return True


    def update_dialstatus(self, **updates):
        """
        Update dialstatus record.

        -- Doctest --
        """
        if "dial_id" in updates:
            where_dict = {"dial_id": updates.pop("dial_id")}
        else:
            where_dict = {"dial_id": self.dial_id}

        self.update_rows("dialstatus", updates, where_dict)
        return True



    def get_dialstatus(self, **dialstatus):
        """
        Get dialstatus record.

        -- Doctest --
        """
        if "dial_id" not in dialstatus:
            return None
        new_dict = {}
        cmd = """SELECT * FROM dialstatus
                 WHERE dial_id = :dial_id"""
        result = self.get_first(cmd, dialstatus)
        for col, value in result.items():
            new_dict[col] = value
        return new_dict

    def get_all_by_campaign(self, campaign):
        """
        Get dialstatus record.

        -- Doctest --
        """
        new_dict = {}
        cmd = """SELECT * FROM dialstatus
                 WHERE campaign = :campaign"""
        result = self.get_first(cmd, dialstatus)
        for col, value in result.items():
            new_dict[col] = value
        return new_dict

    def get_summary(self, **cond):
        """
        Get campaign summary.

        -- Doctest --
        """
