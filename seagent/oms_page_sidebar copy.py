import streamlit as st
import oms_component_navigation, oms_library_project, oms_page_project, oms_page_home, oms_page_action, oms_page_variable, oms_page_testset, oms_page_specification_generation, oms_library_specification, oms_page_upload
import json

# const return_element = {
#       node_type: "action",
#       reason: "all_chidren_deleted",
#       node_oms_identifier: current_node.data["id"],
#       element: {
#         node_old_name: null,
#         node_new_name: null
#       }
#     };

# reason: "created" | "deleted" | "updated" | "all_chidren_deleted" | "generate_testset" | "upload_documents" | "generate_specifications"; 

def set_open_page():
    # if st.session_state.app_state["page_visible"] == "do not change page":
    #     return

    return_node = st.session_state.app_state["navtree_return_element"]

    if return_node["node_type"] == "user":
        st.session_state.app_state["page_visible"] = "home page"
        # oms_page_home.open()

    elif return_node["node_type"] == "project":
        if return_node["reason"] == "generate_testset":
            st.session_state.app_state["page_visible"] = "testset page"
        else:
            st.session_state.app_state["page_visible"] = "project page"
            # oms_page_project.open()

    elif return_node["node_type"] == "specifications":
        st.session_state.app_state["page_visible"] = "specification generation page"

    elif return_node["node_type"] == "action":
        st.session_state.app_state["page_visible"] = "action page"
        # oms_page_specification_generation.open()

    elif return_node["node_type"] == "variable":
        st.session_state.app_state["page_visible"] = "variable page"
        # oms_page_variable.open()

    elif return_node["node_type"] == "page":
        st.session_state.app_state["page_visible"] = "specification page"

    elif return_node["node_type"] == "specifications":
        pass
        # oms_page_specification.open()

    elif return_node["node_type"] == "documents":
        pass
    else:
        pass


def add():
    with st.sidebar:
        st.markdown(
            """
            <style>
            /* Adjust the width of the sidebar */
            .css-1d391kg {
                width: 450px;  /* Set the initial width */
            }
            .css-1d391kg .css-1lcbmhc {
                width: 300px;  /* Set the content width */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        image_path = "/opt/bihua/reqgpt/seagent/bihua.png"  # Replace with your image path
        st.image(image_path, width=400)

        # print(st.session_state.app_state["user_identifier"])
        project_tree = oms_library_project.build_project_tree_json(st.session_state.app_state["user_identifier"])
        json_string = json.dumps(project_tree)

        # project_tree = []
        # if "tree_data" not in st.session_state:
        #     project_tree = oms_library_project.build_project_tree_json(st.session_state.app_state["user_identifier"])
        #     st.session_state["tree_data"] = project_tree
        # else:
        #     project_tree = st.session_state["tree_data"]
        # json_string = json.dumps(project_tree)

    #    const return_element: NodeOperationResult = {
    #   node_type: current_node.data["node_type"],
    #   reason: "generate_testset",
    #   node_oms_identifier: current_node.data["id"],
    #   node_old_name: null,
    #   node_new_name: null,
    #   project_name: project_name,
    #   result: "success"
    # };
        user_key = st.session_state.app_state["user_identifier"]
        return_node_raw = oms_component_navigation.st_navigation_component(tree_json=json_string, key=user_key)

        st.session_state.app_state["project_tree_data"] = json_string
        if return_node_raw is not None:            
            return_node = json.loads(return_node_raw)
            st.session_state.app_state["navtree_return_element"] = return_node
            st.session_state.app_state["project_name"] = return_node["project_name"]

            if return_node["reason"] == "created":
                # update project data, do not change main area display page
                oms_library_project.create()

            elif return_node["reason"] == "updated":
                # update project data, do not change main area display page
                oms_library_project.rename()
            
            elif return_node["reason"] == "deleted":
                # update project data, do not change main area display page
                oms_library_project.delete()

            elif return_node["reason"] == "checked":
                # update project data, do not change main area display page
                oms_library_project.check()

            elif return_node["reason"] == "view": # double click at tree node
                # if st.session_state.app_state["page_visible"] == "do not change page":
                #     st.session_state.app_state["page_visible"] = "change page"
                # else:
                set_open_page()

            elif return_node["reason"] == "all_chidren_deleted":
                # update project data, do not change main area display page
                oms_library_project.delete_all()

            elif return_node["reason"] == "generate states":
                oms_library_specification.generate_variable_states()
                
            elif return_node["reason"] == "generate cars":
                oms_library_specification.generate_action_cars()

            elif return_node["reason"] == "generate_specifications":
                st.session_state.app_state["page_visible"] = "specification generation page"
                # oms_page_specification_generation.open()
            
            elif return_node["reason"] == "generate_testset":
                st.session_state.app_state["page_visible"] = "testset page"
                # # oms_page_testset.open()


            elif return_node["reason"] == "upload_documents": # triggered at input documents node
                st.session_state.app_state["page_visible"] = "upload page"
            else:
                print("default is reached.")

            



        # if return_node is not None:
        #     if return_node["reason"] == "created":
        #         oms_library_project.create()
        #     elif return_node["reason"] == "updated":
        #         oms_library_project.rename()
        #     elif return_node["reason"] == "deleted":
        #         oms_library_project.delete()
        #     elif return_node["reason"] == "all_chidren_deleted":
        #         oms_library_project.delete_all()


        #     elif return_node["reason"] == "generate_testset":
        #         oms_page_testset.open()
        #     elif return_node["reason"] == "upload_documents":
        #         oms_page_upload.open()
        #     elif return_node["reason"] == "generate_specifications":
        #         pass
        #     else:
        #         pass


        # which page to open
        # update project or spec
        


        
        # if return_node is not None:
        #     if return_node["node_type"] == "project":
        #         st.session_state.project_name = return_node["name"]
        #         st.session_state.page = "testset page"
        #     elif return_node["node_type"] == "action":
        #         st.session_state.action_name = return_node["name"]
        #         st.session_state.action_identifier = return_node["id"]
        #         spec_path = req_project.get_spec_file_path_from_action_identifier(
        #             st.session_state.action_identifier, 
        #             st.session_state.user_id, 
        #             st.session_state.project_name)
                
        #         st.session_state.path_spec_with_action = spec_path
        #         st.session_state.page = "object page"
        #         # print("reached here")
        #     else:
        #         print(return_node["node_type"])


