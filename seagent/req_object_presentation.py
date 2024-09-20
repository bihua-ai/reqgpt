import streamlit.components.v1 as components
import seagent_file, re, json, os
import streamlit as st
import req_states_table_component, req_action_table_component
import req_attributes_table_component, req_navigation_component, req_project

if 'rerun_needed' not in st.session_state:
        st.session_state.rerun_needed = False

# st.set_page_config(layout="wide")
def load_valid_json(return_data):
    try:
        data = json.loads(return_data)
        return data
    except (json.JSONDecodeError, TypeError):
        return None

def cars_table_crud(return_car_element, action_identifier, spec_json):
    if return_car_element is None:
        return

    return_car_wrapper = load_valid_json(return_car_element)
    if return_car_wrapper:
        req_action_table_component.process_car(return_car_wrapper, action_identifier, spec_json)

def attributes_table_crud(return_attibute_element, variable_identifier, spec_json):
    if return_attibute_element is None:
        return

    return_attribute_wrapper = load_valid_json(return_attibute_element)
    if return_attribute_wrapper:
        req_attributes_table_component.process_attribute(return_attribute_wrapper, variable_identifier, spec_json)

def states_table_crud(return_states_element, variable_identifier, spec_json):
    if return_states_element is None:
        return

    return_state_wrapper = load_valid_json(return_states_element)
    if return_state_wrapper:
        req_states_table_component.process_state(return_state_wrapper, variable_identifier, spec_json)

def diaplay_variable_page(name, variable_identifier, spec_json):

    # if 'rerun_needed' not in st.session_state:
    #     st.session_state.rerun_needed = False
    
    if 'last_attributes_element' not in st.session_state:
        st.session_state.last_attributes_element = None
    if 'last_states_element' not in st.session_state:
        st.session_state.last_states_element = None
    
    st.title("属性表") # 6cc14ab9c86b4f4898467833f25f5af6
    spec_json_string = json.dumps(spec_json)
    with st.empty():
        return_attibute_element = req_attributes_table_component.st_attributes_component(
            variable_identifier, spec_json_string, key=f"attributes_table_{variable_identifier}")
        
        if (return_attibute_element is not None) and (return_attibute_element != st.session_state.last_attributes_element):
            attributes_table_crud(return_attibute_element, variable_identifier, spec_json)
            st.session_state.last_attributes_element = return_attibute_element
            st.session_state.rerun_needed = True

    st.title("状态表")
    with st.empty():
        return_states_element = req_states_table_component.st_states_component(
            variable_identifier, spec_json_string, key=f"states_table_{variable_identifier}")
        print("状态表")
        print(return_states_element)
        if (return_states_element is not None) and (return_states_element != st.session_state.last_states_element):
            st.session_state.last_states_element = return_states_element
            st.session_state.rerun_needed = True
            
            states_table_crud(return_states_element, variable_identifier, spec_json)    

    print(f"in retun....{st.session_state.rerun_needed}")
    if  st.session_state.rerun_needed == True:
        st.session_state.rerun_needed = False
        # st.rerun()
    
    # if st.session_state.attributes_changed and st.session_state.states_changed:
    #     # Reset flags after rerun
    #     st.session_state.attributes_changed = False
    #     st.session_state.states_changed = False
    #     st.rerun()

# input is one spec json file full_path
def load_all_specs_json(spec_json_full_path):
    specs_json = {"specs": []}

    spec_directory = os.path.dirname(spec_json_full_path)
    try:
        for filename in os.listdir(spec_directory):
            if filename.endswith(".json"):  # assuming the specs are in JSON format
                full_path = os.path.join(spec_directory, filename)

                # Load the spec file
                spec_content = seagent_file.oms_load(full_path)

                # Create a new spec entry
                spec = {
                    "spec_path": full_path,
                    "status": "initial_load",  # Or some other logic to determine status
                    "spec_json": spec_content
                }

                # Append the spec to the specs_json list
                specs_json["specs"].append(spec)
    except Exception as e:
        print(f"An error occurred while loading specs: {e}")
        specs_json = None
    finally:
        return specs_json


# @st.fragment()
def object_page(action_identifier, spec_json_path):

    specs_json = load_all_specs_json(spec_json_path)
    spec_json = seagent_file.oms_load(spec_json_path)


    action_name = st.session_state.action_name
    st.title(f"操作: {action_name}")

    with st.sidebar:
        st.sidebar.title("导航")
        if st.session_state.user_id:
            project_tree = req_project.build_project_tree_json(st.session_state.user_id)

            json_string = json.dumps(project_tree)
            return_node = req_navigation_component.st_navigation_component(tree_json=json_string, key="navigation_tree")
            # print(f"here = {return_node}")
            # print(return_node["node_type"])
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
                    # print("reached here in object page")
    
    with st.container(height=150):
        prompt = st.chat_input("Say something", key="chat_reqgpt")
        if prompt:
            st.write(f"User has sent the following prompt: {prompt}")

    variable_name_list = req_action_table_component.get_variable_name_list(action_identifier, spec_json)
    action_variable_name_list = [action_name] + variable_name_list
    # add selection box
    selected_name = st.selectbox("选择操作或操作的变量:", action_variable_name_list, index=0)
    if selected_name is not None:
        if selected_name != action_name:
            selected_index = action_variable_name_list.index(selected_name)
            variable_identifier_list = req_action_table_component.get_action_variable_list(action_identifier, spec_json)
            # print(action_variable_name_list)
            diaplay_variable_page(selected_name, variable_identifier_list[selected_index + 1], spec_json)
        else:
            if 'last_car_element' not in st.session_state:
                st.session_state.last_car_element = None
            variable_list_json = req_action_table_component.get_action_variable_list(action_identifier, spec_json)
            variable_list_json_string = json.dumps(variable_list_json)
            spec_json_string = json.dumps(spec_json)
            specs_json_string = json.dumps(specs_json)
            return_car_element  = req_action_table_component.st_action_component(action_identifier, variable_list_json_string, spec_json_string, specs_json_string, key="action_car_table")

            if (return_car_element is not None) and (return_car_element != st.session_state.last_car_element):
                st.session_state.last_car_element = return_car_element
                st.session_state.rerun_needed = True
                cars_table_crud(return_car_element, action_identifier, spec_json)
                if  st.session_state.rerun_needed == True:
                    st.session_state.rerun_needed = False
                    # st.rerun()

    # with st.container(height=300):
    #     # prompt = st.chat_input("Say something")
    #     # if prompt:
    #     #     st.write(f"User has sent the following prompt: {prompt}")
    #     if prompt := st.chat_input("Say something"):
    #         messages.chat_message("user").write(prompt)
    #         messages.chat_message("assistant").write(f"Echo: {prompt}")
    # messages = st.container(height=300)
    # if prompt := st.chat_input("Say something", key="chat_123"):
    #     messages.chat_message("user").write(prompt)
    #     messages.chat_message("assistant").write(f"Echo: {prompt}")





