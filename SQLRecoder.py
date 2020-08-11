import sys
import json
import pymysql
import traceback

from DBERROR import *

def search_multi_list(source,target):
    tar_type=type(target)
    for i in source:
        if isinstance(i,tar_type):
            if i==target:
                return True
        elif isinstance(i,(list,tuple)):
            if search_multi_list(i,target):
                return True
    return False

attach=lambda x,y:x+' '+y+','
dropTail=lambda x:x[:-1]

class record:
    def __init__(self,config,location):
        self.config=config
        self.location=location

class SQLRecoder:
    def __init__(self):
        self.configDict = json.loads(open(('/home/molijuly/github/SwiftDPP/management/config.json')).read())

    def apply(self,excode):
        try:
            if not hasattr(self,'db'):
                raise DisconnectError()
            if not excode.endswith(';'):
                excode+=';'
            print(excode)
            cursor = self.db.cursor()
            cursor.execute(excode)
            result = cursor.fetchall()
            cursor.close()
            return result
        except DisconnectError:
            print(DisconnectError.message)
            sys.exit(0)
        except:
            print("Unknow error:",sys.exc_info())
            print(traceback.format_exc())
            sys.exit(0)

    def commit(self):
    # Because in MySql, auto-commit is set as default, thus this function is normally needn't be used.
        try:
            if not hasattr(self,'db'):
                raise DisconnectError()
            self.db.commit()
        except DisconnectError:
            print(DisconnectError.message)
            sys.exit(0)
        except:
            print("Unknow error:",sys.exc_info())
            print(traceback.format_exc())
            sys.exit(0)

    def createTable(self,tabelName,NameTypeDict):
        try:
            if not hasattr(self,'db'):
                raise DisconnectError()
            print("Tips: Do not use foreign keys but you can set primary key and other attribute by "
                  "adding them after the type")
            excode='create table %s'%tabelName + ' ('
            excode=excode+'id INT AUTO_INCREMENT PRIMARY KEY,'
            for key,value in NameTypeDict.items():
                excode+=attach(key,value)
            excode=dropTail(excode)
            excode+=');'
            #DEBUG
            print(excode)
            result=self.apply(excode)
            print(result)
            self.selectTable=tabelName
            self.tableForm=NameTypeDict
        except DisconnectError:
            print(DisconnectError.message)
            sys.exit(0)
        except:
            print("Unknow error:", sys.exc_info())
            print(traceback.format_exc())
            sys.exit(0)


    def showTable(self):
        excode="show tables"
        result=self.apply(excode)
        print(result)

    def check(self,checktype,tar):
        excode="show %ss"%checktype
        result=self.apply(excode)
        return search_multi_list(result,tar)

    def useExistTable(self,tableName):
        try:
            if not self.check('table', tableName):
                raise TableNameError(tableName)
            self.selectTable = tableName

        except TableNameError as tn:
            print(tn.message)
            exit(0)
    def deleteTable(self,tableName):
        try:
            if not self.check('table', tableName):
                raise TableNameError(tableName)
            excode="drop table %s"%tableName
            print(self.apply(excode))

        except TableNameError as tn:
            print(tn.message)
            exit(0)
    def note(self,dataList,nomore=False):
    # note will apply the excode until you stop note more which is achieved by sending a signal nomore.
    # When you send nomore as True, the dataDict will be ignored but you need to put a useless value
    # for example None.
        try:
            if not hasattr(self, 'selectTable'):
                raise LackForm
            if not hasattr(self,'excode'):
                if nomore:
                    return
                else:

                    self.excode = '''insert into {} values'''.format(self.selectTable)
            if nomore:
                self.excode=dropTail(self.excode)
                try:
                    result = self.apply(self.excode)
                    self.commit()
                except BrokenPipeError as b:
                    self.wakeUp()
                    result = self.apply(self.excode)
                    self.commit()
                del self.excode
                return
            self.excode+='( null,'
            for i in dataList:
                if i!='null':
                    self.excode += repr(i) + ','
                else:
                    self.excode += 'null' + ','
            self.excode=dropTail(self.excode)+'),'


        except LackForm as lf:
            print(lf.message)
            if hasattr(self,'excode'):
                del self.excode
            exit(0)
        except:
            print("Unknow error:", sys.exc_info())
            print(traceback.format_exc())
            if hasattr(self,'excode'):
                del self.excode
            sys.exit(0)

    def tell(self,tableName):
        return self.apply('select * from %s;'%tableName)

    def getBest(self):
        pass

    def getLocation(self):
        pass

    def getLastID(self):
        return self.apply('select LAST_INSERT_ID()')[0][0]

    def wakeUp(self):
        try:
            self.db = pymysql.connect(self.configDict['host'], self.configDict['user'], self.configDict['passwd'],
                                      self.configDict['database'],port=self.configDict['port'])
            if self.db == None:
                raise ConnectionError(self.configDict['database'])

            cursor = self.db.cursor()

            cursor.execute("SELECT VERSION()")

            data = cursor.fetchone()
            print("Connection is successfully established!")
            print("Database version : %s " % data)

        except ConnectionError:
            print(ConnectionError.message)
        except:
            print("Unknow error:", sys.exc_info())
            print(traceback.format_exc())
            sys.exit(0)
        else:
            cursor.close()

    def sleep(self):
        if hasattr(self, 'excode'):
            del self.excode
        self.db.close()


if __name__=='__main__':
    rd=SQLRecoder()
    rd.wakeUp()
    rd.showTable()
    rd.deleteTable('Field_Problem')
    rd.createTable('Field_Problem',{
        'Field':'CHAR(30)',
        'Problem':'CHAR(50)'
    })
    rd.showTable()
    rd.useExistTable('Field_Problem')
