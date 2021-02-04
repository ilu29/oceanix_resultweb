
import os
import json
import numpy as np


class ParticipantUser:

    results={}

    def __init__(self, dir):
        infofile=open( os.path.join(dir, "info.json"))
        info = json.load(infofile)
        infofile.close()
        self.name=info["name"]
        self.lastname = info["lastname"]
        self.userid = info["userid"]
        self.directory=dir

    def openUserNpz(self,fname,name=''):
        container = np.load(os.path.join(self.directory, fname))
        data = [container[key] for key in container][0]
        res=data
        #self.results[name]= res
        return res

    def openUserNpz_serie(self,fname,name=''):

        container=np.load(os.path.join(self.directory,fname))
        data = [container[key] for key in container][0]
        res= {"x":data[0,:] , "y":data[1,:] ,"label":self.userid}
        #self.results[name]= res
        return res

def createParticipantDir(dir):

    tempdir={}

    templist = [ParticipantUser(os.path.join(dir,item)) for item in os.listdir(dir)]
    for item in templist:
            tempdir[item.userid]=item


    return tempdir
