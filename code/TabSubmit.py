import streamlit as st
from config import *
from captcha.image import ImageCaptcha
import ResultsProcessor
import UserFiles


def SubmissionTab(SessionState, session_state):
    st.write("Enter Submission URL with your code to participate:")
    if SessionState.repo_submitted:
        st.write('Already submited!!!')
    else:
        repo_url = st.text_input("enter link", "https://www.github.com/CIA-Oceanix/2020a_IMT_SSH_mapping_NATL60")

        if REQ_CAPTCHA:


            image = ImageCaptcha()
            import random
            if session_state.capnum == 0:
                session_state.capnum = random.randint(1000, 10000)
            data = image.generate(str(session_state.capnum))
            st.image(data)
            col1, ca, cb, cc = st.beta_columns(4)
            with col1:
                captcha_usr_in = st.text_input("enter captcha", max_chars=4)

        # st.write(captcha_usr_in)
        # st.write(str(session_state.capnum))

        import re

        def check_form(user_captcha, url, check_captcha=True, check_url_pattern=True, check_url_response=True):

            if check_url_pattern:
                pattern = re.compile("https://www.github.com/\S*")
                isgiturl = pattern.match(url)
                # st.write(isgiturl)
                if isgiturl is not None:
                    isgiturl = True
                else:
                    isgiturl = False
                    st.error('Invalid REGEX!!!')
                    return False
            if check_captcha:
                valid_captcha = False
                if str(session_state.capnum) == user_captcha:
                    valid_captcha = True
                else:
                    st.error('Invalid CAPTCHA!!!')
                    return False

            if check_url_response:
                valid_url = False
                try:
                    import urllib.request

                    req = urllib.request.Request(url)
                    with urllib.request.urlopen(req) as response:
                        valid_url = True
                except:
                    st.error('Cannot connect to URL!!!')
                    return False

            return True

        if st.button('Submit'):
            if check_form(captcha_usr_in, repo_url, check_captcha=REQ_CAPTCHA, check_url_response=URL_VERIF,
                          check_url_pattern=PATTERN_VERIF):
                st.info('Submited!!!')
                if SessionState.repo_submitted == True:
                    st.write('Already submitted!!!')
                else:
                    SessionState.repo_submitted = True
                    with open("submissions.txt", "a") as myfile:
                        from datetime import date

                        today = date.today().strftime("%m/%d/%Y, %H:%M:%S")
                        myfile.writelines("%s\n" % l for l in [today, repo_url, ''])
