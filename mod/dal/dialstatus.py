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
        
        if "dialID" in kwargs:
            self.__dict__ = self.get_dialstatus(dialID = kwargs["dialID"])
        else
        # for key, value in kwargs.items():
        #     setattr(self, key, value)
        
        

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

    def new_dialstatus(self, call):
        """
        Create new dialstatus record.

        -- Doctest --
        """
        if not self.table_exists('dialstatus'):
            self.create_table('dialstatus',
                              ['dialId integer primary key'
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
                               'errorText'])
        dialstatus = {"vmNumber": call["vmNumber"],
        
        
        self.insert_rows('dialstatus', self.__dict__)
        return True


    def update_dialstatus(self, dialstatus):
        """
        Update dialstatus record.

        -- Doctest --
        """

        where_dict = {"vmNumber": dialstatus.pop("vmNumber"),
                      "campaign": dialstatus.pop("campaign"),
                      "listFile": dialstatus.pop("listFile")}
        self.update_rows("dialstatus", dialstatus, where_dict)
        return True



    def get_dialstatus(self, call):
        """
        Get dialstatus record.

        -- Doctest --
        """
        if "vmNumber" and "campaign" and "listFile" not in call:
            return None 
        new_dict = {}
        where_dict = {"vmNumber": call["vmNumber"],
                      "campaign": call["campaign"],
                      "listFile": call["listFile"]}
        cmd = """SELECT * FROM dialstatus 
                 WHERE vmNumber=:vmNumber AND
                 campaign=:campaign AND
                 listFile=:listFile"""
        result = self.get_first(cmd, call)
        if result is None:
            self.new_dialstatus(dialstatus_dict(call))
            new_dict = dialstatus
        else:
            for col, value in result.items:
                new_dict[col] = value
        return new_dict


    def get_summary(self, campaign, list):
        """
        Get campaign summary.

        -- Doctest --
        """