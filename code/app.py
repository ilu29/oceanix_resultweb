import pandas as pd
import os
import datetime
from ResultPlots import *
from PIL import Image
from httpx_oauth.clients.google import GoogleOAuth2

import ResultsProcessor
import UserFiles




def main():
	np.random.seed(19680801)

	wd = os.getcwd()
	usersfolder = os.path.join(wd, "generatedData/Users")  # Users folder, absolute path

	users_list = UserFiles.getUserslistFromDir(usersfolder)
	users_info = UserFiles.getUsersInfo(usersfolder, users_list)
	user_results = ResultsProcessor.GetUserResults(usersfolder, users_list)
	"""Simple Login App"""
	st.set_page_config(layout="wide")
	st.title("Oceanix Data Challenge")


	st.sidebar.image(Image.open("imgs/im-datawave.jpg"),use_column_width=True)

	menu = ["Home","Results"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.image(Image.open("imgs/hackpromotion.jpg"), use_column_width=True)
		st.write("Welcome to the Oceanix data challenge. We are happy to recieve your submissions.")
		st.write(
			"Please PUSH all your files in the following repository:\n "
			"https://github.com/CIA-Oceanix/2020a_IMT_SSH_mapping_NATL60")
		st.write(
			"Check out this [link](https://rfablet.github.io/) for more information on OceaniX. ")
	if choice == "Results":
		st.subheader("Participant List")

		row_array=[]
		for user, results in user_results.items():
			row_array.append([user,users_info[user]["name"],users_info[user]["lastname"],results["score"][0]])



		option = st.multiselect(
		'search for user',users_list)



		df = pd.DataFrame(row_array, columns=['User',"Name","Last Name" ,'Score'])
		if (len(option))is not 0:
			print("User selected:%s" % option[0])
			search_df=df[df['User'].isin(option) ]
			st.table(search_df)
		else:
			st.table(df)

		if (len(option))is not 0:

			fig, ax = plt.subplots()

			# Plot the data
			for user in option:
				plt.plot(user_results[user]["testplot"][0], user_results[user]["testplot"][1], label=user)

			# Add a legend
			plt.legend()
			ax.set_title(r'Result from notebook')

			# Tweak spacing to prevent clipping of ylabel
			fig.tight_layout()
			st.pyplot(fig)
			for user in option:
				my_expander = st.beta_expander("Results of %s" % user)
				with my_expander:


					plotUserResults(user_results[user])








if __name__ == '__main__':
	main()