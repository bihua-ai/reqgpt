import json, os, seagent_file
import streamlit as st
from dotenv import load_dotenv

def get_app_state(user_id):
    load_dotenv()
    APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    use_home = os.path.join(APP_DATA_HOME, user_id)
    if os.path.exists(use_home):
        app_state = seagent_file.oms_load(use_home)
    else:
        app_state = {
            "user_id": user_id,
            "project_name": "",
            "navigation_node_selected": "",
        }
        seagent_file.oms_save(use_home, app_state)
    return app_state

def set_app_state(user_id, app_state=None):
    load_dotenv()
    APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    use_home = os.path.join(APP_DATA_HOME, user_id)
    if os.path.exists(use_home):
        if app_state is not None:
            seagent_file.oms_save(use_home, app_state)
    else:
        if app_state is None:
            app_state = {
                "user_id": user_id,
                "project_name": "",
                "navigation_node_selected": "",
            }
        seagent_file.oms_save(use_home, app_state)

# print("in __st_states")

# st.session_state.user_id = None
# st.session_state.project_name = None
# st.session_state.path_spec_with_action = None
# st.session_state.action_identifier = None
# st.session_state.action_name = None
# st.session_state.page = None

# home page, 
# object page, 
# upload page, 
# document generator page

######### action car
#  const return_car =  {
#       action_identifier: this.action_identifier,
#       car: newRow,
#       reason: "created" // or "deleted" or "updated"
#     }

##########variable attribute
# const return_attribute =  {
#         variable_identifier: this.variable_identifier,
#         attribute_identifier: null,
#         equivalence_identifier: null,
#         attribue: newAttributeRow,
#         equivalence_class: null,
#         type: "attribute",
#         reason: "created" // or "deleted" or "updated"
#       };

###########state
# interface ReturnElement {
#   varaible_identifier: string;
#   state_identifier: string;
#   attribute_identifier: string;
#   equivalence_identifier: string;
#   state: any;
#   attributeAndEquivalenceClasses: any;
#   type: "state" | "attribute" | "equivalence class";
#   reason: "created" | "deleted" | "updated";
# }

# }







