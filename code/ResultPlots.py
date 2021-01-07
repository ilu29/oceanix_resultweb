import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def test_plot(level):
	# example data
	mu = 100  # mean of distribution
	sigma = 15  # standard deviation of distribution
	x = mu + sigma * np.random.randn(437)

	num_bins = 50

	fig, ax = plt.subplots()

	# Prepare the data
	x = np.linspace(0, 10, 100)
	y=(x/x)*level

	# Plot the data
	plt.plot(x, y, label='linear')

	# Add a legend
	plt.legend()
	ax.set_title(r'Histogram of user privilege')

	# Tweak spacing to prevent clipping of ylabel
	fig.tight_layout()
	st.pyplot(fig)

def plot_seq(x,y):

	fig, ax = plt.subplots()

	# Plot the data
	plt.plot(x,y, label='linear')

	# Add a legend
	plt.legend()
	ax.set_title(r'Result from notebook')

	# Tweak spacing to prevent clipping of ylabel
	fig.tight_layout()
	st.pyplot(fig)

def plot_arrayimg(array):
		fig, ax = plt.subplots()

		# Plot the data
		plt.contourf(array)

		# Add a legend
		plt.legend()
		ax.set_title(r'Map simulation')

		# Tweak spacing to prevent clipping of ylabel
		fig.tight_layout()
		st.pyplot(fig)

def plotUserResults(results):
	plot_seq(results["testplot"][0],results["testplot"][1])
	plot_arrayimg(results["dummyimage"][0])



