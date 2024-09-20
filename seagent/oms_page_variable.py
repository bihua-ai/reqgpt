import streamlit as st
import json
import oms_library_project, oms_library_specification, seagent_file, oms_component_attributes_table, oms_component_state_table


def open():
    return_node = st.session_state.app_state["navtree_return_element"]

    if return_node["reason"] == "view":
        st.session_state.app_state["current_navtree_return_element"] = st.session_state.app_state["navtree_return_element"]
    else:
         current_node = st.session_state.app_state["current_navtree_return_element"]
         if return_node["node_oms_identifier"] != current_node["node_oms_identifier"]:
              return_node = current_node

    # if return_node["node_type"] == "action" or return_node["node_type"] == "variable":
    #             st.session_state.app_state["current_navtree_return_element"] = st.session_state.app_state["navtree_return_element"]

    # if return_node["node_type"] != "variable":
    #     return_node = st.session_state.app_state["current_navtree_return_element"]

    variable_name = return_node["node_new_name"]
    variable_identifier = return_node["node_oms_identifier"]
    user_id = st.session_state.app_state["user_identifier"]
    project_name = return_node["project_name"]

    if st.session_state.app_state["navtree_return_element"]["node_type"] == "project":
        path = oms_library_project.is_owner_project_name_variable_identifier(variable_identifier, user_id, st.session_state.app_state["navtree_return_element"]["node_new_name"])
        if path != None: # action's parent
            st.session_state.app_state["current_navtree_return_element"]["project_name"] = st.session_state.app_state["navtree_return_element"]["node_new_name"]
            project_name = st.session_state.app_state["navtree_return_element"]["node_new_name"]

    # st.title(f"变量: {variable_name}")
    if st.session_state.app_state["AI"] is not None:
        with st.container(height=150):
            prompt = st.chat_input("Say something", key="chat_reqgpt")
            if prompt:
                st.write(f"User has sent the following prompt: {prompt}")

    spec_json_path = oms_library_project.get_spec_file_path_from_variable_identifier(variable_identifier, user_id, project_name)
    st.session_state.app_state["path_spec_with_action"] = spec_json_path
    spec_json = seagent_file.oms_load(spec_json_path)

    st.markdown("## 属性表")
    # st.title("属性表") 
    spec_json_string = json.dumps(spec_json)
    with st.empty():
        return_attibute_element = oms_component_attributes_table.st_attributes_component(
            variable_identifier, spec_json_string, key=f"attributes_table_{variable_identifier}")
        
        if return_attibute_element is not None:
            oms_library_specification.attributes_table_crud(return_attibute_element, variable_identifier, spec_json)

    st.markdown("## 状态表")
    # st.title("状态表")
    with st.empty():
        return_states_element = oms_component_state_table.st_states_component(
            variable_identifier, spec_json_string, key=f"states_table_{variable_identifier}")
        print("状态表")
        print(return_states_element)
        if return_states_element is not None:
            oms_library_specification.states_table_crud(return_states_element, variable_identifier, spec_json) 




# def diaplay_variable_page(name, variable_identifier, spec_json):

#     # if 'rerun_needed' not in st.session_state:
#     #     st.session_state.rerun_needed = False
    
#     if 'last_attributes_element' not in st.session_state:
#         st.session_state.last_attributes_element = None
#     if 'last_states_element' not in st.session_state:
#         st.session_state.last_states_element = None
    
#     st.title("属性表") # 6cc14ab9c86b4f4898467833f25f5af6
#     spec_json_string = json.dumps(spec_json)
#     with st.empty():
#         return_attibute_element = req_attributes_table_component.st_attributes_component(
#             variable_identifier, spec_json_string, key=f"attributes_table_{variable_identifier}")
        
#         if (return_attibute_element is not None) and (return_attibute_element != st.session_state.last_attributes_element):
#             attributes_table_crud(return_attibute_element, variable_identifier, spec_json)
#             st.session_state.last_attributes_element = return_attibute_element
#             st.session_state.rerun_needed = True

#     st.title("状态表")
#     with st.empty():
#         return_states_element = req_states_table_component.st_states_component(
#             variable_identifier, spec_json_string, key=f"states_table_{variable_identifier}")
#         print("状态表")
#         print(return_states_element)
#         if (return_states_element is not None) and (return_states_element != st.session_state.last_states_element):
#             st.session_state.last_states_element = return_states_element
#             st.session_state.rerun_needed = True
            
#             states_table_crud(return_states_element, variable_identifier, spec_json)    
