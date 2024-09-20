import streamlit as st
st.set_page_config(

    page_title="笔画",
    page_icon="/opt/bihua/reqgpt/seagent/logo.png",
    layout="wide",  # Optional: Set the layout to wide
    initial_sidebar_state="expanded"  # Optional: Set the initial state of the sidebar
)

import oms_page_sidebar, oms_page_home, oms_config, oms_page_project, oms_page_specification_generation, oms_page_action, oms_page_variable, oms_page_testset, oms_page_upload, oms_page_user_admin, oms_page_specifications, oms_page_specification, oms_page_information, oms_page_documents, oms_page_document
import streamlit_authenticator as stauth
import yaml, os
from yaml.loader import SafeLoader
from dotenv import load_dotenv


st.markdown("""
    <style>
    /* Change the default font size for the entire page */
    html, body, [class*="css"]  {
        font-size: 18px;  /* Adjust this value to change the global font size */
    }
    header[data-testid="stHeader"] {
        display: none;
    }
    .custom-container {
        max-width: 300px;  /* Set the desired width */
        margin: 0 auto;    /* Center the container */
    }
    </style>
    """, unsafe_allow_html=True)


def logout():
    st.session_state["authentication_status"] = "before login"
    st.session_state["login_attempted"] = False
    st.session_state["name"] = None
    st.rerun()


# def clear_cache_on_start():
#     if 'app_initialized' not in st.session_state:
#         logout() # Clear session state at the start of the app
#         st.session_state['app_initialized'] = True  # Mark the app as initialized

# clear_cache_on_start()

load_dotenv()
AUTHENTICATION_YAML_PATH = os.getenv("AUTHENTICATION_YAML_PATH") 

# Load authentication configuration
with open(AUTHENTICATION_YAML_PATH) as file:
    data = yaml.load(file, Loader=SafeLoader)


def validate_login(username, password):
    if username in data['credentials']['usernames']:
        stored_password = data['credentials']['usernames'][username]['password']
        if stored_password == password:
            return "passed", username, data['credentials']['usernames'][username]['name']
    return "failed", None, None

if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = "before login"

if "login_attempted" not in st.session_state:
    st.session_state["login_attempted"] = False


if st.session_state["authentication_status"] == "before login" or st.session_state["authentication_status"] == "failed":
    if st.session_state["login_attempted"] == False:
        
        st.title("笔画智能软件工程平台")
        # login_container = st.container()
        with st.container():
            st.markdown('<div class="custom-container">', unsafe_allow_html=True)
            # st.title("Login Page")
            # Input fields for username and password
            username = st.text_input("用户名", key="login_user_name")
            password = st.text_input("密码", type="password", key="login_password")

            # Button to submit the form
            
            if st.button("登录"):
                st.session_state["login_attempted"] = True
                status, username, name = validate_login(username, password)

                if status == "passed":
                    # Set session state for authentication
                    # user_id = st.session_state["user_identifier"]
                    oms_config.app_state_initialisation(username)
                    st.session_state["authentication_status"] = "passed"
                    st.session_state["name"] = name
                    st.session_state["user_identifier"] = username
                    if username == "admin":
                        # oms_page_user_admin.admin()
                        st.session_state.app_state["page_visible"] = "admin page"
                    else:
                        st.session_state.app_state["page_visible"] = "home page"
                    st.rerun()
                    # st.success(f"Welcome, {name}!")

                    # Optionally hide the login container after successful login
                    # login_container.empty()

                    # Display protected content
                    # st.write("This is some protected content.")
                elif status == "failed":
                    st.session_state["login_attempted"] = False
                    st.session_state["authentication_status"] = "failed"
                    st.write("用户名或密码错误。")
                    # st.error("用户名或密码错误。")
                # login_container.empty()
            else:
                print("button click = false")

if st.session_state["authentication_status"] == "passed":
    # user_id = st.session_state["user_identifier"]
    # oms_config.app_state_initialisation(user_id)
    oms_page_sidebar.add()

    if st.session_state.app_state["page_visible"] == "home page":
        oms_page_home.open()
    elif st.session_state.app_state["page_visible"] == "project page":
        oms_page_project.open()
    elif st.session_state.app_state["page_visible"] == "specifications page":
        # oms_page_specification_generation.open()
        oms_page_specifications.open()
    elif st.session_state.app_state["page_visible"] == "action page":
        oms_page_action.open()
    elif st.session_state.app_state["page_visible"] == "variable page":
        oms_page_variable.open()
    elif st.session_state.app_state["page_visible"] == "testset page":
        oms_page_testset.open()
    elif st.session_state.app_state["page_visible"] == "upload page":
        oms_page_upload.open()
    elif st.session_state.app_state["page_visible"] == "specification page":
        oms_page_specification.open()
    elif st.session_state.app_state["page_visible"] == "information page":
        oms_page_information.open()
    elif st.session_state.app_state["page_visible"] == "documents page":
        oms_page_documents.open()
    elif st.session_state.app_state["page_visible"] == "document page":
        oms_page_document.open()
    elif st.session_state.app_state["page_visible"] == "admin page":
        oms_page_user_admin.admin()
    else:
        pass  
    




