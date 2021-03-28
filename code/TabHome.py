import streamlit as st
from PIL import Image

#Home tab giving welcome message to participants
def HomeTab():
	st.image(Image.open("imgs/hackpromotion.jpg"), use_column_width=True)
	st.write("Welcome to the Oceanix data challenge. We are happy to recieve your submissions.")
	st.write(
		"Please PUSH all your files in the following repository:\n "
		"https://github.com/CIA-Oceanix/2020a_IMT_SSH_mapping_NATL60")
	st.write(
		"Check out this [link](https://rfablet.github.io/) for more information on OceaniX. ")