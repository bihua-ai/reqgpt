import json, os, seagent_file
import streamlit as st
from dotenv import load_dotenv

# example: st.session_state.app_state["checked_element"]["checked_actions"]

# page_visible = "home page" | "project page" | "specification generation page" | "action page" | "variable page"

# reason: "created" | "deleted" | "updated" | "all_chidren_deleted" | "generate_testset" | "upload_documents" | "generate_specifications";

def app_state_initialisation(user_id):

    st.session_state.app_state = {
        "AI": None,
        "user_identifier": user_id,
        "project_tree_data": None,
        "navtree_return_element": None,
        "navtree_key": "navigation_tree", 
        "checked_elements": {               
            "checked_projects": [],
            "checked_documents": [],
            "checked_specifications": [],
            "checked_actions": [],
            "checked_cars": [],
            "checked_conditions": [],
            "checked_results": [],
            "checked_next_cars": [],
            "checked_variables": [],
            "checked_attributes": [],
            "checked_states": [],
        },

        "project_name": None,
        "project_path": None,
        "path_spec_with_action": None,
        "action_identifier": None,
        "action_name": None,
        "page_visible": "home page",
    }

    st.session_state["tree_data"] = None
    st.session_state.app_state["current_navtree_return_element"] = None

    load_dotenv()
    APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    user_home_path = os.path.join(APP_DATA_HOME, user_id)
    if not os.path.exists(user_home_path):
        os.mkdir(user_home_path)

    

def app_state_load(user_id):
    load_dotenv()
    APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    APP_STATE_FILE_NAME = os.getenv("APP_STATE_FILE_NAME")
    user_config_file_path = os.path.join(APP_DATA_HOME, user_id, APP_STATE_FILE_NAME)
    if os.path.exists(user_config_file_path):
        st.session_state.app_state = seagent_file.oms_load(user_config_file_path)
    else:
        # use the current state, save it for later
        seagent_file.oms_save(user_config_file_path, st.session_state.app_state)
    

def app_state_save(user_id, app_state=None):
    load_dotenv()
    APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    APP_STATE_FILE_NAME = os.getenv("APP_STATE_FILE_NAME")
    user_config_file_path = os.path.join(APP_DATA_HOME, user_id, APP_STATE_FILE_NAME)
    seagent_file.oms_save(user_config_file_path, app_state)


# Tree
# interface NodeOperationResult {
#   node_type: "user" | "project" | "documents" | "specifications" | "document" | "page" | "action" | "variable";
#   reason: "created" | "deleted" | "updated" | "view" | "checked" | "all_chidren_deleted" | "generate cars" | "generate states" | "generate_testset" | "upload_documents" | "generate_specifications";
#   project_name: string | null;
#   node_old_name: string | null;
#   node_new_name: string | null;
#   node_oms_identifier: string | null;
#   result: string;
# }

# Action
# interface ReturnElement {
#   action_identifier: string | null;
#   car_identifier: string | null;
#   element: any;
#   type: "car" | "condition" | "result" | "next_car";
#   reason: "created" | "deleted" | "updated" | "calculate_cars" | "next_car_checked" | "checked";
# }

# Attribute
# interface ReturnElement {
#   varaible_identifier: string;
#   attribute_identifier: string;
#   equivalence_identifier: string;
#   element: any;
#   type: "attribute" | "equivalence class";
#   reason: "created" | "deleted" | "updated";
# }

# State
# interface ReturnElement {
#   varaible_identifier: string;
#   state_identifier: string;
#   state: any;
#   reason: "created" | "deleted" | "updated";
# }
