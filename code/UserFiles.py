import os
import json
import re


prefix_folder="jupyter-"

def getUserFromFolder(folder_name):
    m = re.search('jupyter-([\S]*)\s*', folder_name)
    if m:
        found = m.group(1)
    else:
        found=None
    return found


def generateUserPath(path,user):
    return os.path.join(path, prefix_folder+user)

def openUserFile(path,user,fname,mode):
    userpath=generateUserPath(path,user)
    filepath=os.path.join(userpath, fname)
    file=None
    if os.path.isdir(userpath):
        try:
            file=open(filepath, mode)
        except OSError:
            print("ERROR: cannot open " % filepath)
    else:
        print("ERROR: User folder: %s doesnt exist" % user)

    return file


def getUserslistFromDir(path):
    res=None
    try:
        res=[ getUserFromFolder(item) for item in os.listdir(path) if os.path.isdir(os.path.join(path, item)) and getUserFromFolder(item)  is not None ]
    except OSError:
        print("ERROR: Recollection of users in %s failed" % path)
    return res


def createUsersfolder(user_comp_path,uslist,prefix=""):

    if not os.path.exists(user_comp_path):
        os.makedirs(user_comp_path)
    for user in uslist:
        user_full_path=generateUserPath(user_comp_path,user)
        try:
            os.mkdir(user_full_path)
        except OSError:
            print("ERROR: Creation of the directory %s failed" % user_full_path)
        else:
            print("Successfully created the directory %s " % user_full_path)

def createUsersInfo(user_comp_path,usersinfo):

    #userlist=getUserslistFromDir(user_comp_path)
    for user, info in usersinfo.items():
        user_full_path = generateUserPath(user_comp_path,user)
        try:
            os.mkdir(user_full_path)
        except OSError:
            pass
        try:
            file = openUserFile(user_comp_path,user,"info.json","w+")
            json.dump(info,file)
            file.close()

        except OSError:
            print("ERROR: Creation of the info for user %s failed" % user)

def loadUserInfo(user_comp_path,user):
    info={}
    try:
        file = openUserFile(user_comp_path, user, "info.json", "r+")
        info=json.load(file)
        file.close()

    except OSError:
        print("ERROR: Cannot load ""info.json"" of %s" % user)
    return info


def getUsersInfo(user_comp_path,userlist):
    info = {}
    for user in userlist:
        info[user] = loadUserInfo(user_comp_path,user)
    return info