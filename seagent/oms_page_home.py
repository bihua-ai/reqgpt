import streamlit as st
import oms_library_project, oms_component_upload, oms_library_specification, oms_page_testset, oms_library_testset, oms_page_sidebar
import streamlit.components.v1 as components
import string, os, base64
from datetime import datetime
from io import BytesIO

def open():
    
    if st.session_state.app_state["AI"] == None:
        st.title("介绍")
        # st.markdown(f'<h2 style="font-size:30px;">介绍</h2>', unsafe_allow_html=True)
        st.write("笔画智能软件工程平台用于软件行为智能分析、军工级别软件测试用例设计和生成。")
        st.write("软件工作两件事，把软件讲清楚，把软件做出来。把软件讲清楚涉及软件需求，软件内部模块划分，模块内部算法设计，测试用例，等等。本工具专注软件行为分析，简单实用，可以让软件工程真正工程化。")
        return
    # st.title("上传文档或代码，一键生成全覆盖测试用例、知识库等。")
    st.markdown(f'<h2 style="font-size:30px;">上传文档或代码，一键生成全覆盖测试用例、知识库等。</h2>', unsafe_allow_html=True)
    with st.container(height=400):
        st.write("上传代码，需求文档等：")
        user_identifier = st.session_state.app_state["user_identifier"]
        project_name = st.session_state.app_state["project_name"]
        uploaded = False
        uploaded = oms_component_upload.upload_ui(user_identifier)
        if uploaded:
            st.write(f"完成上传文档！")
        if st.button("生成全覆盖测试用例等文档"):
            if not uploaded:
                st.write(f"请先上传文档！")
            else:
                st.write(st.session_state.app_state["project_name"])

                oms_library_specification.generate_oms(user_identifier, project_name)
                print("generate_oms...done!")



        # if uploaded:
        #     st.session_state.app_state["navtree_key"] = st.session_state.app_state["navtree_key"] + "1"
        #     oms_page_sidebar.add()
        #     print("open()")
        #     print(st.session_state.app_state["navtree_key"])
            # if st.session_state.app_state["return"] == False:
            #     st.reurn()
            # oms_page_sidebar.add()
            

        # project_path = None
        # if project_name is not None:
        #     project_path = oms_library_project.get_project_path(user_identifier, project_name)
        # if st.button("生成全覆盖测试用例等文档"):
        #     if not uploaded:
        #         st.write(f"请先上传文档！")
        #     else:
        #         st.write(st.session_state.app_state["project_name"])

        #         oms_library_specification.generate_oms(user_identifier, project_name)
        #         print("generate_oms...done!")

                # oms_page_testset.generate_full_coverage_testset(user_identifier, project_name)
                # current_datetime = datetime.now()
                # formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                # file_name = "测试集" + formatted_datetime
                # testcase_scope = []
                # project_name = st.session_state.app_state["project_name"]
                # user_identifier = st.session_state.app_state["user_identifier"]
                # testset_xlsx_data = oms_library_testset.generate_testset(user_identifier, project_name,  testcase_scope)

                # buffer = BytesIO()
                # testset_xlsx_data.save(buffer)
                # buffer.seek(0)  # Move the cursor to the beginning of the buffer
                # xlsx_data = buffer.getvalue()
                # b64 = base64.b64encode(xlsx_data).decode()  # Encode bytes to base64
                # download_link = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{file_name}">{file_name}</a>'
                # # st.markdown(f'<a href="{download_link}" download="sample_data.xlsx" id="download_link">Hidden Download</a>', unsafe_allow_html=True)
                # st.markdown("## 测试集")
                # st.markdown("---")  # Horizontal line
                # st.markdown(download_link, unsafe_allow_html=True)
    # st.markdown("## 高级操作可以从左边导航树开始")
    st.markdown(f'<h3 style="font-size:20px;">高级操作可以从左边导航树开始。</h3>', unsafe_allow_html=True)