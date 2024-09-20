import streamlit as st
import oms_component_upload

# it opens from tree's project input document node
def open():
    return_element_from_tree = st.session_state.app_state["navtree_return_element"]
    user_identifier = st.session_state.app_state["user_identifier"]
    project_name = return_element_from_tree["project_name"]
    st.title(f"上传文档到{project_name}")
    with st.container(height=400):
        user_identifier = st.session_state.app_state["user_identifier"]
        project_name = st.session_state.app_state["project_name"]
        uploaded = oms_component_upload.upload_ui(user_identifier, project_name=project_name)

