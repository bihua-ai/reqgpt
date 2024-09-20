import streamlit as st
import streamlit.components.v1 as components
import seagent_file, req_action_table_component, req_project, req_navigation_component
import re, json


# st.sidebar.page_link('req_main.py', label='首页')
# st.sidebar.page_link('pages/req_upload.py', label='上传文档')
# st.sidebar.page_link('pages/req_document_generation.py', label='生成文档')

with st.sidebar:
    st.sidebar.title("导航")
    if st.session_state.user_id:
        project_tree = req_project.build_project_tree_json(st.session_state.user_id)
        json_string = json.dumps(project_tree)
        return_action = req_navigation_component.st_navigation_component(tree_json=json_string)
        if return_action is not None:
             print(f"return_action = {return_action}")

             space_index = return_action.find(' ')
             action_identifier = return_action[:space_index]
             action_name = return_action[space_index + 1:]
             st.session_state.action_identifier = action_identifier
             st.session_state.action_name = action_name

def get_action_variable_list(action_description):
    # Define the regular expression pattern for hexadecimal identifiers
    pattern = r'identifier:\s*([0-9a-zA-Z]+)'
    
    # Find all matches in the text
    matches = re.findall(pattern, action_description)
    
    return matches

def create_action_page(spec_json, action_identifier):
    st.title("展示操作")
    action_name = None
    action_description = None
    for i in range(len(spec_json["omsObject"]["actions"])):
        if action_identifier == spec_json["omsObject"]["actions"][i]["identifier"]:
            action_name = spec_json["omsObject"]["actions"][i]["name"]
            action_description = spec_json["omsObject"]["actions"][i]["description"]
            break
    if action_name is None:
        print("no action name found in create_action_page")
        return None
    
    action_title = f"Action Name: {action_name}"
    action_title_html = f"<h1>{action_title}</h1>"
    attributes_title_html = "<h2>CAR Table</h2>"

    req_action_table_component.st_action_component(action_identifier=action_identifier, )

spec_json_path = "/opt/bihua/reqgpt/data/apps/output/app_安全文件上传与登录验证系统_2dc30f9e32b240fb9d2ca6a578f6a096.json"
spec_json = seagent_file.oms_load(spec_json_path)
action_identifier = "c8ce30fe304741a1aaabc6b4e24f1058"
create_action_page(spec_json, action_identifier)




