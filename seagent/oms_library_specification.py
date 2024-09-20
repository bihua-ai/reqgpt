import os, json
from shutil import rmtree
import streamlit as st
from dotenv import load_dotenv
import oms_page_variable, seagent_file, seagent_specs, oms_component_action_table, oms_component_attributes_table, oms_component_state_table, seagent_pict, oms_library_project


def load_valid_json(return_data):
    try:
        data = json.loads(return_data)
        return data
    except (json.JSONDecodeError, TypeError):
        return None

def update_next_cars(spec_json, action_identifier, car_identifier, next_car_list):
    number_of_actions = len(spec_json["omsObject"]["actions"])
    for i in range(number_of_actions):
        if spec_json["omsObject"]["actions"][i]["identifier"] == action_identifier:
            number_of_cars = len(spec_json["omsObject"]["actions"][i]["cars"])
            for j in range(number_of_cars):
                if(spec_json["omsObject"]["actions"][i]["cars"][j]["identifier"] == car_identifier):
                    spec_json["omsObject"]["actions"][i]["cars"][j]["nextCar"] = next_car_list
                    # for k in range(len(next_car_list)):
                    #     if next_car_list[k] not in spec_json["omsObject"]["actions"][i]["cars"][j]["nextCar"]:
                    #         spec_json["omsObject"]["actions"][i]["cars"][j]["nextCar"].append(next_car_list[k])
                    break
            break
    seagent_file.oms_save(st.session_state.app_state["path_spec_with_action"], spec_json)
    st.session_state.app_state["checked_elements"]["checked_cars"] = []
    st.session_state.app_state["checked_elements"]["checked_next_cars"] = []
    

def cars_table_crud(return_car_element, action_identifier, spec_json):
    if return_car_element is None:
        return

    return_car_wrapper = load_valid_json(return_car_element)
    if return_car_wrapper:
        oms_component_action_table.process_car(return_car_wrapper, action_identifier, spec_json)

def attributes_table_crud(return_attibute_element, variable_identifier, spec_json):
    if return_attibute_element is None:
        return

    return_attribute_wrapper = load_valid_json(return_attibute_element)
    if return_attribute_wrapper:
        oms_component_attributes_table.process_attribute(return_attribute_wrapper, variable_identifier, spec_json)

def states_table_crud(return_states_element, variable_identifier, spec_json):
    if return_states_element is None:
        return

    return_state_wrapper = load_valid_json(return_states_element)
    if return_state_wrapper:
        oms_component_state_table.process_state(return_state_wrapper, variable_identifier, spec_json)

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
    


    #############For now, we just cinclude all variables under action. Later we add checked variables
    # const return_element: NodeOperationResult = {
    #   node_type: current_node.data.node_type,
    #   reason: "generate cars",
    #   node_old_name: null,
    #   node_new_name: null,
    #   project_name: project_name,
    #   node_oms_identifier: current_node.data["id"],
    #   result: "success"
    # };

def get_variable_list_for_action_car(spec_json, action_identifier):
    number_of_actions = len(spec_json["omsObject"]["actions"])
    for i in range(number_of_actions):
        if spec_json["omsObject"]["actions"][i]["identifier"] == action_identifier:
            return spec_json["omsObject"]["actions"][i]["variables"]
    return None

def generate_action_cars():
    user_id = st.session_state.app_state["user_identifier"]
    navtree_return_element = st.session_state.app_state["navtree_return_element"]
    # we generate cars at action element node on the tree
    action_identifier = navtree_return_element["node_oms_identifier"] 
    project_name = navtree_return_element["project_name"] 
    st.session_state.app_state["path_spec_with_action"] = oms_library_project.get_spec_file_path_from_action_identifier(action_identifier, user_id, project_name)

    spec_json_path = st.session_state.app_state["path_spec_with_action"]  
    spec_json = seagent_file.oms_load(spec_json_path)
    # variable_list = st.session_state.app_state["checked_elements"]["checked_variables"]
    variable_list = get_variable_list_for_action_car(spec_json, action_identifier)
    
    # this line will update spec_json and the updated is saved to spec json file.
    page_spec_json = seagent_pict.oms_calculate_car_without_ai_for_one_action(spec_json, action_identifier, variable_list)
    seagent_file.oms_save(spec_json_path, page_spec_json)
    st.session_state.app_state["page_visible"] = "information page"



# it will not delet existing state data, just append computed states and append to state table.
# const return_element: NodeOperationResult = {
#     node_type: current_node.data.node_type,
#     reason: "generate states",
#     node_old_name: null,
#     node_new_name: null,
#     project_name: project_name,
#     node_oms_identifier: current_node.data["id"],
#     result: "success"
# };

# this is called at variable node
def generate_variable_states():
    user_id = st.session_state.app_state["user_identifier"]
    navtree_return_element = st.session_state.app_state["navtree_return_element"]
    project_name = navtree_return_element["project_name"] 
    variable_identifier = navtree_return_element["node_oms_identifier"] 
    spec_json_path = oms_library_project.get_spec_file_path_from_variable_identifier(variable_identifier, user_id, project_name)
    # spec_json_path = st.session_state.app_state["path_spec_with_action"]  
    spec_json = seagent_file.oms_load(spec_json_path)

    page_spec_json = seagent_pict.calculate_states_without_ai_for_one_variable(spec_json, variable_identifier)
    seagent_file.oms_save(spec_json_path, page_spec_json)

    return variable_identifier, project_name

# this is called at project node
def generate_oms(user_id, project_name):
    load_dotenv()
    APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
    INPUT_DOCUMENT_SUB_DIRECTORY = os.getenv("INPUT_DOCUMENT_SUB_DIRECTORY")

    # user_id = st.session_state.user_id
    user_home = os.path.join(APP_DATA_HOME, user_id)

    app_input_document_location = os.path.join(user_home, project_name, INPUT_DOCUMENT_SUB_DIRECTORY)
    app_spec_file_target_location = os.path.join(user_home, project_name, SPEC_SUB_DIRECTORY)

    ##### WARNING: change later: existing specs will be cleared first#########
    if os.path.exists(app_spec_file_target_location):
            # Remove the contents of the document directory
            for item in os.listdir(app_spec_file_target_location):
                item_path = os.path.join(app_spec_file_target_location, item)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)  # Remove files and links
                elif os.path.isdir(item_path):
                    rmtree(item_path)
    seagent_specs.create_webapp_page_specifications(app_input_document_location, app_spec_file_target_location)
    print("Done!")