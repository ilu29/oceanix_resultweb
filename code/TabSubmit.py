import streamlit as st
from config import *
from captcha.image import ImageCaptcha



def SubmissionTab(SessionState, session_state):
    captcha_usr_in=None


    st.write("Enter Submission URL with your code to participate:")
    if SessionState.repo_submitted:
        st.write('Already submited!!!')
    else:
        repo_url = st.text_input("enter link", "https://www.github.com/CIA-Oceanix/2020a_IMT_SSH_mapping_NATL60")

        if REQ_CAPTCHA:

            #Create a captcha image
            image = ImageCaptcha()
            import random
            if session_state.capnum == 0:
                session_state.capnum = random.randint(1000, 10000)
            #Create a captacha image based on a random n digits number
            data = image.generate(str(session_state.capnum))
            st.image(data)
            col1, ca, cb, cc = st.beta_columns(4)
            with col1:
                captcha_usr_in = st.text_input("enter captcha", max_chars=4)

        # st.write(captcha_usr_in)
        # st.write(str(session_state.capnum))

        import re
        #Check that the URL compliys with all the security steps selected
        def check_form(user_captcha, url, check_captcha=True, check_url_pattern=True, check_url_response=True):

            if check_url_pattern:
                #Check against URL REGEX ex, Github
                pattern = re.compile(REGEX_PATTERN)
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
                #Do an HTML request to check if there is a response
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
            #Check form
            if check_form(captcha_usr_in, repo_url, check_captcha=REQ_CAPTCHA, check_url_response=URL_VERIF,
                          check_url_pattern=PATTERN_VERIF):
                st.info('Submited!!!')
                if SessionState.repo_submitted == True:
                    st.write('Already submitted!!!')
                else:
                    SessionState.repo_submitted = True
                    #Register in a psecific txt the submisison of the participant
                    with open(SUBMISSIONS_FILE, "a") as myfile:
                        from datetime import date

                        today = date.today().strftime("%m/%d/%Y, %H:%M:%S")
                        myfile.writelines("%s\n" % l for l in [today, repo_url, ''])
