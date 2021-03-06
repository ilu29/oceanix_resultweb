import streamlit as st
import pandas as pd
import ResultsProcessor
import UserFiles
from ResultPlots import *


@st.cache(allow_output_mutation=True)
def getUserImages(user):
    print("Caching image data")
    arr = user.openUserNpz("im_plot.npz", "img")
    # res=plot_arrayimg(imgs[value, :, :])
    res = [plot_arrayimg(arr[v, :, :]) for v in range(arr.shape[0])]
    print(arr.shape[0])
    return res


def ResultTab(users):
    st.subheader("Participant List")

    row_array = []
    users_list = []
    for user, data in users.items():
        row_array.append([data.userid, data.name, data.lastname])
        users_list.append(data.userid)

    st.write("Search for user in the following bar by typing user name:")
    option = st.multiselect(
        '', users_list)

    df = pd.DataFrame(row_array, columns=['User', "Name", "Last Name"])
    if (len(option)) is not 0:
        search_df = df[df['User'].isin(option)]
        st.table(search_df)
    else:
        st.table(df)

    if (len(option)) > 1:
        st.subheader("Comaprison of users")

        seqgroup = [users[opt].openUserNpz_serie("rms_plot.npz") for opt in option]
        res = plotMultSeq(seqgroup, type="linear")
        st.image(res)

        seqgroup = [users[opt].openUserNpz_serie("freq_plot.npz") for opt in option]
        res = plotMultSeq(seqgroup, type="frequence")
        st.image(res)

    if (len(option)) == 1:
        cols = st.beta_columns(2)
        # for usr_ind in range(len(option)):
        cols[0].subheader("Results of %s" % (option[0]))
        res1 = plotSingSeq(users[option[0]].openUserNpz_serie("rms_plot.npz"), type="linear")
        res2 = plotSingSeq(users[option[0]].openUserNpz_serie("freq_plot.npz"), type="frequence")
        cols[0].image(res1)
        cols[0].image(res2)
        res = getUserImages(users[option[0]])
        cols[0].write("Move the slider to visualize the reconstructed satelital timelapse")
        value = cols[0].slider("Number of frames: "+str(len(res)), 0, len(res)-1, 0, 1)
        # res3 = plot_arrayimg(res[value])
        cols[0].image(res[value])
