import streamlit as st
st.set_page_config(

    page_title="笔画",
    page_icon="/opt/bihua/reqgpt/seagent/logo.png",
    layout="wide",  # Optional: Set the layout to wide
    initial_sidebar_state="expanded"  # Optional: Set the initial state of the sidebar
)

import json, os
import oms_library_specification, oms_library_project, oms_component_navigation, oms_page_sidebar, oms_page_home, oms_config, oms_page_project, oms_page_specification_generation, oms_page_action, oms_page_variable, oms_page_testset, oms_page_upload

######################################################
# configuration
######################################################

st.markdown("""
    <style>
    /* Change the default font size for the entire page */
    html, body, [class*="css"]  {
        font-size: 18px;  /* Adjust this value to change the global font size */
    }
    </style>
    """, unsafe_allow_html=True)

######################################################
# assemble pages
######################################################
user_id = "eric"
if "app_state_initialisation" not in st.session_state:
    oms_config.app_state_initialisation(user_id)
    st.session_state["app_state_initialisation"] = True

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

        elif return_node["reason"] == "all_chidren_deleted":
            # update project data, do not change main area display page
            oms_library_project.delete_all()

        elif return_node["reason"] == "generate states":
            oms_library_specification.generate_variable_states()
            
        elif return_node["reason"] == "generate cars":
            oms_library_specification.generate_action_cars()

        else:
            print("all calculation handling is done.")

        # elif return_node["reason"] == "generate_specifications":
        #     st.session_state.app_state["page_visible"] = "specification generation page"
        #     # oms_page_specification_generation.open()
        
        # elif return_node["reason"] == "generate_testset":
        #     st.session_state.app_state["page_visible"] = "testset page"
        #     # # oms_page_testset.open()


        # elif return_node["reason"] == "upload_documents": # triggered at input documents node
        #     st.session_state.app_state["page_visible"] = "upload page"
        # elif return_node["reason"] == "view": # double click at tree node

            
        #     # if st.session_state.app_state["page_visible"] == "do not change page":
        #     #     st.session_state.app_state["page_visible"] = "change page"
        #     # else:
        #     set_open_page()
        

# main area below
return_node = st.session_state.app_state["navtree_return_element"]
print(return_node)
if return_node is not None:
    print(return_node)
    if return_node["reason"] == "generate_specifications":
        print("generate_specifications")
        oms_page_specification_generation.open()

    elif return_node["reason"] == "generate_testset":
        print("generate_testset")
        oms_page_testset.open()

    elif return_node["reason"] == "upload_documents":
        print("upload_documents")
        oms_page_upload.open()

    elif return_node["reason"] == "view":
        print("view")
        if return_node["node_type"] == "user":
            oms_page_home.open()

        elif return_node["node_type"] == "project":
            oms_page_project.open()

        elif return_node["node_type"] == "specifications":
            pass

        elif return_node["node_type"] == "action":
            print("action")
            oms_page_action.open()

        elif return_node["node_type"] == "variable":
            print("variable")
            oms_page_variable.open()

        elif return_node["node_type"] == "page":
            pass

        elif return_node["node_type"] == "specifications":
            pass

        elif return_node["node_type"] == "documents":
            pass
        else:
            pass
    else:
        pass
else:
    oms_page_home.open()

# oms_page_sidebar.add()
# # if st.session_state.app_state["page_visible"] == "do not change page":
# #     pass
# if st.session_state.app_state["page_visible"] == "home page":
#     oms_page_home.open()
# elif st.session_state.app_state["page_visible"] == "project page":
#     oms_page_project.open()
# elif st.session_state.app_state["page_visible"] == "specification generation page":
#     oms_page_specification_generation.open()
# elif st.session_state.app_state["page_visible"] == "action page":
#     oms_page_action.open()
# elif st.session_state.app_state["page_visible"] == "variable page":
#     oms_page_variable.open()
# elif st.session_state.app_state["page_visible"] == "testset page":
#     oms_page_testset.open()
# elif st.session_state.app_state["page_visible"] == "upload page":
#     oms_page_upload.open()
# else:
#     pass 



