import streamlit as st
import yaml, os
import pandas as pd
from dotenv import load_dotenv
from yaml.loader import SafeLoader

def admin():
  # data = yaml.safe_load(yaml_data)
  st.title("用户管理")
  load_dotenv()
  AUTHENTICATION_YAML_PATH = os.getenv("AUTHENTICATION_YAML_PATH") 

  # Load authentication configuration
  with open(AUTHENTICATION_YAML_PATH) as file:
      data = yaml.load(file, Loader=SafeLoader)

  # yaml_file = '/opt/bihua/reqgpt/seagent/.streamlit/authentication.yaml'
  # with open(yaml_file, 'r') as file:
  #     data = yaml.safe_load(file)

  # Convert YAML data to a DataFrame
  df = pd.DataFrame(data["credentials"]['usernames']).T  # .T to transpose the dataframe

  # df = df.drop(columns=['email'])

  # Allow the user to edit the DataFrame
  edited_df = st.data_editor(df, width=500, num_rows="dynamic", key="editable_df")

  # Save the edited DataFrame back to YAML
  if st.button('保存'):
      # Convert the edited DataFrame back to dictionary format
      updated_usernames = edited_df.T.to_dict()

      # Update the original data with the edited usernames
      data['credentials']['usernames'] = updated_usernames

      # Convert the entire data back to YAML format
      updated_yaml_string = yaml.dump(data, allow_unicode=True)

      # Display the updated YAML string in Streamlit
    #   st.code(updated_yaml_string, language='yaml')

      # Optionally, save the updated YAML string to a file
      with open(AUTHENTICATION_YAML_PATH, "w", encoding='utf-8') as file:
          file.write(updated_yaml_string)

      st.success("用户数据已保存。")
# admin()