import streamlit as st
st.set_page_config(

    page_title="笔画",
    page_icon="/opt/bihua/reqgpt/seagent/logo.png",
    layout="wide",  # Optional: Set the layout to wide
    initial_sidebar_state="expanded"  # Optional: Set the initial state of the sidebar
)


import oms_page_login, oms_page_sidebar, oms_page_home, oms_config, oms_page_project, oms_page_specification_generation, oms_page_action, oms_page_variable, oms_page_testset, oms_page_upload, oms_page_user_admin
import streamlit_authenticator as stauth
import yaml, os
from yaml.loader import SafeLoader
from dotenv import load_dotenv
######################################################
# configuration
######################################################

st.markdown("""
    <style>
    /* Change the default font size for the entire page */
    html, body, [class*="css"]  {
        font-size: 18px;  /* Adjust this value to change the global font size */
    }
    header[data-testid="stHeader"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

#####################################################
# Clear cache
#####################################################
def clear_cache_on_start():
    if 'app_initialized' not in st.session_state:
        st.session_state.clear()  # Clear session state at the start of the app
        st.session_state['app_initialized'] = True  # Mark the app as initialized

clear_cache_on_start()


######################################################
# Authentication page
######################################################
# load_dotenv()
# AUTHENTICATION_YAML_PATH = os.getenv("AUTHENTICATION_YAML_PATH") 

# # Load authentication configuration
# with open(AUTHENTICATION_YAML_PATH) as file:
#     config = yaml.load(file, Loader=SafeLoader)

# # Setup authenticator
# authenticator = stauth.Authenticate(
#     credentials=config['credentials'],
#     cookie_name=config['cookie']['name'],
#     cookie_key=config['cookie']['key'],
#     cookie_expiry_days=config['cookie']['expiry_days'],
#     pre_authorized=config.get('preauthorized')
# )

# App title
# st.title("智能软件工程平台")
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = "before login"

if st.session_state["authentication_status"] == "before login":
    oms_page_login.open()

if st.session_state["authentication_status"] == "failed":
    # oms_page_login.open()
    pass

if st.session_state["authentication_status"] == "login clicked":
    pass
if st.session_state["authentication_status"] == "passed":
    # user_id = st.session_state["user_identifier"]
    # oms_config.app_state_initialisation(user_id)

    if st.session_state.app_state["page_visible"] == "admin page":
        oms_page_user_admin.admin()
    # elif st.session_state.app_state["page_visible"] == "login page":
    #     oms_page_login.open()
    else:
        oms_page_sidebar.add()

        if st.session_state.app_state["page_visible"] == "home page":
            oms_page_home.open()
        elif st.session_state.app_state["page_visible"] == "project page":
            oms_page_project.open()
        elif st.session_state.app_state["page_visible"] == "specification generation page":
            oms_page_specification_generation.open()
        elif st.session_state.app_state["page_visible"] == "action page":
            oms_page_action.open()
        elif st.session_state.app_state["page_visible"] == "variable page":
            oms_page_variable.open()
        elif st.session_state.app_state["page_visible"] == "testset page":
            oms_page_testset.open()
        elif st.session_state.app_state["page_visible"] == "upload page":
            oms_page_upload.open()
        # elif st.session_state.app_state["page_visible"] == "admin page":
        #     oms_page_user_admin.admin()
        # elif st.session_state.app_state["page_visible"] == "login page":
        #     oms_page_login.open()
        else:
            pass 
    


    

# # Authentication
# # name, authentication_status, username = authenticator.login(location='main')

# if st.session_state["authentication_status"]:
#     cols = st.sidebar.columns([2, 1])
#     cols[0].write(f'欢迎 *{st.session_state["name"]}*')
#     authenticator.logout('退出', 'sidebar', key="auth_logout")

#     if username == "admin":
#         oms_page_user_admin.admin()
#         print("test here")
#     else:
#     ######################################################
#     # assemble pages
#     ######################################################
#         # create user folders if not there.
#         # print(f"username = {username}")
#         # user_id = "eric"
#         user_id = username
#         print("userid")
#         print(user_id)
#         oms_config.app_state_initialisation(user_id)

#         oms_page_sidebar.add()

#         if st.session_state.app_state["page_visible"] == "home page":
#             oms_page_home.open()
#         elif st.session_state.app_state["page_visible"] == "project page":
#             oms_page_project.open()
#         elif st.session_state.app_state["page_visible"] == "specification generation page":
#             oms_page_specification_generation.open()
#         elif st.session_state.app_state["page_visible"] == "action page":
#             oms_page_action.open()
#         elif st.session_state.app_state["page_visible"] == "variable page":
#             oms_page_variable.open()
#         elif st.session_state.app_state["page_visible"] == "testset page":
#             oms_page_testset.open()
#         elif st.session_state.app_state["page_visible"] == "upload page":
#             oms_page_upload.open()
#         else:
#             pass 



