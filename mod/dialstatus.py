""" Handle carrier database """
import mod.dal

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
            self.__dict__.update(self.__get_dialstatus(dial_id=kwargs["dial_id"]))
        elif "vm_number" and "campaign" and "list_file" in kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
            self.__dict__.update(self.__new_dialstatus())
        # At this point this is a utility object

    def __new_dialstatus(self):
        """
        Create new dialstatus record.

        -- Doctest --
        """
        if not self.table_exists('dialstatus'):
            self.create_table('dialstatus',
                              ['dial_id integer primary key',
                               'campaign',
                               'vm_number',
                               'access_number',
                               'list_file',
                               'vm_file',
                               'job_start',
                               'sched_time',
                               'call_start',
                               'call_end',
                               'spool_file',
                               'dial_status',
                               'number_type',
                               'error',
                               'error_text'])
        new_dict = dict(campaign='',
                        vm_number='',
                        access_number='',
                        list_file='',
                        vm_file='',
                        job_start='',
                        sched_time='',
                        call_start='',
                        call_end='',
                        spool_file='',
                        dial_status='',
                        number_type='',
                        error='',
                        error_text='')
        for key in new_dict:
            if key in self.__dict__:
                new_dict[key] = self.__dict__[key]

        insert_dict = {}
        for key in new_dict:
            #print "{0}: {1}".format(key, new_dict[key])
            if new_dict[key] == '':
                continue
            else:
                # print "Inserting: {0}: {1}".format(key, new_dict[key])
                insert_dict[key] = new_dict[key]

        # new_dict.update(self.__dict__) <-- Not good because self has more keys than the table!
        self.insert_rows('dialstatus', insert_dict)
        new_dial_id = self.get_first("""SELECT max(dial_id)
                                                FROM dialstatus
                                                WHERE vm_number = :vm_number 
                                                and campaign = :campaign 
                                                and list_file = :list_file""", **new_dict)
        if new_dial_id is None:
            new_dict["dial_id"] = 0
        else:
            new_dict["dial_id"] = new_dial_id[0]
        return new_dict


    def update(self, **updates):
        """
        Update dialstatus record.

        -- Doctest --
        """
        if "dial_id" not in self.__dict__:
            self.__dict__.update(self.__new_dialstatus())
        where_dict = {"dial_id": self.dial_id}
        self.update_rows("dialstatus", updates, where_dict)
        # print self.__dict__
        self.__dict__.update(self.__get_dialstatus(dial_id=self.dial_id))

    def __get_dialstatus(self, **dialstatus):
        """
        Get dialstatus record.

        -- Doctest --
        """
        if "dial_id" not in dialstatus:
            return None
        new_dict = {}
        cmd = """SELECT * FROM dialstatus
                 WHERE dial_id = :dial_id"""
        result = self.get_first(cmd, **dialstatus)
        for col in result.keys():
            new_dict[col] = result[col]
        return new_dict

    def get_all_where(self, **params):
        """
        Get dialstatus record.

        -- Doctest --
        """
        if params == {}:
            where_str = ""
        else:
            where_str = "WHERE"
            for key in params:
                where_str = "{0} {1}=:{1} AND".format(where_str, key)
            where_str = where_str[:-4]
        cmd = """SELECT * FROM dialstatus
                 {0}""".format(where_str)
        return self.get_all(cmd, params)

    def get_summary(self, **cond):
        """
        Get campaign summary.

        -- Doctest --
        """
