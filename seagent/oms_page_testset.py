import streamlit as st
import streamlit.components.v1 as components
import seagent_file, re, json, os
import  oms_library_testset
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import PatternFill, Border, Side, Font, Alignment
import seagent_file
import string, os, base64
from datetime import datetime
from dotenv import load_dotenv
from io import BytesIO
import oms_library_project

def testcase_scope_has_checked_items(testcase_scope:json):
    has_checked_items = False
    for i in range(len(testcase_scope)):
        if testcase_scope[i]["checked"] == "true":
            has_checked_items = True
    return has_checked_items


def generate_full_coverage_testset(user_id, project_name):
    load_dotenv()
    APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
    spec_json_home = os.path.join(APP_DATA_HOME, user_id, project_name, SPEC_SUB_DIRECTORY)
    testcase_scope = [] # cover all specifications in the project
    download_links = []

def testset_page(project_path: str, user_id: str):
    # st. title("Generate tes")
    load_dotenv()
    SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
    spec_json_home = os.path.join(project_path, SPEC_SUB_DIRECTORY)
    testcase_scope = [] # cover all specifications in the project
    download_links = []

    for file_entry in os.scandir(spec_json_home):
        # Check if the entry is a file. It is always a file, there is no subdirectory here.
        if file_entry.is_file():
            spec_path = os.path.join(spec_json_home, file_entry.name)
            spec_json = seagent_file.oms_load(spec_path)
            omsObject_scope = {"omsObject_name": spec_json["omsObject"]["name"], 
                               "omsObject_identifier":spec_json["omsObject"]["identifier"],
                               "checked": "false", 
                               "actions": []}
            for action in spec_json["omsObject"]["actions"]:
                action_item = {"name": action["name"], "checked": "false"}
                omsObject_scope["actions"].append(action_item)
            testcase_scope.append(omsObject_scope)
                
    # with st.sidebar:
    #     st.sidebar.title("导航")
    #     if st.session_state.user_id:
    #         project_tree = req_project.build_project_tree_json(st.session_state.user_id)

    #         json_string = json.dumps(project_tree)
    #         return_node = req_navigation_component.st_navigation_component(tree_json=json_string, key="navigation_tree")

    with st.container(height=500):
        # num_checkboxes = 10
        columns_per_row = 5
        columns = st.columns(columns_per_row)

        # Iterate through the number of checkboxes and place them in columns
        number_of_omsObjects = len(testcase_scope)
        col = None
        for i in range(number_of_omsObjects):
            col = columns[i % columns_per_row]  # Select column based on index
            label_checkbox = testcase_scope[i]["omsObject_name"]
            with col:
                if st.checkbox(label_checkbox, value=(testcase_scope[i]["checked"] == "true")):
                    testcase_scope[i]["checked"] = "true"
                else:
                    testcase_scope[i]["checked"] = "false"
                # print(testcase_scope[i]["checked"])

            # number_of_omsObjects = len(testcase_scope)
            # for i in range(number_of_omsObjects):
            #     col = columns[i % columns_per_row]  # Select column based on index
            #     label_checkbox = testcase_scope[i]["omsObject_name"]
            #     testcase_scope[i]["checked"] = "true"

              




        if st.button("产生测试用例"):
            if testcase_scope_has_checked_items(testcase_scope) == False:
                st.write("请至少选择一个被测对象。")
            else:
                st.write("正在生成测试用例。请稍候。。。")
                current_datetime = datetime.now()
                formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                file_name = "测试集" + formatted_datetime
                project_name = st.session_state.app_state["project_name"]
                user_identifier = st.session_state.app_state["user_identifier"]
                testset_xlsx_data = oms_library_testset.generate_testset(user_identifier, project_name, testcase_scope)

                buffer = BytesIO()
                testset_xlsx_data.save(buffer)
                buffer.seek(0)  # Move the cursor to the beginning of the buffer
                xlsx_data = buffer.getvalue()
                b64 = base64.b64encode(xlsx_data).decode()  # Encode bytes to base64
                download_link = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{file_name}">{file_name}</a>'
                # st.markdown(f'<a href="{download_link}" download="sample_data.xlsx" id="download_link">Hidden Download</a>', unsafe_allow_html=True)
                download_links.append(download_link)
                st.markdown("## 测试集")
                st.markdown("---")  # Horizontal line
                # for item in download_links:
                #     st.markdown(f"- [**{item['text']}**]({item['url']})")
                for link in download_links:
                    st.markdown(link, unsafe_allow_html=True)

# testset_page("/opt/bihua/reqgpt/data/apps/eric/bookstore", "eric")
def open():
    st.title("产生测试集")

    user_identifier = st.session_state.app_state["user_identifier"]
    project_name = st.session_state.app_state["project_name"]
    project_path = oms_library_project.get_project_path(user_identifier, project_name)
    testset_page(project_path, user_identifier)


def open1():
    st.title("产生测试集")
    if st.session_state.app_state["AI"] == None:
        st.write("AI测试用例生成功能以后会提供。")
        return
    user_identifier = st.session_state.app_state["user_identifier"]
    project_name = st.session_state.app_state["project_name"]
    project_path = oms_library_project.get_project_path(user_identifier, project_name)
    testset_page(project_path, user_identifier)
    

# st.sidebar.page_link('req_main.py', label='首页')
# st.sidebar.page_link('pages/req_upload.py', label='上传文档')
# st.sidebar.page_link('pages/req_document_generation.py', label='生成文档')


# def generate_testset(project_path: str, user_id: str, testcase_scope:json):

#     testset_json = req_testset_library.testset_generate
#     testset_xlsx_data = req_testset_library.testset_convert_json_to_xlsx(testset_json)
#     return testset_xlsx_data


    # print("generate_testcase")
    # load_dotenv()
    # SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
    # spec_json_home = os.path.join(project_path, SPEC_SUB_DIRECTORY)

    # # load spec to neo4j
    # req_gdb.insert_all_oms(spec_json_home, user_id)
    # # generate test case json
    # testset_json = req_testset_library.generate_testset_json(project_path, user_id, testcase_scope)
    # # testset_json = {}
    # # generate xlsx
    # st.session_state.testset_json = testset_json
    # req_testset_library.convert_json_to_xlsx(testset_json)

# 例子
# testcase_scope = [
#       {
#           "omsObject_name": "登陆页面", 
#           "omsObject_identifier": "1345",
#           "checked": "false", 
#           "actions": [
#               {
#                   "name":"登录",
#                   "checked": "false", 
#                   "identifier": "id1212341235"
#               }
#             ]
#       }
# ] 