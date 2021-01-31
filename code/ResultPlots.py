import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st



def plot_seq(x,y,labels=None):

	if not isinstance(x[0], list):

		fig, ax = plt.subplots()

		# Plot the data
		plt.plot(x,y, label='linear')

		# Add a legend
		plt.legend()
		ax.set_title(r'Results')

		import io
		buf = io.BytesIO()
		fig.savefig(buf, format='png')
		return buf


def plot_arrayimg(array):
		fig, ax = plt.subplots()

		# Plot the data
		plt.contourf(array)

		# Add a legend
		plt.legend()
		ax.set_title(r'Map simulation')

		# Tweak spacing to prevent clipping of ylabel
		import io
		buf = io.BytesIO()
		fig.savefig(buf, format='png')
		return buf



def plotUserResults(results):
	res1=plot_seq(results["testplot"][0],results["testplot"][1])
	res2=plot_arrayimg(results["dummyimage"][0])
	return res1,res2



