import matplotlib.pyplot as plt

#np.random.seed(19680001)



# userdb=database.User_MYSQL_Database()
#
# userdb.connect()
#
# userdb.create_usertable()
#
# userdb.add_userdata("pepe","123",2)
# print(userdb.view_all_users())
# print(userdb.login_user("pepe","123"))


import os

import sys
wd=os.getcwd()
sys.path.append( os.path.join(wd, "code"))


import UserFiles






wd=os.getcwd()

usersfolder = os.path.join(wd, "generatedData/Users")


#file=UserFiles.openUserFile(os.path.join(wd, "Users"),"carlos","hola.txt","w+")
#if file is not None:
#    file.writelines(["Holis a todes"])
#    file.close()
UserFiles.createUsersfolder(usersfolder, ["lili23", "carl456"])
users_infodict={
    "lili23":{"name":"Liliana" ,"lastname":"Sario" },
    "carl456":{"name":"Carlos" ,"lastname":"Rememtien" },
"rob23":{"name":"robert" ,"lastname":"Tuqui" },
"nasii83":{"name":"Alinasia" ,"lastname":"Marelo" },
"tipi49":{"name":"Matias" ,"lastname":"Ponsio" },
                }
UserFiles.createUsersInfo(usersfolder, users_infodict)
print(UserFiles.loadUserInfo(usersfolder, "lili23"))
users= UserFiles.getUserslistFromDir(usersfolder)
print (users)

import ResultsProcessor

ResultsProcessor.generateDummyResults(usersfolder)
res= ResultsProcessor.OpenUserResult(usersfolder, "lili23")
#print(res)

#fig, ax = plt.subplots()
#print(res["score"][0])

#print("score of %s is :%d"%("carlos",res["score"][0]))

#plt.contourf(res["dummyimage"][0])
#plt.show()
print("!"+UserFiles.getUserFromFolder("jupyter-ilan ")+"!")

path="/../home"
res=[ item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))]
print(res)



import http.client

#c = http.client.HTTPConnection("www.github.com/CIA-Oceanix/2020a_IMT_SSH_mapping_NATL60")
#c.request("HEAD", '')
    #if c.getresponse().status == 200:
     #   print("success")


import urllib.request

req = urllib.request.Request("https://www.github.com/CIA-Oceanix/2020a_IMT_SSH_mapping_NATL60")
with urllib.request.urlopen(req) as response:
   the_page = response.read()



import re
pattern = re.compile("https://www.github.com/\S*")
isgiturl = pattern.match("https://www.github.com/CIA-Oceanix/2020a_IMT_SSH_mapping_NATL60")
print(isgiturl)