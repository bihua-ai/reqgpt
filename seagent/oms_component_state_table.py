import streamlit.components.v1 as components
import seagent_file, re, json, os
import streamlit as st

# IF True， use component buit; False, we run npm start, so we can modify code easily
_RELEASE = True # or False. Change this line manually
# _RELEASE = False # or False. Change this line manually


if not _RELEASE:
    _component_func  = components.declare_component(
        "st_states_component", 
        url="http://localhost:3004")
    
else:
# __file__ is /opt/bihua/reqgpt/seagent/
    # folder destination is /opt/bihua/reqgpt/seagent/component-template/template/st_states_component/frontend
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "component-template/template/st_states_component/frontend/build")
    _component_func = components.declare_component("st_states_component", path=build_dir)



def st_states_component(variable_identifier, spec_json, key=None, default=None):
    """Create a new instance of "st_states_component"."""
    return _component_func(variable_identifier=variable_identifier, spec_json=spec_json, key=key, default=None)


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

def process_state(return_state_wrapper, variable_identifier, spec_json):
    reason = return_state_wrapper["reason"]

    number_of_variables = len(spec_json["omsObject"]["memberObjects"])
    variable_index = -1
    for i in range(number_of_variables):
        if variable_identifier == spec_json["omsObject"]["memberObjects"][i]["identifier"]:
            variable_index = i
            break
    
    if reason == "updated": # attribute and equivalence class change will be handled here too
        number_of_attributes = len(spec_json["omsObject"]["memberObjects"][variable_index]["states"])
        for i in range(number_of_attributes):
            if return_state_wrapper["state"]["identifier"] == spec_json["omsObject"]["memberObjects"][variable_index]["states"][i]["identifier"]:          
                spec_json["omsObject"]["memberObjects"][variable_index]["states"][i]= return_state_wrapper["state"]
                break 
            
    elif reason == "deleted":
        number_of_attributes = len(spec_json["omsObject"]["memberObjects"][variable_index]["states"])
        for i in range(number_of_attributes):
            if return_state_wrapper["state_identifier"] == spec_json["omsObject"]["memberObjects"][variable_index]["states"][i]["identifier"]:             
                del spec_json["omsObject"]["memberObjects"][variable_index]["states"][i]
                break 

    elif reason == "created":
        spec_json["omsObject"]["memberObjects"][variable_index]["states"].append(return_state_wrapper["state"])

    seagent_file.oms_save(st.session_state.app_state["path_spec_with_action"], spec_json)
    print("saved in process_state")
    # st.rerun()

# spec_json_path = "/opt/bihua/reqgpt/data/apps/eric/bookstore/specifications/app_安全文件上传与登录验证系统_aa5d8c86634e4989a9f1c9c27432f5f7.json"
# spec_json = seagent_file.oms_load(spec_json_path)
# spec_json_string = json.dumps(spec_json)

# variable_identifier = "6cc14ab9c86b4f4898467833f25f5af6" 

# st.title("Test st_states_component")

# return_value  = st_states_component(variable_identifier, spec_json_string)
# print(return_value)

# # if return_value:
# #     return_car_wrapper = json.loads(return_value)

# #     if return_car_wrapper:
# #         st.write(return_car_wrapper)
# #     else:
# #         st.write("return_car_wrapper is empty")
