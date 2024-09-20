import streamlit.components.v1 as components
import seagent_file, re, json, os
import streamlit as st

# IF True， use component buit; False, we run npm start, so we can modify code easily
_RELEASE = True # or False. Change this line manually
# _RELEASE = False # or False. Change this line manually


######### will be relocated ###############
# Declare the component:
# parent_dir = os.path.dirname(os.path.abspath(__file__))
# build_dir = os.path.join(parent_dir, "frontend/build")
# build_dir = "/opt/bihua/reqgpt/seagent/component-template/template/my_component/frontend/build"
# # print(parent_dir)
# _component_func  = components.declare_component(
#     "my_component", 
#     path=build_dir)

if not _RELEASE:
    _component_func  = components.declare_component(
        "st_action_component", 
        url="http://localhost:3002")
    
else:
    # __file__ is /opt/bihua/reqgpt/seagent/
    # folder destination is /opt/bihua/reqgpt/seagent/component-template/template/st_action_component/frontend
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "component-template/template/st_action_component/frontend/build")
    _component_func = components.declare_component("st_action_component", path=build_dir)


def st_action_component(action_identifier, variable_list_json, spec_json, specs_json, checked_cars_json, checked_next_cars_json, key=None, default=None):
    """Create a new instance of "st_action_component"."""
    return _component_func(action_identifier=action_identifier, variable_list_json=variable_list_json, spec_json=spec_json, specs_json=specs_json, checked_cars_json=checked_cars_json, checked_next_cars_json=checked_next_cars_json, key=key, default=None)

# get the variables for the action. we will use the variables to dispkay urls and to access attributes and states
def get_action_variable_list(action_identifier, spec_json):
    # Define the regular expression pattern for hexadecimal identifiers
    for i in range(len(spec_json["omsObject"]["actions"])):
        if action_identifier == spec_json["omsObject"]["actions"][i]["identifier"]:
            action_description = spec_json["omsObject"]["actions"][i]["description"]
            break

    pattern = r'identifier:\s*([0-9a-zA-Z]+)'
    
    # Find all matches in the text
    matches = re.findall(pattern, action_description)
    return matches

def get_variable_name_list(action_identifier, spec_json):
    variable_name_list = []
    variable_identifier_list = []
    number_of_actions = len(spec_json["omsObject"]["actions"])
    for i in range(number_of_actions):
        if spec_json["omsObject"]["actions"][i]["identifier"] == action_identifier:
            variable_identifier_list = spec_json["omsObject"]["actions"][i]["variables"]
            for i in range(len(variable_identifier_list)):
                for j in range(len(spec_json["omsObject"]["memberObjects"])):
                    if variable_identifier_list[i] == spec_json["omsObject"]["memberObjects"][j]["identifier"]:
                        variable_name_list.append(spec_json["omsObject"]["memberObjects"][j]["name"])
                        break
    return variable_name_list
            


def get_variable_name_list_old(action_identifier, spec_json):
    variable_name_list = []
    variable_identifier_list = get_action_variable_list(action_identifier, spec_json)
    for i in range(len(variable_identifier_list)):
        for j in range(len(spec_json["omsObject"]["memberObjects"])):
            if variable_identifier_list[i] == spec_json["omsObject"]["memberObjects"][j]["identifier"]:
                variable_name_list.append(spec_json["omsObject"]["memberObjects"][j]["name"])
                break
    return variable_name_list

# update spec_json based on UI operation
def process_car(car_wraper, action_identifier, spec_json):
    reason = car_wraper["reason"]

    number_of_actions = len(spec_json["omsObject"]["actions"])
    for i in range(number_of_actions):
        if spec_json["omsObject"]["actions"][i]["identifier"] == action_identifier:
            break
    number_of_cars = len(spec_json["omsObject"]["actions"][i]["cars"])
    if reason == "updated":
        for j in range(number_of_cars):
            if spec_json["omsObject"]["actions"][i]["cars"][j]["identifier"] == car_wraper["element"]["identifier"]:
                spec_json["omsObject"]["actions"][i]["cars"][j] = car_wraper["element"]
                break

    elif reason == "deleted":
        for j in range(number_of_cars):
            if spec_json["omsObject"]["actions"][i]["cars"][j]["identifier"] == car_wraper["car_identifier"]:
                del spec_json["omsObject"]["actions"][i]["cars"][j]
                break
    elif reason == "created":
        spec_json["omsObject"]["actions"][i]["cars"].append(car_wraper["element"])

    try:
        print(st.session_state.app_state["path_spec_with_action"])
        seagent_file.oms_save(st.session_state.app_state["path_spec_with_action"], spec_json)
        print("saved in process_car")
    except Exception as e:
        print(e)
    
    # st.rerun()

##############

# spec_json_path = "/opt/bihua/reqgpt/data/apps/output/app_安全文件上传与登录验证系统_2dc30f9e32b240fb9d2ca6a578f6a096.json"
# spec_json = seagent_file.oms_load(spec_json_path)
# spec_json_string = json.dumps(spec_json)

# action_identifier = "c8ce30fe304741a1aaabc6b4e24f1058"
# action_description = ""
# for i in range(len(spec_json["omsObject"]["actions"])):
#     if action_identifier == spec_json["omsObject"]["actions"][i]["identifier"]:
#         action_name = spec_json["omsObject"]["actions"][i]["name"]
#         action_description = spec_json["omsObject"]["actions"][i]["description"]
#         break


# # action page content below

# st.title(f"Action: {action_name}")
# # action_title = st.text_input("action name:", key="action_name", value=action_name, label_visibility=False)
# # print(action_description)

# variable_name_list = get_variable_name_list(action_identifier, spec_json)
# for i in range(len(variable_name_list)):
#     name = variable_name_list[i]
    

# # name = "abc"
# # st.markdown('[用户名](?page=page1)') 
# # st.markdown(f'[{name}](?page=page2)')

# # variable_list_json = [identifier, identifier, ......]
# variable_list_json = get_action_variable_list(action_identifier, spec_json)

# variable_list_json_string = json.dumps(variable_list_json)

# # st.write(variable_list_json)
# st.write('')

# # st.write(spec_json)
# return_value  = st_action_component(action_identifier, variable_list_json_string, spec_json_string)
# print(f"Test data = {return_value}")

# return_car_wrapper = None
# if return_value is not None and return_value != "test setComponentValue":
#     return_car_wrapper = json.loads(return_value)
#     process_car(return_car_wrapper, action_identifier, spec_json)


# st.write(return_value)


