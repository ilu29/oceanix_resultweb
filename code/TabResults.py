import streamlit as st
import pandas as pd


from ResultPlots import *


@st.cache(allow_output_mutation=True)
def getUserImages(user):
    print("Caching image data")
    arr = user.openUserNpz("im_plot.npz", "img")
    # res=plot_arrayimg(imgs[value, :, :])
    #Plot each satelital sanpshot of the particiant and cache it
    res = [plot_arrayimg(arr[v, :, :]) for v in range(arr.shape[0])]
    print(arr.shape[0])
    return res


def ResultTab(users):
    st.subheader("Participant List")

    row_array = []
    users_list = []
    #Create a list of particiapnts for internal computation
    for user, data in users.items():
        row_array.append([data.userid, data.name, data.lastname])
        users_list.append(data.userid)

    st.write("Search for user in the following bar by typing user name:")
    option = st.multiselect(
        '', users_list)
    #Show list of all participants
    df = pd.DataFrame(row_array, columns=['User', "Name", "Last Name"])
    if (len(option)) is not 0:
        #Show a table with only the selected participants
        search_df = df[df['User'].isin(option)]
        st.table(search_df)
    else:
        #If not selected participant show all of them
        st.table(df)
    #More than one selected user
    if (len(option)) > 1:
        st.subheader("Comaprison of users")
        # Generate RMS plot concatenating all selected users
        seqgroup = [users[opt].openUserNpz_serie("rms_plot.npz") for opt in option]
        res = plotMultSeq(seqgroup, type="linear")
        st.image(res)
        # Generate Frequency spectral error plot concatenating all selected users
        seqgroup = [users[opt].openUserNpz_serie("freq_plot.npz") for opt in option]
        res = plotMultSeq(seqgroup, type="frequence")
        st.image(res)
    #In the user selction bar there was only one user selected
    if (len(option)) == 1:
        cols = st.beta_columns(2)
        # for usr_ind in range(len(option)):
        cols[0].subheader("Results of %s" % (option[0]))
        #Generate RMS plot
        res1 = plotSingSeq(users[option[0]].openUserNpz_serie("rms_plot.npz"), type="linear")
        #Generate spectral power plot
        res2 = plotSingSeq(users[option[0]].openUserNpz_serie("freq_plot.npz"), type="frequence")
        cols[0].image(res1)
        cols[0].image(res2)
        #Generate images of satelital reconstructed snaptshots
        res = getUserImages(users[option[0]])
        cols[0].write("Move the slider to visualize the reconstructed satelital timelapse")
        #Slider creation
        value = cols[0].slider("Number of frames: "+str(len(res)), 0, len(res)-1, 0, 1)
        # res3 = plot_arrayimg(res[value])
        #Show the snapshot
        cols[0].image(res[value])
