import sys
import mysql.connector
import json
from DBERROR import ExistError

configDict=json.loads(open(('./config.json')).read())
'''
Create a database in your local machine's MySQL.
You should fill the config first.
'''



db=mysql.connector.connect(
    host=configDict['host'],
    user=configDict['user'],
    passwd=configDict['passwd']
)
try:
    cursor=db.cursor()

    cursor.execute("show databases")
    isExist=False
    for i in cursor:
        if i[0].decode('utf-8')==configDict['database']:
            isExist=True
    if isExist:
        raise ExistError(configDict['database'])
    cursor.execute("create database {}".format(configDict['database']))

except ExistError:
    print(ExistError.message)

except:
    print('Unexpected error:', sys.exc_info()[0])
finally:
    cursor.close()
    db.close()
    sys.exit(0)




