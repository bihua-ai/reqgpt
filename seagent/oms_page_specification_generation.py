import streamlit as st
import time
import threading
import oms_library_specification

def open():
    st.title("生成规约")
    if st.session_state.app_state["AI"] == None:
        st.write("AI规约生成功能以后会提供。")
        return

    status_text = st.empty()
    progress = st.progress(0)

    if st.button("点击生成规约"):
        user_identifier = st.session_state.app_state["user_identifier"]
        project_name = st.session_state.app_state["project_name"]
        oms_library_specification.generate_oms(user_identifier, project_name)
        print("Done!")


        # if "oms_generated" not in st.session_state:
        #     st.session_state.app_state["oms_generated"] = False
        # user_identifier = st.session_state.app_state["user_identifier"]
        # project_name = st.session_state.app_state["project_name"]

        # # Start task in a separate thread
        # threading.Thread(target=oms_library_specification.generate_oms, args=(user_identifier, project_name)).start()  
        
        # count = 0
        # while not st.session_state["oms_generated"]:
        #     progress.progress(count % 100 + 1)
        #     status_text.text(f"Operation in progress... {count} seconds elapsed.")
        #     count += 1
        #     time.sleep(1)
        
        # progress.progress(100)
        # status_text.text("完成!")






# def open():
#     st.title("生成规约")
#     progress_text = "Operation in progress. Please wait."
#     my_bar = st.progress(0, text=progress_text)

#     for percent_complete in range(100):
#         time.sleep(0.01)
#         my_bar.progress(percent_complete + 1, text=progress_text)
#     time.sleep(1)
#     my_bar.empty()

