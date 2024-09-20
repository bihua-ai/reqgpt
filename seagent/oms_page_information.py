import streamlit as st
import oms_library_project, oms_component_upload, oms_library_specification, oms_page_testset, oms_library_testset, oms_page_sidebar
import streamlit.components.v1 as components
import string, os, base64
from datetime import datetime
from io import BytesIO

def open():

    st.markdown(f'<h2 style="font-size:30px;">信息提示</h2>', unsafe_allow_html=True)
    st.write("操作完毕。")

    