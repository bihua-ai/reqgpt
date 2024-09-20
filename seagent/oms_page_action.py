import streamlit as st
import json, os
from dotenv import load_dotenv
import seagent_file, oms_library_project, oms_library_specification, oms_component_action_table, oms_component_navigation


#  const return_element: NodeOperationResult = {
#       node_type: node.data["node_type"],
#       reason: "view",
#       node_old_name: null,
#       node_new_name: node.data["name"],
#       project_name: project_name,
#       node_oms_identifier: node.data["id"],
#       result: "success"
#     };
st.markdown(
    """""
    <style>
    [data-testid="some_container_tag"] {
    outline: 2px solid red;
    border-radius: 2px;
}
    </style>
    """,
    unsafe_allow_html=True
)


# when user double-clicks action node on the tree
def open():
    return_node = st.session_state.app_state["navtree_return_element"]
    
    if return_node["reason"] == "view":
        st.session_state.app_state["current_navtree_return_element"] = st.session_state.app_state["navtree_return_element"]
    else:
         current_node = st.session_state.app_state["current_navtree_return_element"]
         if return_node["node_oms_identifier"] != current_node["node_oms_identifier"]:
              return_node = current_node

    action_name = return_node["node_new_name"]
    action_identifier = return_node["node_oms_identifier"]
    user_id = st.session_state.app_state["user_identifier"]
    project_name = return_node["project_name"] # if project name has not been changed

    if st.session_state.app_state["navtree_return_element"]["node_type"] == "project":
        path = oms_library_project.is_owner_project_name_action_identifier(action_identifier, user_id, st.session_state.app_state["navtree_return_element"]["node_new_name"])
        if path != None: # action's parent
            st.session_state.app_state["current_navtree_return_element"]["project_name"] = st.session_state.app_state["navtree_return_element"]["node_new_name"]
            project_name = st.session_state.app_state["navtree_return_element"]["node_new_name"]

        # load_dotenv()
        # APP_DATA_HOME = os.getenv("APP_DATA_HOME")
        # project_path = os.path.join(APP_DATA_HOME, user_id, project_name)
        # if not os.path.exists(project_path):
        #     project_name = st.session_state.app_state["navtree_return_element"]["node_new_name"]

    # st.title(f"操作场景")

    if st.session_state.app_state["AI"] is not None:
        with st.container(height=150):
            prompt = st.chat_input("Say something", key="chat_reqgpt")
            if prompt:
                st.write(f"User has sent the following prompt: {prompt}")

    spec_json_path = oms_library_project.get_spec_file_path_from_action_identifier(action_identifier, user_id, project_name)
    st.session_state.app_state["path_spec_with_action"] = spec_json_path
    specs_json = oms_library_specification.load_all_specs_json(spec_json_path)
    spec_json = seagent_file.oms_load(spec_json_path)
    variable_name_list = oms_component_action_table.get_variable_name_list_old(action_identifier, spec_json)
    variable_list_json_string = json.dumps(variable_name_list)
    spec_json_string = json.dumps(spec_json)
    specs_json_string = json.dumps(specs_json)
    checked_cars = st.session_state.app_state["checked_elements"]["checked_cars"]
    checked_cars_json_string = json.dumps(checked_cars)
    checked_next_cars = st.session_state.app_state["checked_elements"]["checked_next_cars"]
    checked_next_cars_json_string = json.dumps(checked_next_cars)
    # checked_condition_description = st.session_state.app_state["checked_elements"]["checked_next_cars"]
    # checked_result_description = st.session_state.app_state["checked_elements"]["checked_next_cars"]

    st.markdown("## 场景表")

    # type: "car" | "condition" | "result" | "next_car";
    # reason: "created" | "deleted" | "updated" | "calculate_cars" | "next_car_checked" | "checked";

    # "checked_cars": [],
    # "checked_conditions": [],
    # "checked_results": [],
    # "checked_next_cars": [],
    # car_name
    # car_next_step
    # next_car
    # car_result_description
    # car_condition_description

    return_car_element_raw  = oms_component_action_table.st_action_component(action_identifier, variable_list_json_string, spec_json_string, specs_json_string, checked_cars_json_string, checked_next_cars_json_string, key=f"action_car_table_{action_identifier}")
    
    if return_car_element_raw is not None:
        return_car_element = json.loads(return_car_element_raw)
        if return_car_element["reason"] == "create_delete_next_cars":
            print("create_delete_next_cars")
            # st.session_state.app_state["page_visible"] = "do not change page"
            # oms_library_specification.update_next_cars(spec_json, return_car_element["action_identifier"], return_car_element["car_identifier"], st.session_state.app_state["checked_elements"]["checked_cars"])
            oms_library_specification.update_next_cars(spec_json, return_car_element["action_identifier"], return_car_element["car_identifier"], return_car_element["element"])
        elif return_car_element["reason"] == "updated" or return_car_element["reason"] == "created" or return_car_element["reason"] == "deleted" or return_car_element["reason"] == "calculate_car":
            print("updated")
            # st.session_state.app_state["page_visible"] = "do not change page"
            oms_library_specification.cars_table_crud(return_car_element_raw, action_identifier, spec_json)
        elif return_car_element["reason"] == "checked":
            if return_car_element["type"] == "car_name":
                st.session_state.app_state["checked_elements"]["checked_cars"] = return_car_element["element"]
                # st.session_state.app_state["page_visible"] = "do not change page"

            elif return_car_element["type"] == "car_condition_description":
                st.session_state.app_state["checked_elements"]["checked_conditions"] = return_car_element["element"]
                # st.session_state.app_state["page_visible"] = "do not change page"

            elif return_car_element["type"] == "car_result_description":
                st.session_state.app_state["checked_elements"]["checked_results"] = return_car_element["element"]
                # st.session_state.app_state["page_visible"] = "do not change page"

            elif return_car_element["type"] == "next_car":
                st.session_state.app_state["checked_elements"]["checked_next_cars"] = return_car_element["element"]
                # st.session_state.app_state["page_visible"] = "do not change page"

            elif return_car_element["type"] == "car_next_step":
                print("car_next_step")
                # st.session_state.app_state["page_visible"] = "do not change page"

        elif return_car_element["reason"] == "calculate_car":
            print("calculate_car")

    

    