import pandas as pd
import os
import datetime
from ResultPlots import *
from PIL import Image
from httpx_oauth.clients.google import GoogleOAuth2

import ResultsProcessor
import UserFiles
import SessionState

session_state = SessionState.get(capnum=0,repo_submitted=False)
SessionState.repo_submitted=False

wd = os.getcwd()
usersfolder = os.path.join(wd, "generatedData/Users")  # Users folder, absolute path


def main():
	np.random.seed(19680801)



	users_list = UserFiles.getUserslistFromDir(usersfolder)
	users_info = UserFiles.getUsersInfo(usersfolder, users_list)
	user_results = ResultsProcessor.GetUserResults(usersfolder, users_list)
	"""Simple Login App"""
	st.set_page_config(layout="wide")
	st.title("Oceanix Data Challenge")


	st.sidebar.image(Image.open("imgs/im-datawave.jpg"),use_column_width=True)

	menu = ["Home","Results","Submission"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.image(Image.open("imgs/hackpromotion.jpg"), use_column_width=True)
		st.write("Welcome to the Oceanix data challenge. We are happy to recieve your submissions.")
		st.write(
			"Please PUSH all your files in the following repository:\n "
			"https://github.com/CIA-Oceanix/2020a_IMT_SSH_mapping_NATL60")
		st.write(
			"Check out this [link](https://rfablet.github.io/) for more information on OceaniX. ")

	if choice == "Submission":

		st.write("Enter GitHub URL with your code to participate:")
		if SessionState.repo_submitted:
			st.write('Already submited!!!')
		else:
			repo_url = st.text_input("enter link", "https://www.github.com/CIA-Oceanix/2020a_IMT_SSH_mapping_NATL60")



			from captcha.image import ImageCaptcha


			image = ImageCaptcha()
			import random
			if session_state.capnum==0:
				session_state.capnum=random.randint(1000, 10000)
			data = image.generate(str(session_state.capnum))
			st.image(data)
			col1, ca,cb,cc= st.beta_columns(4)
			with col1:
				captcha_usr_in = st.text_input("enter captcha",max_chars=4)

			#st.write(captcha_usr_in)
			#st.write(str(session_state.capnum))



			import re



			def check_form(user_captcha,url):

				pattern = re.compile("https://www.github.com/\S*")
				isgiturl = pattern.match(url)
				#st.write(isgiturl)
				if isgiturl is not None:
					isgiturl = True
				else:
					isgiturl = False
					st.error('Invalid REGEX!!!')

				valid_captcha = False
				if str(session_state.capnum) == user_captcha:
					valid_captcha = True
				else:
					st.error('Invalid CAPTCHA!!!')

				valid_url = False
				try:
					import urllib.request

					req = urllib.request.Request(url)
					with urllib.request.urlopen(req) as response:
						valid_url = True
						#st.write('Submited!!!')
						#verified_subm_form=True
				except:
					st.error('Cannot connect to URL!!!')

				if isgiturl and valid_url and valid_captcha:
					return True
				else:
					return False





			if st.button('Submit'):
				if check_form(captcha_usr_in, repo_url):
					st.info('Submited!!!')
					if SessionState.repo_submitted==True:
						st.write('Already submitted!!!')
					else:
						SessionState.repo_submitted=True
						with open("submissions.txt", "a") as myfile:
							from datetime import date

							today = date.today().strftime("%m/%d/%Y, %H:%M:%S")
							myfile.writelines("%s\n" % l for l in [today, repo_url,''])














	if choice == "Results":
		st.subheader("Participant List")

		row_array=[]
		for user, results in user_results.items():
			row_array.append([user,users_info[user]["name"],users_info[user]["lastname"],results["score"][0]])


		st.write("Search for user in the following bar by typing user name:")
		option = st.multiselect(
		'',users_list)



		df = pd.DataFrame(row_array, columns=['User',"Name","Last Name" ,'Score'])
		if (len(option))is not 0:
			print("User selected:%s" % option[0])
			search_df=df[df['User'].isin(option) ]
			st.table(search_df)
		else:
			st.table(df)

		if (len(option))>1:
			st.subheader("Comaprison of users")

			#	ax.plot(user_results[user]["testplot"][0], user_results[user]["testplot"][1], label=user)
			x=[user_results[user]["testplot"][0] for user in option]
			y = [user_results[user]["testplot"][1] for user in option]
			res=plot_seq(x,y,option)
			st.image(res)


		if (len(option)) > 0:
			cols = st.beta_columns(len(option))
			for usr_ind in range(len(option)):
				cols[usr_ind].subheader("Results of %s"%(option[usr_ind]))
				res1,res2=plotUserResults(user_results[option[usr_ind]])
				cols[usr_ind].image(res1)
				cols[usr_ind].image(res2)






if __name__ == '__main__':
	main()