import streamlit as st
st.set_page_config(

    page_title="SpecMap",
    page_icon="/opt/bihua/reqgpt/seagent/logo.png",
    layout="wide",  # Optional: Set the layout to wide
    initial_sidebar_state="expanded"  # Optional: Set the initial state of the sidebar
)


import oms_page_documents, oms_page_document, oms_page_specifications, oms_page_information, oms_page_specification, oms_page_sidebar, oms_page_home, oms_config, oms_page_project, oms_page_specification_generation, oms_page_action, oms_page_variable, oms_page_testset, oms_page_upload

######################################################
# configuration
######################################################

st.markdown("""
    <style>
    /* Change the default font size for the entire page */
    html, body, [class*="css"]  {
        font-size: 18px;  /* Adjust this value to change the global font size */
    }   
    header[data-testid="stHeader"] {
                display: none;
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

if "AI" not in st.session_state.app_state:
    st.session_state.app_state["AI"] = None

oms_page_sidebar.add()
# if st.session_state.app_state["page_visible"] == "do not change page":
#     pass
if st.session_state.app_state["page_visible"] == "home page":
    oms_page_home.open()
elif st.session_state.app_state["page_visible"] == "project page":
    oms_page_project.open()
elif st.session_state.app_state["page_visible"] == "specifications page":
    # oms_page_specification_generation.open()
    oms_page_specifications.open()
elif st.session_state.app_state["page_visible"] == "action page":
    oms_page_action.open()
elif st.session_state.app_state["page_visible"] == "variable page":
    oms_page_variable.open()
elif st.session_state.app_state["page_visible"] == "testset page":
    oms_page_testset.open()
elif st.session_state.app_state["page_visible"] == "upload page":
    oms_page_upload.open()
elif st.session_state.app_state["page_visible"] == "specification page":
    oms_page_specification.open()
elif st.session_state.app_state["page_visible"] == "information page":
    oms_page_information.open()
elif st.session_state.app_state["page_visible"] == "documents page":
    oms_page_documents.open()
elif st.session_state.app_state["page_visible"] == "document page":
    oms_page_document.open()
else:
    pass 



