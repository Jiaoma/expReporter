import torch
import shutil

import os
from os.path import join

from SQLRecoder import SQLRecoder

def saveCheckpoint(state,is_best,filename='checkpoint.pth.tar'):
    torch.save(state,filename)
    if is_best:
        shutil.copyfile(filename,'model_best.pth.tar')


class modelAssistant:
    def __init__(self,expName):
        pass



# Back up the old code
# changed the idea of modelSaver
'''
class modelSaver:
    ''''''
    Though modelSaver only take down limited information but they are the minist for the following,
    you can create new table to take down more information as long as you set the 'expID' from table expSave
    and 'repID' from trainSave as foreign keys.
    ''''''
    def __init__(self):
        self.sqlRecoder=SQLRecoder()
        print('modelSaver want to connect to database')
        self.sqlRecoder.wakeUp()
        try:
            self.sqlRecoder.useExistTable('expSave')
        except:
            self.sqlRecoder.createTable('expSave',
                                        {
                                            'expID':'INT(10) PRIMARY KEY AUTO_INCREMENT',
                                            'expName':'CHAR(50)',
                                            'dataset':'CHAR(50)',
                                            'configs':'CHAR(100)'
                                        })
        try:
            self.sqlRecoder.useExistTable('trainSave')
        except:
            self.sqlRecoder.createTable('trainSave',{
                'repID':'INT(10) PRIMARY KEY AUTO_INCREMENT',
                'expID':'INT(10)',
                'location':'CHAR(50)',
                'epoch':'INT(10)',
                'loss':'FLOAT',
                'CONSTRAINT exp_train_ID':'FOREIGN KEY(expID) REFERENCES expSave(expID)'
            })
        ''''''
        The table of test is named testSave, but it's form I can't defined here for the various possibility of test
        methods may used in testing.
        ''''''

    def wakeUp(self):
        self.sqlRecoder.wakeUp()

    def sleep(self):
        self.sqlRecoder.sleep()

    def setExpInfo(self,expName:str,dataset:str,saveLocation:str,configs:str):
        assert isinstance(expName,str)
        assert isinstance(dataset,str)
        assert isinstance(configs,str)
        assert isinstance(saveLocation)
        assert os.path.isdir(saveLocation)
        self.sqlRecoder.useExistTable('expSave')
        self.sqlRecoder.note([expName,dataset,configs])
        self.sqlRecoder.note(None,nomore=True)
        self.expID=self.sqlRecoder.getLastID()
        self.saveLocation=saveLocation
        self.lossLowest=99999

    def save(self,parameters:dict,fileName:str,epoch:int,loss:float,postlude='.pth.tar',mode='newLowest'):
        ''''''

        :param parameters: dict of parameters of optimizer and net
        :param fileName: the name you want save your parameters as without postlude, the default postlude is '.pth.tar'/
                        And you needn't specify the location here, the location is specified in setExpInfo().
        :param epoch: the epoch of current parameters
        :param loss: the loss of current parameters
        :param postlude: the postlude you want to save your checkpoint as, for most cases you needn't change it.
        :param mode: there are two modes here named 'newLowest' and 'onlyOneLowest', the former one/
                    means write down every checkpoint that is lower than the local lowest, while the/
                    other means write down only one checkpoint that is the lowest in global history.
        :return: None unless error occurs.
        ''''''
        location=join(self.saveLocation,fileName,'_',str(epoch),'_',str(loss),postlude)
        torch.save(parameters,location)
        self.sqlRecoder.useExistTable('trainSave')
        self.sqlRecoder.note([self.expID,location,str(epoch),str(loss)])
        self.sqlRecoder.note(None,nomore=True)
        if loss<self.lossLowest:
            shutil.copyfile(location, join(self.saveLocation,fileName,'_best.pth.tar'))
            self.lossLowest=loss
'''






