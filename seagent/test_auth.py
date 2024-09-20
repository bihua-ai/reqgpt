import streamlit as st
import streamlit_authenticator as stauth
import yaml, os
from yaml.loader import SafeLoader
from dotenv import load_dotenv

load_dotenv()
AUTHENTICATION_YAML_PATH = os.getenv("AUTHENTICATION_YAML_PATH") # /opt/bihua/reqgpt/seagent/.streamlit/authentication.yaml

with open(AUTHENTICATION_YAML_PATH) as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    cookie_key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days'],
    pre_authorized=config.get('preauthorized')
)

st.title("笔画智能软件工程平台")
name, authentication_status, username = authenticator.login(location='main')

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main', key="auth_logout")
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')





