class Error(Exception):
    """
    Base class for exceptions in database problem
    """
    pass

class ConnectionError(Error):
    def __init__(self,name):
        self.message="Can't connect to database %s"%(name)

class DBNameError(Error):
    def __init__(self,name):
        self.message="Can't find %s in your MySQL"%(name)

class ExistError(Error):
    def __init__(self,name):
        self.message="%s is already exist"%(name)

class TableNameError(Error):
    def __init__(self,name):
        self.message="Can't find %s in your database"%(name)

class DisconnectError(Error):
    def __init__(self):
        self.message="The database is not connected"

class LackForm(Error):
    def __init__(self):
        self.message="Recording form haven't been chosen yet."