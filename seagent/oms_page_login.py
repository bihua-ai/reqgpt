import streamlit as st
import yaml, os
import oms_page_user_admin, oms_config
from yaml.loader import SafeLoader
from dotenv import load_dotenv

def logout():
    st.session_state["authentication_status"] = "before login"
    st.session_state["name"] = None
    # st.session_state.app_state["page_visible"] = "login page"

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

def open():
    # st.session_state["authentication_status"] = "in login page"

    # if "authentication_status" not in st.session_state:
    #     st.session_state["authentication_status"] = None

    # if st.session_state["authentication_status"]:
    #     pass
    #     # Sidebar with username and logout button
    #     # cols = st.sidebar.columns([2, 1])
    #     # cols[0].write(f'欢迎 *{st.session_state["name"]}*')
    #     # if cols[1].button('退出', key="auth_logout"):
    #     #     logout()
    #         # st.sidebar.success('您已成功登出。')

    #     # Main content after login
    #     # st.write("This is some protected content.")
    # else:
    st.title("笔画智能软件工程平台")
    login_container = st.container()
    with login_container:
        # st.title("Login Page")
        # Input fields for username and password
        username = st.text_input("用户名", key="login_user_name")
        password = st.text_input("密码", type="password", key="login_password")

        # Button to submit the form
        if st.button("登录"):
            st.session_state["authentication_status"] = "login clicked"
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
                # st.success(f"Welcome, {name}!")

                # Optionally hide the login container after successful login
                # login_container.empty()

                # Display protected content
                # st.write("This is some protected content.")
            elif status == "failed":
                st.session_state["authentication_status"] = "failed"
                st.write("用户名或密码错误。")


