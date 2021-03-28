
import os
import json
import numpy as np
import random

from config import *

#Participant representation object
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
    #Open an NPZ
    def openUserNpz(self,fname,name=''):
        container = np.load(os.path.join(self.directory, fname))
        data = [container[key] for key in container][0]
        res = data
        #self.results[name]= res
        return res
    #Open npz containing a series to plot
    def openUserNpz_serie(self,fname,name=''):

        container=np.load(os.path.join(self.directory,fname))
        data = [container[key] for key in container][0]
        #res= {"x":data[0,:] , "y":data[1,:] +abs(np.random.normal(loc=0.0, scale=0.3, size=data[1,:].shape )),"label":self.userid}
        res = {"x": data[0, :], "y": data[1, :] ,
               "label": self.userid}
        #self.results[name]= res
        return res

#Create a now partiicpant
def createParticipant(dir):
    mandatoyFiles={"info.json","freq_plot.npz","rms_plot.npz","im_plot.npz"}
    #Does the participant folder has all necessary folders
    for fn in mandatoyFiles:
        if  not os.path.exists(os.path.join(dir,fn)):
            return None
    return ParticipantUser(dir)

#Create the participant list by analysing all folders in the user dir
def getParticipantDir(dir):

    tempdir={}

    templist = []

    for item in os.listdir(dir):
        p=createParticipant(os.path.join(dir,item))
        #Should we create even if not all files are present
        if p is not None or not IGNORE_IF_MISSING_FILES:
            templist.append(p)
    for item in templist:
            tempdir[item.userid]=item


    return tempdir

#For helping the creation of the particiapnt info files
def createTemplateInfos(dir):
    #print("Analysing existence of info.json in user folders")
    for d in os.listdir(dir):
        #print(os.path.join(dir,d,"info.json"))
        if not os.path.exists(os.path.join(dir,d,"info.json")):
            #print("Creating a dummy file in"+d)
            #Dummy data to be modified by manager of contest
            duminfo={'name':'dummyname','lastname':'dummylastname','userid':'dummyid'}
            with open(os.path.join(dir,d,"info.json"), 'w') as outfile:
                json.dump(duminfo, outfile)
