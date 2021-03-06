
import os
import json
import numpy as np

from config import *

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
        res = data
        #self.results[name]= res
        return res

    def openUserNpz_serie(self,fname,name=''):

        container=np.load(os.path.join(self.directory,fname))
        data = [container[key] for key in container][0]
        res= {"x":data[0,:] , "y":data[1,:] ,"label":self.userid}
        #self.results[name]= res
        return res


def createParticipant(dir):
    mandatoyFiles={"info.json","freq_plot.npz","rms_plot.npz","im_plot.npz"}
    for fn in mandatoyFiles:
        if  not os.path.exists(os.path.join(dir,fn)):
            return None
    return ParticipantUser(dir)

def getParticipantDir(dir):

    tempdir={}

    templist = []

    for item in os.listdir(dir):
        p=createParticipant(os.path.join(dir,item))
        if p is not None or not IGNORE_IF_MISSING_FILES:
            templist.append(p)
    for item in templist:
            tempdir[item.userid]=item


    return tempdir


def createTemplateInfos(dir):
    #print("Analysing existence of info.json in user folders")
    for d in os.listdir(dir):
        #print(os.path.join(dir,d,"info.json"))
        if not os.path.exists(os.path.join(dir,d,"info.json")):
            #print("Creating a dummy file in"+d)
            duminfo={'name':'dummyname','lastname':'dummylastname','userid':'dummyid'}
            with open(os.path.join(dir,d,"info.json"), 'w') as outfile:
                json.dump(duminfo, outfile)
