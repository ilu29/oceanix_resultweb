import UserFiles
import os
import numpy as np

def generateDummyResults(usersfolder):

    users_list = UserFiles.getUserslistFromDir(usersfolder)



    for user in users_list:
        #dummy graph
        user_path=UserFiles.generateUserPath(usersfolder,user)
        file_path=os.path.join(user_path, "dummyplot.npz")
        data_y = np.random.rand(10)
        data_x = np.arange(10)
        data=[data_x,data_y]
        np.savez(file_path, *data)

        #dummy score
        file_path = os.path.join(user_path, "score.npz")
        np.savez(file_path, np.random.randint(0,10))

        #dummy array
        x = np.arange(-5, 5, 0.1)
        y = np.arange(-5, 5, 0.1)
        xx, yy = np.meshgrid(x, y, sparse=True)
        z = np.sin(xx ** 2 + yy ** 2 )
        file_path = os.path.join(user_path, "image.npz")
        np.savez(file_path, z)


def OpenUserResult(usersfolder,user):
    res_filedict={"testplot": "dummyplot.npz","score":"score.npz","dummyimage":"image.npz"}

    user_path = UserFiles.generateUserPath(usersfolder,user)
    result={}

    for resultname, filename in res_filedict.items():
        file_path = os.path.join(user_path, filename)
        container = np.load(file_path)
        data = [container[key] for key in container]
        result[resultname]=data
    return result

def GetUserResults(usersfolder,userlist):
    results={}
    for user in userlist:
        results[user]=OpenUserResult(usersfolder,user)
    return results
