#
#
# uploaded_file = st.file_uploader("Choose a file")
#
#
#
# 		if path.exists("result.csv"):
# 			print("Notebook excecuted")
# 			# res=getresults_notebook("notebooks/output.ipynb")
# 			res = np.genfromtxt('result.csv', delimiter=',')
# 			print(res)
# 			plot_seq(res)
#
# 		if uploaded_file is not None:
# 			# To read file as bytes:
# 			bytes_data = uploaded_file.read()
# 			#st.write(bytes_data)
# 			print("file uploaded")
# 			st.info("File uploaded")
#
# 			filename = os.path.join(dirname, 'notebooks/temp.ipynb', )
# 			file = open(filename, 'wb')
# 			file.write(bytes_data)
# 			file.close()
# 			if st.button("Run"):
#
#
# 				def task():
# 					pm.execute_notebook(
# 						'notebooks/temp.ipynb',
# 						'notebooks/output.ipynb'
# 					)
# 					print("finished")
#
# 				thread = threading.Thread(target=task)
# 				add_report_ctx(thread)
# 				thread.start()
# 				print("hola")