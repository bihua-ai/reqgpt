import streamlit as st
import req_project, req_navigation_component, seagent_specs
import os, json
from dotenv import load_dotenv
import streamlit as st

languages = {
    "button": "浏览文件",
    "instructions": "将文件拖放到这里",
    "limits": "每个文件限制为200MB",
}

hide_label = (
    """
<style>
    div[data-testid="stFileUploader"]>section[data-testid="stFileUploadDropzone"]>button[data-testid="baseButton-secondary"] {
       color:white;
    }
    div[data-testid="stFileUploader"]>section[data-testid="stFileUploadDropzone"]>button[data-testid="baseButton-secondary"]::after {
        content: "BUTTON_TEXT";
        color:black;
        display: block;
        position: absolute;
    }
    div[data-testid="stFileDropzoneInstructions"]>div>span {
       visibility:hidden;
    }
    div[data-testid="stFileDropzoneInstructions"]>div>span::after {
       content:"INSTRUCTIONS_TEXT";
       visibility:visible;
       display:block;
    }
     div[data-testid="stFileDropzoneInstructions"]>div>small {
       visibility:hidden;
    }
    div[data-testid="stFileDropzoneInstructions"]>div>small::before {
       content:"FILE_LIMITS";
       visibility:visible;
       display:block;
    }
</style>
""".replace(
        "BUTTON_TEXT", languages.get("button")
    )
    .replace("INSTRUCTIONS_TEXT", languages.get("instructions"))
    .replace("FILE_LIMITS", languages.get("limits"))
)

st.markdown(hide_label, unsafe_allow_html=True)




def generate_oms(user_id, project_name):
    load_dotenv()
    APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
    INPUT_DOCUMENT_SUB_DIRECTORY = os.getenv("INPUT_DOCUMENT_SUB_DIRECTORY")

    user_id = st.session_state.user_id
    user_home = os.path.join(APP_DATA_HOME, user_id)

    app_input_document_location = os.path.join(user_home, project_name, INPUT_DOCUMENT_SUB_DIRECTORY)
    app_spec_file_target_location = os.path.join(user_home, project_name, SPEC_SUB_DIRECTORY)
    seagent_specs.create_webapp_page_specifications(app_input_document_location, app_spec_file_target_location)

def upload_ui(user_id):
    project_name, project_home_path = req_project.create_project_name(st.session_state.user_id)
    uploaded = False
    uploaded_files = st.file_uploader("选择上传文档：", accept_multiple_files=True, label_visibility="collapsed")
    if uploaded_files and len(project_name) > 0:
        # adjusted_project_name = req_project.create_project_name(user_id, project_identifier, project_name)
        # adjusted_project_name = project_name
        # print(adjusted_project_name)
        st.session_state.project_name = project_name
        req_project.upload_documents(uploaded_files, user_id, project_name=project_name)
        uploaded = True
        
    return uploaded