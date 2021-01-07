import pandas as pd
import os
import datetime
from ResultPlots import *

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
	st.title("My app ("+str(datetime.datetime.now())+")")

	menu = ["Home"]
	choice = st.sidebar.selectbox("Menu",menu)


	if choice == "Home":
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