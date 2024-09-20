import streamlit.components.v1 as components
import seagent_file, re, json
import streamlit as st


# st.set_page_config(layout="wide")

_component_func  = components.declare_component(
    "st_attributes_component", 
    url="http://localhost:3003")

def st_attributes_component(variable_identifier, spec_json, key=None, default=None):
    """Create a new instance of "st_action_component"."""
    return _component_func(variable_identifier=variable_identifier, spec_json=spec_json, key=key, default=None)


##########variable attribute
# const return_attribute =  {
#         variable_identifier: this.variable_identifier,
#         attribute_identifier: null,
#         equivalence_identifier: null,
#         attribute: newAttributeRow,
#         equivalence_class: null,
#         type: "attribute",
#         reason: "created" // or "deleted" or "updated"
#       };
def process_attribute(return_attribute_wrapper, variable_identifier, spec_json):
    reason = return_attribute_wrapper["reason"]

    number_of_variables = len(spec_json["omsObject"]["memberObjects"])
    variable_index = -1
    for i in range(number_of_variables):
        if variable_identifier == spec_json["omsObject"]["memberObjects"][i]["identifier"]:
            variable_index = i
            break
    
    if reason == "updated":
        number_of_attributes = len(spec_json["omsObject"]["memberObjects"][variable_index]["attributes"])
        for i in range(number_of_attributes):
            if return_attribute_wrapper["attribute_identifier"] == spec_json["omsObject"]["memberObjects"][variable_index]["attributes"][i]["identifier"]:          
                
                spec_json["omsObject"]["memberObjects"][variable_index]["attributes"][i]= return_attribute_wrapper["element"]
                break 

    elif reason == "deleted":
        number_of_attributes = len(spec_json["omsObject"]["memberObjects"][variable_index]["attributes"])
        for i in range(number_of_attributes):
            if return_attribute_wrapper["attribute_identifier"] == spec_json["omsObject"]["memberObjects"][variable_index]["attributes"][i]["identifier"]:             
                del spec_json["omsObject"]["memberObjects"][variable_index]["attributes"][i]
                break 

    elif reason == "created":
        spec_json["omsObject"]["memberObjects"][variable_index]["attributes"].append(return_attribute_wrapper["element"])

    # print(st.session_state.path_spec_with_action)
    seagent_file.oms_save(st.session_state.path_spec_with_action, spec_json)
    # print("saved file in process attributes.")
    # st.rerun()




# spec_json_path = "/opt/bihua/reqgpt/data/apps/eric/bookstore/specifications/app_安全文件上传与登录验证系统_aa5d8c86634e4989a9f1c9c27432f5f7.json"
# spec_json = seagent_file.oms_load(spec_json_path)
# spec_json_string = json.dumps(spec_json)

# variable_identifier = "6cc14ab9c86b4f4898467833f25f5af6" 

# st.title("Test st_attributes_component")

# return_value  = st_attributes_component(variable_identifier, spec_json_string)
# print(return_value)

# if return_value:
#     return_car_wrapper = json.loads(return_value)

#     if return_car_wrapper:
#         st.write(return_car_wrapper)
#     else:
#         st.write("return_car_wrapper is empty")
