import os
import SessionState
import participant
from TabHome import *
from TabResults import *
from TabSubmit import *

from config import *

session_state = SessionState.get(capnum=0,repo_submitted=False)
SessionState.repo_submitted=False

wd = os.getcwd()
usersfolder = os.path.join(wd, USR_FOLDER_DIR)  # Users folder, absolute path



def main():
	np.random.seed(19680801)

	#participant.createTemplateInfos(usersfolder)
	users = participant.getParticipantDir(usersfolder)

	"""Simple Login App"""
	st.set_page_config(layout="wide")
	st.title("Oceanix Data Challenge")


	st.sidebar.image(Image.open("imgs/im-datawave.jpg"),use_column_width=True)

	menu = ["Home","Results","Submission"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		HomeTab()

	if choice == "Submission":
		SubmissionTab(SessionState, session_state)



	if choice == "Results":
		ResultTab(users)




if __name__ == '__main__':
	main()