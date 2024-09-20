import streamlit as st
import oms_library_project
import os, json
from dotenv import load_dotenv

st.markdown(
    """
    <style>
        .st-emotion-cache-9ycgxx::before {
            content: "将上传文档拖放此处";
        }
        .st-emotion-cache-9ycgxx {
            visibility: hidden;
        }
        .st-emotion-cache-9ycgxx::before {
            visibility: visible;
            position: absolute;
        }

        .st-emotion-cache-1aehpvj::before {
            content: "最大上传文档为200MB";
        }
        .st-emotion-cache-1aehpvj {
            visibility: hidden;
        }
        .st-emotion-cache-1aehpvj::before {
            visibility: visible;
            position: absolute;
        }

        div[data-testid="stFileUploader"] > section[data-testid="stFileUploaderDropzone"] > button[data-testid="baseButton-secondary"] {
            position: relative; /* Ensure button is a positioning context for ::after */
            color: transparent; /* Hide the original button text */
            background: transparent; /* Optional: Remove any background if needed */
        }

        div[data-testid="stFileUploader"] > section[data-testid="stFileUploaderDropzone"] > button[data-testid="baseButton-secondary"]::after {
            content: "选择文档";
            color: black;
            display: block;
            position: absolute;
            width: 140px;
            padding: 1px 5px;
        }
    </style>
    """, unsafe_allow_html=True)

def upload_ui(user_id, project_name=None):
    if project_name is None:
        project_name, project_home_path = oms_library_project.create_project_name(st.session_state.app_state["user_identifier"])
    uploaded = False
    uploaded_files = st.file_uploader("选择上传文档：", accept_multiple_files=True, key="upload_ui", label_visibility="collapsed")
    if uploaded_files and project_name is not None:
        # adjusted_project_name = req_project.create_project_name(user_id, project_identifier, project_name)
        # adjusted_project_name = project_name
        # print(adjusted_project_name)
        st.session_state.app_state["project_name"] = project_name
        oms_library_project.upload_documents(uploaded_files, user_id, project_name=project_name)
        uploaded = True
        
    return uploaded