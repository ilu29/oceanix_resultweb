import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st



#Helper plotting functions

def FreqSequence_PlotConfig(plt,ax):
	# Add a legend
	plt.legend()
	ax.set_title(r'Results')

	ax.set_xlabel("Wavenumber", fontweight='bold')
	ax.set_ylabel("Power spectral density (m2/(cy/km))", fontweight='bold')
	ax.set_xscale('log');
	ax.set_yscale('log')
	plt.legend(loc='best', prop=dict(size='small'), frameon=False)
	plt.xticks([50, 100, 200, 500, 1000], ["50km", "100km", "200km", "500km", "1000km"])
	ax.invert_xaxis()
	plt.grid(which='both', linestyle='--')


def BaseSequence_PlotConfig(plt,ax):
		plt.legend()
		ax.set_title(r'Results')

#Plot multiple sequences inside the same plot, for comparing participants
def plotMultSeq(seqgroup, type="frequence"):
	import io
	buf = io.BytesIO()

	fig, ax = plt.subplots()

	for seq in seqgroup:

		ax.plot(seq["x"], seq["y"], label=seq["label"])
		#print("label %s" % seq["label"])

	if type == "linear":
		BaseSequence_PlotConfig(plt, ax)
	elif type == "frequence":
		FreqSequence_PlotConfig(plt, ax)
	fig.savefig(buf, format='png', bbox_inches="tight")

	return buf

#Single sequence plotting logic
def plotSingSeq(seq, type="frequence"):
	import io
	buf = io.BytesIO()


	fig, ax = plt.subplots()

	ax.plot(seq["x"], seq["y"], label=seq["label"])

	if type=="linear":
		BaseSequence_PlotConfig(plt, ax)
	elif type == "frequence":
		FreqSequence_PlotConfig(plt, ax)



	fig.savefig(buf, format='png', bbox_inches = "tight")

	return buf


def plot_freqseq(x,y,label='None'):
	import io
	buf = io.BytesIO()

	if not isinstance(x[0], (list,np.ndarray)):

		fig, ax = plt.subplots()
		# Plot the data
		plt.plot(x,y, label='linear')

		# Add a legend
		plt.legend()
		ax.set_title(r'Results')

		ax.set_xlabel("Wavenumber", fontweight='bold')
		ax.set_ylabel("Power spectral density (m2/(cy/km))", fontweight='bold')
		ax.set_xscale('log');
		ax.set_yscale('log')
		plt.legend(loc='best', prop=dict(size='small'), frameon=False)
		plt.xticks([50, 100, 200, 500, 1000], ["50km", "100km", "200km", "500km", "1000km"])
		ax.invert_xaxis()
		plt.grid(which='both', linestyle='--')


		fig.savefig(buf, format='png', bbox_inches = "tight")


	else:
		fig, ax = plt.subplots()
		# fig.update_layout(width=400, height=400)

		for i in range(len(label)):
			#print(label[i])
			ax.plot(x[i], y[i], label=label[i])

		ax.legend()
		ax.set_title(r'Result from notebook')

		# Add a legend
		#plt.legend()
		ax.set_title(r'Results')

		ax.set_xlabel("Wavenumber", fontweight='bold')
		ax.set_ylabel("Power spectral density (m2/(cy/km))", fontweight='bold')
		ax.set_xscale('log');
		ax.set_yscale('log')
		plt.legend(loc='best', prop=dict(size='small'), frameon=False)
		plt.xticks([50, 100, 200, 500, 1000], ["50km", "100km", "200km", "500km", "1000km"])
		ax.invert_xaxis()
		plt.grid(which='both', linestyle='--')

		fig.savefig(buf, format='png')
	return buf

def plot_arrayimg(array):
		fig, ax = plt.subplots()

		# Plot the data
		plt.contourf(array)

		# Add a legend
		#plt.legend()
		ax.set_title(r'Map simulation (delete)')

		# Tweak spacing to prevent clipping of ylabel
		import io
		buf = io.BytesIO()
		fig.savefig(buf, format='png')
		return buf






