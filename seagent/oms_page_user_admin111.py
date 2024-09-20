import streamlit as st
import yaml
import pandas as pd

def admin():
  # data = yaml.safe_load(yaml_data)
  st.title("用户管理")
  yaml_file = '/opt/bihua/reqgpt/seagent/.streamlit/authentication.yaml'
  with open(yaml_file, 'r') as file:
      data = yaml.safe_load(file)

  # Convert YAML data to a DataFrame
  df = pd.DataFrame(data["credentials"]['usernames']).T  # .T to transpose the dataframe

  df = df.rename_axis("username", axis="index")
  df.columns = ['name', 'password']

  # Allow the user to edit the DataFrame
#   edited_df = st.data_editor(df, width=500, num_rows="dynamic", key="editable_df")
  edited_df = st.data_editor(df, width=500, num_rows="dynamic")

  # Save the edited DataFrame back to YAML
  if st.button('保存'):
      if edited_df.index.hasnans or edited_df.index.duplicated().any():
            st.error("用户名必须唯一且不可为空。")
            return
      
      if edited_df.isnull().any():
            st.error("名字和密码不能为空。")
            return
      # Convert the edited DataFrame back to dictionary format
      updated_usernames = edited_df.T.to_dict()

      # Update the original data with the edited usernames
      data['credentials']['usernames'] = updated_usernames

      # Convert the entire data back to YAML format
      updated_yaml_string = yaml.dump(data, allow_unicode=True)

      # Display the updated YAML string in Streamlit
    #   st.code(updated_yaml_string, language='yaml')

      # Optionally, save the updated YAML string to a file
      with open(yaml_file, "w", encoding='utf-8') as file:
          file.write(updated_yaml_string)

      st.success("用户数据已保存。")
admin()