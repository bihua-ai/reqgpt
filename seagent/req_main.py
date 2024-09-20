import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    /* Change the default font size for the entire page */
    html, body, [class*="css"]  {
        font-size: 18px;  /* Adjust this value to change the global font size */
    }
    </style>
    """, unsafe_allow_html=True)

import req_project, req_navigation_component, req_upload_component, req_testset_generation, req_testset_library
import streamlit.components.v1 as components
import json, __st_states
import req_object_presentation
import seagent.req_testset_generation as req_testset_generation
import string, os, base64
from datetime import datetime
from io import BytesIO

# reqgpt_logo_path = "/opt/bihua/reqgpt/seagent/reqgpt_logo.png"
# st.sidebar.page_link('req_main.py', label='首页')
# st.sidebar.page_link('pages/req_upload.py', label='上传文档')
# st.sidebar.page_link('pages/req_document_generation.py', label='生成测试用例')

if 'user_id' not in st.session_state:
    st.session_state.user_id = None

if 'project_name' not in st.session_state:
    st.session_state.project_name = None

if 'project_path' not in st.session_state:
    st.session_state.project_path = None

if 'path_spec_with_action' not in st.session_state:
    st.session_state.path_spec_with_action = None
if 'action_identifier' not in st.session_state:
    st.session_state.action_identifier = None
if 'action_name' not in st.session_state:
    st.session_state.action_name = None

if 'checked_actions' not in st.session_state:
    st.session_state.checked_actions = []
if 'checked_cars' not in st.session_state:
    st.session_state.checked_cars = []
if 'checked_variables' not in st.session_state:
    st.session_state.checked_variables = []
if 'checked_attributes' not in st.session_state:
    st.session_state.checked_attributes = []
if 'checked_states' not in st.session_state:
    st.session_state.checked_states = []


if 'page' not in st.session_state:
    st.session_state.page = "home page"

if st.session_state.page == "project page":
    pass

if st.session_state.page == "specification page":
    pass

if st.session_state.page == "action page":
    
    req_object_presentation.object_page(st.session_state.action_identifier, st.session_state.path_spec_with_action)

if st.session_state.page == "variable page":
    pass

if st.session_state.page == "testset page":
    project_path = req_project.get_project_path(st.session_state.user_id, st.session_state.project_name)
    req_testset_generation.testset_page(project_path, st.session_state.user_id)

if st.session_state.page == "home page":

    st.title("ReqGPT，AI测试用例生成工具：全覆盖！")
    st.write("")
    st.markdown(f'<h3 style="font-size:20px;">上传文档（源代码或文档），一键生成全覆盖测试用例！</h3>', unsafe_allow_html=True)

    # user_id = st.text_input("输入user key: ", key="user_key_input")

    # # after clicking button, jump to upload page
    # if st.button("点击此按钮，使用此user key"):
    #     st.session_state.user_id = user_id
    #     __st_states.set_app_state(user_id) 
    #     st.markdown(f'<h2 style="font-size:28px;">用户user key已经收到。下一步打开上传文档，上传需求或代码。</h2>', unsafe_allow_html=True)
    #     # req_upload.upload_ui(user_id)

    # after login: we see this
    user_id = "eric"
    st.session_state.user_id = user_id
    __st_states.set_app_state(user_id) 

    with st.sidebar:
        st.sidebar.title("导航")
        if st.session_state.user_id:
            project_tree = req_project.build_project_tree_json(st.session_state.user_id)

            json_string = json.dumps(project_tree)
            return_node = req_navigation_component.st_navigation_component(tree_json=json_string, key="navigation_tree")
            
            if return_node is not None:
                if return_node["node_type"] == "project":
                    st.session_state.project_name = return_node["name"]
                    st.session_state.page = "testset page"
                elif return_node["node_type"] == "action":
                    st.session_state.action_name = return_node["name"]
                    st.session_state.action_identifier = return_node["id"]
                    spec_path = req_project.get_spec_file_path_from_action_identifier(
                        st.session_state.action_identifier, 
                        st.session_state.user_id, 
                        st.session_state.project_name)
                    
                    st.session_state.path_spec_with_action = spec_path
                    st.session_state.page = "object page"
                    # print("reached here")
                else:
                    print(return_node["node_type"])

    with st.container(height=400):
        uploaded = req_upload_component.upload_ui(st.session_state.user_id)

        if st.button("一键生成全覆盖测试用例(Excel文档)"):
            if not uploaded:
                st.write(f"请先上传文档！")
            else:
                st.write(st.session_state.project_name)

                req_upload_component.generate_oms(st.session_state.user_id, st.session_state.project_name)
                req_testset_generation.generate_full_coverage_testset(st.session_state.user_id, st.session_state.project_name)
                current_datetime = datetime.now()
                formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                file_name = "测试集" + formatted_datetime
                testcase_scope = []
                testset_xlsx_data = req_testset_library.generate_testset(project_path, user_id, testcase_scope)

                buffer = BytesIO()
                testset_xlsx_data.save(buffer)
                buffer.seek(0)  # Move the cursor to the beginning of the buffer
                xlsx_data = buffer.getvalue()
                b64 = base64.b64encode(xlsx_data).decode()  # Encode bytes to base64
                download_link = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{file_name}">{file_name}</a>'
                # st.markdown(f'<a href="{download_link}" download="sample_data.xlsx" id="download_link">Hidden Download</a>', unsafe_allow_html=True)
                st.markdown("## 测试集")
                st.markdown("---")  # Horizontal line
                st.markdown(download_link, unsafe_allow_html=True)

    st.markdown(f'<h3 style="font-size:20px;">高级操作可以从左边导航树开始。</h3>', unsafe_allow_html=True)




        # project_name, project_home_path = req_project.create_project_name(st.session_state.user_id)
        # uploaded_files = st.file_uploader("选择上传文档：", accept_multiple_files=True)
        # if uploaded_files and len(project_name) > 0:
        #     st.session_state.project_name = project_name
        #     # if project_name sub folder is not created, the upload_documents() will create it
        #     req_project.upload_documents(uploaded_files, user_id, project_name=project_name)
        #     st.write(f"File uploaded to {project_name}")
        # if st.button("一键生成Excel格式的全覆盖测试用例"):
        #     st.write("test")





