import os
import sys
wd=os.getcwd()
sys.path.append( os.path.join(wd, "code"))

import participant

usersfolder = os.path.join(wd, "generatedData/Users")
res=participant.createParticipantDir(usersfolder)