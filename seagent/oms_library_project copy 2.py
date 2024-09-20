import os, re, seagent_file, seagent_general
from dotenv import load_dotenv
import time
from shutil import rmtree
import streamlit as st

# def create_project_name(user_identifier, project_identifier="", project_name=""):
#     load_dotenv()
#     APP_DATA_HOME = os.getenv("APP_DATA_HOME")

#     user_home = os.path.join(APP_DATA_HOME, user_identifier)
#     if not os.path.exists(user_home):
#         os.mkdir(user_home)

#     projiect_identifier = project_identifier

#     final_project_name = ""

#     # name holder, it will be replaced by LLM
#     if project_name == "":
#         project_name = "项目"

#     project_folder = os.path.join(user_home, project_name)  
#     if not os.path.exists(project_folder):
#         final_project_name = project_name
#     else:
#         final_project_name = project_name
#         # counter = 1
#         # while True:
#         #     new_folder_name = f"{project_name} ({counter})"
#         #     if not os.path.exists(os.path.join(user_home, new_folder_name)):
#         #         # os.makedirs(os.path.join(user_home, new_folder_name))
#         #         # print(f"Folder '{new_folder_name}' created.")
#         #         final_project_name = project_name
#         #     counter += 1

#     return final_project_name

# def create_project_name(user_identifier):
#     project_name_base = "项目"
#     APP_DATA_HOME = os.getenv("APP_DATA_HOME")
#     project_home_path = os.path.join(APP_DATA_HOME, user_identifier)

#     # Initialize the maximum found serial number to 0
#     max_serial_number = 0

#     # Check if the project directory exists
#     if os.path.exists(project_home_path):
#         # Iterate over all files and directories in the project home path
#         for name in os.listdir(project_home_path):
#             # Match the pattern "项目" followed by an integer
#             match = re.match(f"{project_name_base}(\\d+)", name)
#             if match:
#                 # Extract the number and convert to an integer
#                 serial_number = int(match.group(1))
#                 # Update the maximum found serial number
#                 if serial_number > max_serial_number:
#                     max_serial_number = serial_number

#     # Form the new project name with the next serial number
#     project_name = f"{project_name_base}{max_serial_number + 1}"

#     return project_name, project_home_path

def user_create(user_identifier):
    load_dotenv()
    APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    user_home = os.path.join(APP_DATA_HOME, user_identifier)
    if not os.path.exists(user_home):
        os.makedirs(user_home)

def project_create(user_identifier, project_name):
    load_dotenv()
    APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    project_home = os.path.join(APP_DATA_HOME, user_identifier, project_name)
    if not os.path.exists(project_home):
        os.makedirs(project_home)

def project_rename(user_identifier, project_name_old, project_name_new):
    load_dotenv()
    APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    project_home_old = os.path.join(APP_DATA_HOME, user_identifier, project_name_old)
    project_home_new = os.path.join(APP_DATA_HOME, user_identifier, project_name_new)
    try:
        if os.path.exists(project_home_old):
            if not os.path.exists(project_home_new):
                os.rename(project_home_old, project_home_new)
            else:
                print(f"Cannot rename project. A project with the name '{project_name_new}' already exists.")
        else:
            print(f"The project '{project_name_old}' does not exist.")

        return True
    except Exception as e:
        print(e)
    finally:
        return False
    
def project_delete(user_identifier, project_name):
    try:
        # Load environment variables from a .env file
        load_dotenv()
        
        # Get the environment variable for the application data home directory
        APP_DATA_HOME = os.getenv("APP_DATA_HOME")
        
        # Define the project home directory path
        project_home = os.path.join(APP_DATA_HOME, user_identifier, project_name)
        
        # Check if the project home directory exists
        if os.path.exists(project_home):
            # Remove the directory and all its contents
            rmtree(project_home)
            print(f"Project '{project_name}' deleted successfully.")
            return True  # Return True to indicate success
        else:
            print(f"The project '{project_name}' does not exist.")
            return False  # Return False because the project did not exist
    except Exception as e:
        # Handle any exception that occurs and print the error message
        print(f"An error occurred while deleting the project: {e}")
        return False  # Return False to indicate failure due to exception
    finally:
        # This block will be executed no matter what, used for cleanup if necessary
        print("Project deletion process finished.")


def documents_delete(user_identifier, project_name, document_name):
    try:
        # Load environment variables from a .env file
        load_dotenv()

        # Get the environment variable for the application data home directory
        APP_DATA_HOME = os.getenv("APP_DATA_HOME")
        
        # Get the environment variable for the input document sub directory
        INPUT_DOCUMENT_SUB_DIRECTORY = os.getenv("INPUT_DOCUMENT_SUB_DIRECTORY")
        
        # Define the document home directory path
        specification_home = os.path.join(APP_DATA_HOME, user_identifier, project_name, INPUT_DOCUMENT_SUB_DIRECTORY)
        
        # Define the path to the specific document to be deleted
        document_path = os.path.join(specification_home, document_name)
        
        # Check if the document home directory exists
        if os.path.exists(specification_home):
            # Check if the specific document exists
            if os.path.exists(document_path):
                # Remove the specific document
                if os.path.isfile(document_path) or os.path.islink(document_path):
                    os.unlink(document_path)  # Remove files and links
                elif os.path.isdir(document_path):
                    rmtree(document_path)  # Remove directories
                return True  # Return True to indicate success
            else:
                print(f"The document '{document_name}' does not exist in the directory.")
                return False  # Return False because the document does not exist
        else:
            print(f"The document home directory does not exist.")
            return False  # Return False because the directory did not exist
    except Exception as e:
        # Handle any exception that occurs and print the error message
        print(f"An error occurred while deleting the document: {e}")
        return False  # Return False to indicate failure due to exception

# Example usage:
# result = documents_delete('user123', 'projectX', 'example_document.txt')
# print('Deletion successful:', result)

def documents_delete(user_identifier, project_name):
    try:
        # Load environment variables from a .env file
        load_dotenv()
        
        # Get the environment variable for the application data home directory
        APP_DATA_HOME = os.getenv("APP_DATA_HOME")
        
        # Get the environment variable for the input document sub directory
        INPUT_DOCUMENT_SUB_DIRECTORY = os.getenv("INPUT_DOCUMENT_SUB_DIRECTORY")
        
        # Define the document home directory path
        documents_home = os.path.join(APP_DATA_HOME, user_identifier, project_name, INPUT_DOCUMENT_SUB_DIRECTORY)
        
        # Check if the document home directory exists
        if os.path.exists(documents_home):
            # Remove the contents of the document directory
            for item in os.listdir(documents_home):
                item_path = os.path.join(documents_home, item)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)  # Remove files and links
                elif os.path.isdir(item_path):
                    rmtree(item_path)  # Remove directories
            return True  # Return True to indicate success
        else:
            return False  # Return False because the directory did not exist
    except Exception as e:
        # Handle any exception that occurs and print the error message
        print(f"An error occurred while deleting documents: {e}")
        return False  # Return False to indicate failure due to exception


def get_filename_from_oms_object_name(spec_path, oms_object_name):
    spec_json = seagent_file.oms_load(spec_path)
    if spec_json["omsObject"]["name"] == oms_object_name:
        return True
    return False

def oms_object_rename(spec_path, oms_object_name_old, oms_object_name_new):
    spec_json = seagent_file.oms_load(spec_path)
    if spec_json["omsObject"]["name"] == oms_object_name_old:
        spec_json["omsObject"]["name"] == oms_object_name_new
        seagent_file.oms_save(spec_path, spec_json)
        return True
    return False

def specification_create(user_identifier, project_name, specification_identifier, oms_object_name):
    try:
        # Load environment variables from a .env file
        load_dotenv()
        
        # Get the environment variable for the application data home directory
        APP_DATA_HOME = os.getenv("APP_DATA_HOME")
        
        # Get the environment variable for the input document sub directory
        SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
        
        # Define the document home directory path
        specification_home = os.path.join(APP_DATA_HOME, user_identifier, project_name, SPEC_SUB_DIRECTORY)
        
        # Check if the document home directory exists
        if os.path.exists(specification_home):
            specification_file_name = f"{oms_object_name}_{specification_identifier}.son"
            path = "data/spec_templates/oms_template_object_only.json"
            spec_template_json = seagent_file.oms_load(path)
            spec_template_json["info"]["title"] = project_name
            spec_template_json["omsObject"]["name"] = oms_object_name
            target_path = os.path.join(specification_home, specification_file_name)
            seagent_file.oms_save(target_path)
            return True  # Return True to indicate success
        else:
            return False  # Return False because the directory did not exist
    except Exception as e:
        # Handle any exception that occurs and print the error message
        print(f"An error occurred while deleting documents: {e}")
        return False  # Return False to indicate failure due to exception

def specification_delete(user_identifier, project_name, oms_object_name):
    try:
        # Load environment variables from a .env file
        load_dotenv()
        
        # Get the environment variable for the application data home directory
        APP_DATA_HOME = os.getenv("APP_DATA_HOME")
        
        # Get the environment variable for the input document sub directory
        SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
        
        # Define the document home directory path
        specification_home = os.path.join(APP_DATA_HOME, user_identifier, project_name, SPEC_SUB_DIRECTORY)
        
        # Check if the document home directory exists
        if os.path.exists(specification_home):
            # Remove the contents of the document directory
            for item in os.listdir(specification_home):
                item_path = os.path.join(specification_home, item)
                if get_filename_from_oms_object_name(item_path, oms_object_name):
                    os.unlink(item_path)  # Remove files and links
                    break
            return True  # Return True to indicate success
        else:
            return False  # Return False because the directory did not exist
    except Exception as e:
        # Handle any exception that occurs and print the error message
        print(f"An error occurred while deleting documents: {e}")
        return False  # Return False to indicate failure due to exception
    
def specifications_delete(user_identifier, project_name):
    try:
        # Load environment variables from a .env file
        load_dotenv()
        
        # Get the environment variable for the application data home directory
        APP_DATA_HOME = os.getenv("APP_DATA_HOME")
        
        # Get the environment variable for the input document sub directory
        SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
        
        # Define the document home directory path
        specification_home = os.path.join(APP_DATA_HOME, user_identifier, project_name, SPEC_SUB_DIRECTORY)
        
        # Check if the document home directory exists
        if os.path.exists(specification_home):
            # Remove the contents of the document directory
            for item in os.listdir(specification_home):
                item_path = os.path.join(specification_home, item)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)  # Remove files and links
                elif os.path.isdir(item_path):
                    rmtree(item_path)  # Remove directories
            return True  # Return True to indicate success
        else:
            return False  # Return False because the directory did not exist
    except Exception as e:
        # Handle any exception that occurs and print the error message
        print(f"An error occurred while deleting documents: {e}")
        return False  # Return False to indicate failure due to exception
    
def specification_oms_object_rename(user_identifier, project_name, oms_old_name, oms_new_name):
    try:
        # Load environment variables from a .env file
        load_dotenv()
        
        # Get the environment variable for the application data home directory
        APP_DATA_HOME = os.getenv("APP_DATA_HOME")
        
        # Get the environment variable for the input document sub directory
        SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
        
        # Define the document home directory path
        specification_home = os.path.join(APP_DATA_HOME, user_identifier, project_name, SPEC_SUB_DIRECTORY)
        
        # Check if the document home directory exists
        if os.path.exists(specification_home):
            # Remove the contents of the document directory
            for item in os.listdir(specification_home):
                item_path = os.path.join(specification_home, item)
                if oms_object_rename(item_path, oms_old_name, oms_new_name):
                    return True  # Return True to indicate success
        else:
            return False  # Return False because the directory did not exist
    except Exception as e:
        # Handle any exception that occurs and print the error message
        print(f"An error occurred while deleting documents: {e}")
        return False  # Return False to indicate failure due to exception


def find_spec_file_add_action(spec_path, oms_object_name, action_name, action_identifier):
    try:
        spec_json = seagent_file.oms_load(spec_path)
        new_action = {
            "identifier": action_identifier,
            "name": action_name,
            "description": "待填",
            "variables": []
        }
        spec_json["omsObject"]["actions"].append(new_action)
        spec_json = seagent_file.oms_save(spec_path, spec_json)
        return True
    except Exception as e:
        print(f"find_spec_file_add_action: {e}")
        return False
    
   

def find_spec_file_delete_action(spec_path, action_identifier):
    try:
        spec_json = seagent_file.oms_load(spec_path)
        number_of_actions = len(spec_json["omsObject"]["actions"])
        for i in range(number_of_actions):
            if spec_json["omsObject"]["actions"][i]["identifier"] == action_identifier:
                del spec_json["omsObject"]["actions"][i]
                spec_json = seagent_file.oms_save(spec_path, spec_json)
                return True
    except Exception as e:
        print(f"find_spec_file_delete_action: {e}")
        return False

def find_spec_file_rename_action(spec_path, action_identifier, action_name_new):
    try:
        spec_json = seagent_file.oms_load(spec_path)
        number_of_actions = len(spec_json["omsObject"]["actions"])
        for i in range(number_of_actions):
            if spec_json["omsObject"]["actions"][i]["identifier"] == action_identifier:
                spec_json["omsObject"]["actions"][i]["name"] = action_name_new
                spec_json = seagent_file.oms_save(spec_path, spec_json)
                return True
    except Exception as e:
        print(f"find_spec_file_rename_action: {e}")
        return False

def find_spec_file_delete_all_actions(spec_path):
    try:
        spec_json = seagent_file.oms_load(spec_path)
        spec_json["omsObject"]["actions"] = []
        spec_json = seagent_file.oms_save(spec_path, spec_json)
        return True
    except Exception as e:
        print(f"find_spec_file_delete_all_actions {e}")
        return False

def find_spec_file_delete_variable(spec_path, variable_identifier):
    try:
        spec_json = seagent_file.oms_load(spec_path) 
        number_of_variables = len(spec_json["omsObject"]["memberObjects"])
        for i in range(number_of_variables):
            if spec_json["omsObject"]["memberObjects"][i]["identifier"] == variable_identifier:
                del spec_json["omsObject"]["memberObjects"][i]
                spec_json = seagent_file.oms_save(spec_path, spec_json)
                return True
    except Exception as e:
        print(f"find_spec_file_delete_variable {e}")
        return False

def find_spec_file_rename_variable(spec_path, variable_identifier, variable_name_new):
    try:
        spec_json = seagent_file.oms_load(spec_path)
        number_of_variables = len(spec_json["omsObject"]["memberObjects"])
        for i in range(number_of_variables):
            if spec_json["omsObject"]["memberObjects"][i]["identifier"] == variable_identifier:
                spec_json["omsObject"]["memberObjects"][i]["name"] = variable_name_new
                spec_json = seagent_file.oms_save(spec_path, spec_json)
                return True
    except Exception as e:
        print(f"find_spec_file_rename_variable {e}")
        return False


def find_spec_file_delete_all_variables(spec_path):
    try:
        spec_json = seagent_file.oms_load(spec_path)
        spec_json["omsObject"]["memberObjects"] = []
        spec_json = seagent_file.oms_save(spec_path, spec_json)
        return True
    except Exception as e:
        print(f"find_spec_file_delete_all_variables {e}")
        return False


# def find_spec_file_add_action(spec_path, oms_object_name, action_name, action_identifier):
#     spec_json = seagent_file.oms_load(spec_path)
    
#     if spec_json["omsObject"]["name"] == oms_object_name:
#         new_action = {
#             "identifier": action_identifier,
#             "name": action_name,
#             "description": "待填",
#             "variables": []
#         }
#         spec_json["omsObject"]["actions"].append(new_action)
#         return True
#     return False

def find_spec_file_add_variable(spec_path, variable_name, variable_identifier):
    try:
        spec_json = seagent_file.oms_load(spec_path)
        new_variable = {
            "identifier": variable_identifier,
            "name": variable_name,
            "description": "待填",
            "attributes": [],
            "states": []
        }
        spec_json["omsObject"]["memberObjects"].append(new_variable)
        return True
    except Exception as e:
        print(f"find_spec_file_add_variable {e}")
        return False


def action_create(user_identifier, project_name, oms_object_name, action_name, action_identifier):
    try:
        # Load environment variables from a .env file
        load_dotenv()
        
        # Get the environment variable for the application data home directory
        APP_DATA_HOME = os.getenv("APP_DATA_HOME")
        
        # Get the environment variable for the input document sub directory
        SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
        
        # Define the document home directory path
        specification_home = os.path.join(APP_DATA_HOME, user_identifier, project_name, SPEC_SUB_DIRECTORY)
        
        # Check if the document home directory exists
        if os.path.exists(specification_home):
            # Remove the contents of the document directory
            for item in os.listdir(specification_home):
                item_path = os.path.join(specification_home, item)
                if find_spec_file_add_action(item_path, oms_object_name, action_name, action_identifier):
                    break
            return True  # Return True to indicate success
        else:
            return False  # Return False because the directory did not exist
    except Exception as e:
        # Handle any exception that occurs and print the error message
        print(f"An error occurred while deleting documents: {e}")
        return False  # Return False to indicate failure due to exception

def action_delete(user_identifier, project_name, action_name, action_identifier):
    try:
        # Load environment variables from a .env file
        load_dotenv()
        
        # Get the environment variable for the application data home directory
        APP_DATA_HOME = os.getenv("APP_DATA_HOME")
        
        # Get the environment variable for the input document sub directory
        SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
        
        # Define the document home directory path
        specification_home = os.path.join(APP_DATA_HOME, user_identifier, project_name, SPEC_SUB_DIRECTORY)
        
        # Check if the document home directory exists
        if os.path.exists(specification_home):
            # Remove the contents of the document directory
            for item in os.listdir(specification_home):
                item_path = os.path.join(specification_home, item)
                if find_spec_file_delete_action(item_path, action_name, action_identifier):
                    break
            return True  # Return True to indicate success
        else:
            return False  # Return False because the directory did not exist
    except Exception as e:
        # Handle any exception that occurs and print the error message
        print(f"An error occurred while deleting documents: {e}")
        return False  # Return False to indicate failure due to exception

def actions_delete(user_identifier, project_name, oms_object_name):
    try:
        # Load environment variables from a .env file
        load_dotenv()
        
        # Get the environment variable for the application data home directory
        APP_DATA_HOME = os.getenv("APP_DATA_HOME")
        
        # Get the environment variable for the input document sub directory
        SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
        
        # Define the document home directory path
        specification_home = os.path.join(APP_DATA_HOME, user_identifier, project_name, SPEC_SUB_DIRECTORY)
        
        # Check if the document home directory exists
        if os.path.exists(specification_home):
            # Remove the contents of the document directory
            for item in os.listdir(specification_home):
                item_path = os.path.join(specification_home, item)
                if find_spec_file_delete_all_actions(item_path, oms_object_name):
                    break
            return True  # Return True to indicate success
        else:
            return False  # Return False because the directory did not exist
    except Exception as e:
        # Handle any exception that occurs and print the error message
        print(f"An error occurred while deleting documents: {e}")
        return False  # Return False to indicate failure due to exception

def variable_create(user_identifier, project_name, oms_object_name, variable_name, variable_identifier):
    try:
        # Load environment variables from a .env file
        load_dotenv()
        
        # Get the environment variable for the application data home directory
        APP_DATA_HOME = os.getenv("APP_DATA_HOME")
        
        # Get the environment variable for the input document sub directory
        SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
        
        # Define the document home directory path
        specification_home = os.path.join(APP_DATA_HOME, user_identifier, project_name, SPEC_SUB_DIRECTORY)
        
        # Check if the document home directory exists
        if os.path.exists(specification_home):
            # Remove the contents of the document directory
            for item in os.listdir(specification_home):
                item_path = os.path.join(specification_home, item)
                if find_spec_file_add_variable(item_path, oms_object_name, variable_name, variable_identifier):
                    break
            return True  # Return True to indicate success
        else:
            return False  # Return False because the directory did not exist
    except Exception as e:
        # Handle any exception that occurs and print the error message
        print(f"An error occurred while deleting documents: {e}")
        return False  # Return False to indicate failure due to exception
    
def variable_delete(user_identifier, project_name, variable_name, variable_identifier):
    try:
        # Load environment variables from a .env file
        load_dotenv()
        
        # Get the environment variable for the application data home directory
        APP_DATA_HOME = os.getenv("APP_DATA_HOME")
        
        # Get the environment variable for the input document sub directory
        SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
        
        # Define the document home directory path
        specification_home = os.path.join(APP_DATA_HOME, user_identifier, project_name, SPEC_SUB_DIRECTORY)
        
        # Check if the document home directory exists
        if os.path.exists(specification_home):
            # Remove the contents of the document directory
            for item in os.listdir(specification_home):
                item_path = os.path.join(specification_home, item)
                if find_spec_file_delete_variable(item_path, variable_name, variable_identifier):
                    break
            return True  # Return True to indicate success
        else:
            return False  # Return False because the directory did not exist
    except Exception as e:
        # Handle any exception that occurs and print the error message
        print(f"An error occurred while deleting documents: {e}")
        return False  # Return False to indicate failure due to exception

def variables_delete(user_identifier, project_name, oms_object_name):
    try:
        # Load environment variables from a .env file
        load_dotenv()
        
        # Get the environment variable for the application data home directory
        APP_DATA_HOME = os.getenv("APP_DATA_HOME")
        
        # Get the environment variable for the input document sub directory
        SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
        
        # Define the document home directory path
        specification_home = os.path.join(APP_DATA_HOME, user_identifier, project_name, SPEC_SUB_DIRECTORY)
        
        # Check if the document home directory exists
        if os.path.exists(specification_home):
            # Remove the contents of the document directory
            for item in os.listdir(specification_home):
                item_path = os.path.join(specification_home, item)
                if find_spec_file_delete_all_variables(item_path, oms_object_name):
                    break
            return True  # Return True to indicate success
        else:
            return False  # Return False because the directory did not exist
    except Exception as e:
        # Handle any exception that occurs and print the error message
        print(f"An error occurred while deleting documents: {e}")
        return False  # Return False to indicate failure due to exception


def get_project_path(user_identifier, project_name):
    APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    spec_json_home = os.path.join(APP_DATA_HOME, user_identifier, project_name)
    return spec_json_home


def get_spec_file_path_from_action_identifier(action_identifier, user_identifier, project_name):
    
    load_dotenv()
    APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
    spec_json_home = os.path.join(APP_DATA_HOME, user_identifier, project_name, SPEC_SUB_DIRECTORY)
    for file_entry in os.scandir(spec_json_home):
        # Check if the entry is a file. It is always a file, there is no subdirectory here.
        if file_entry.is_file():
            spec_path = os.path.join(spec_json_home, file_entry)
            spec_json = seagent_file.oms_load(spec_path)
            for i in range(len(spec_json["omsObject"]["actions"])):
                if action_identifier == spec_json["omsObject"]["actions"][i]["identifier"]:
                    return spec_path    

    return None


def upload_documents(uploaded_files, user_identifier, project_name=""):

    # new_project = True if project_identifier == "" or project_identifier is None else False

    # if new_project:
    #     project_identifier = seagent_general.generate_uuid()
    project_identifier = None
    
    input_document_path, specification_path = seagent_general.get_document_folders(user_identifier, project_name)

    # Check if files were uploaded
    # /opt/bihua/reqgpt/data/apps/{user_id}/project_id/INPUT_DOCUMENT_SUB_DIRECTORY
    # /opt/bihua/reqgpt/data/apps/{user_id}/project_id/SPECIFICATION
    if uploaded_files is not None:
        file_names = []

        for uploaded_file in uploaded_files:
            file_names.append(uploaded_file.name)
            file_name = uploaded_file.name

            # input_document_folder = os.path.join(user_project_home_path, INPUT_DOCUMENT_SUB_DIRECTORY)
            file_content = uploaded_file.read()
            with open(os.path.join(input_document_path, file_name), 'wb') as f:
                f.write(file_content)



def get_variable_name(spec_json, variable_identifier):
    variable_name = None
    number_variables = len(spec_json["omeObject"]["memberObjects"])
    for i in range(number_variables):
        if spec_json["omeObject"]["memberObjects"][i]["identifier"] == variable_identifier:
            variable_name = spec_json["omeObject"]["memberObjects"][i]["name"]
    variable_name

def build_project_tree_json(user_id):
    # build project tree
    load_dotenv()
    APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
    INPUT_DOCUMENT_SUB_DIRECTORY = os.getenv("INPUT_DOCUMENT_SUB_DIRECTORY")

    user_root_path = os.path.join(APP_DATA_HOME, user_id) # data/apps/user_id
    # projects are sub folders under user_id, collect directory name, eahc folder is a project

    projects_tree = {}
    projects_tree["id"] = user_id
    projects_tree["parent_id"] = ""
    projects_tree["node_type"] = "user" # same as projects
    projects_tree["name"] = user_id
    projects_tree["children"] = []

    seagent_file.oms_save("/opt/bihua/reqgpt/seagent/project_tree_sample.json", projects_tree)

    # Iterate over the entries in the directory
    project_index = 0
    with os.scandir(user_root_path) as entries: # data/apps/user_id/projects/project
        for entry in entries:
            # Check if the entry is a directory (subfolder)
            if entry.is_dir():
                # Add the subfolder name to the list
                
                new_project = {
                        "name": entry.name,
                        "id": entry.name,
                        "node_type": "project",
                        "children": []
                }
                projects_tree["children"].append(new_project)

                seagent_file.oms_save("/opt/bihua/reqgpt/seagent/project_tree_sample.json", projects_tree)

                # load input documents
                project_id_as_directory_name = entry.name
                projects_directory = os.path.join(user_root_path, project_id_as_directory_name)

                inout_documents_directory = os.path.join(projects_directory, INPUT_DOCUMENT_SUB_DIRECTORY)
                new_documents = {
                    "name": "Input documents",
                    "id": seagent_general.generate_uuid(),
                    "node_type": "documents",
                    "children": [] 
                }
                projects_tree["children"][project_index]["children"].append(new_documents)
                # projects_tree["children"][0]["name"] = "Documents"
                # projects_tree["children"][project_index]["id"] = seagent_general.generate_uuid()
                # projects_tree["children"][0]["node_type"] = "documents"

                seagent_file.oms_save("/opt/bihua/reqgpt/seagent/project_tree_sample.json", projects_tree)

                # append input documents
                for file_entry in os.scandir(inout_documents_directory):
                    # Check if the entry is a file
                    if file_entry.is_file():
                        # Add the file name to the list
                        new_input_document = {
                            "name": file_entry.name,
                            "id": seagent_general.generate_uuid(),
                            "node_type": "document",
                            "children": [] 
                        }
                        projects_tree["children"][project_index]["children"][0]["children"].append(new_input_document)

                        seagent_file.oms_save("/opt/bihua/reqgpt/seagent/project_tree_sample.json", projects_tree)

                # load specifications
                # project_id_as_directory_name = entry.name
                specification_directory = os.path.join(projects_directory, SPEC_SUB_DIRECTORY)
                new_specifications = {
                        "name": "Specifications",
                        "id": seagent_general.generate_uuid(),
                        "node_type": "specifications",
                        "children": [] 
                }
                # projects_tree["children"][1]["name"] = "Specifications"
                # projects_tree["children"][project_index]["id"] = seagent_general.generate_uuid()
                projects_tree["children"][project_index]["children"].append(new_specifications)

                seagent_file.oms_save("/opt/bihua/reqgpt/seagent/project_tree_sample.json", projects_tree)
                
                for file_entry in os.scandir(specification_directory):
                    # Check if the entry is a file
                    if file_entry.is_file():
                        # get page name, action name
                        spec_json_file_path = os.path.join(specification_directory, file_entry.name)
                        spec_json = seagent_file.oms_load(spec_json_file_path)
                        page_name = spec_json["omsObject"]["name"]
                        page_id = spec_json["omsObject"]["identifier"]

                        # Add page to the list, each json file has one page name
                        new_page = {
                            "name": page_name,
                            "id": page_id,
                            "node_type": "page",
                            "children": [] 
                        }

                        projects_tree["children"][project_index]["children"][1]["children"].append(new_page)

                        seagent_file.oms_save("/opt/bihua/reqgpt/seagent/project_tree_sample.json", projects_tree)

                        action_len = len(spec_json["omsObject"]["actions"])
                        for j in range(action_len):
                            new_action = {
                                "name": spec_json["omsObject"]["actions"][j]["name"],
                                "id": spec_json["omsObject"]["actions"][j]["identifier"],
                                "node_type": "action",
                                "children": [] 
                            }
                            projects_tree["children"][project_index]["children"][1]["children"][j]["children"].append(new_action)
                            seagent_file.oms_save("/opt/bihua/reqgpt/seagent/project_tree_sample.json", projects_tree)

                            # process variables
                            if 'variables' in spec_json['omsObject']['actions'][j]:
                                variable_len = len(spec_json['omsObject']['actions'][j]["variables"])
                                for k in range(variable_len):
                                    variable_identifier = spec_json["omsObject"]["actions"][j]["variables"][k]["identifier"]
                                    new_variable = {
                                        "name": get_variable_name(spec_json, variable_identifier),
                                        "id": variable_identifier,
                                        "node_type": "variable",
                                    }
                                    projects_tree["children"][project_index]["children"][1]["children"][j]["children"][k]["children"].append(new_variable)

            project_index = project_index + 1
    all_projects_for_one_user = []
    all_projects_for_one_user.append(projects_tree)
    # seagent_file.oms_save("/opt/bihua/reqgpt/seagent/project_tree_sample.json", all_projects_for_one_user)
    return all_projects_for_one_user

    #   node_oms_identifier: specification_node["id"],
    #   node_old_name: null,
    #   node_new_name: newSpecificationName,
    #   project_name: project_name

def create():
    return_element = st.session_state.app_state["navtree_return_element"]
    user_identifier = st.session_state.app_state["user_identifier"]
    project_name = return_element["project_name"]
    if return_element["node_type"] == "project":
        project_create(user_identifier, project_name)
    
    if return_element["node_type"] == "page":
        specification_create(user_identifier, project_name, return_element["node_oms_identifier"], return_element["node_new_name"])
    
    if return_element["node_type"] == "action":
        action_create(user_identifier, project_name, return_element["node_oms_identifier"])

    if return_element["node_type"] == "variable":
        variable_create(user_identifier, project_name, return_element["node_oms_identifier"])


def action_rename(user_identifier, project_name, oms_object_name, action_identifier, action_name_new):
    try:
        # Load environment variables from a .env file
        load_dotenv()
        
        # Get the environment variable for the application data home directory
        APP_DATA_HOME = os.getenv("APP_DATA_HOME")
        
        # Get the environment variable for the input document sub directory
        SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
        
        # Define the document home directory path
        specification_home = os.path.join(APP_DATA_HOME, user_identifier, project_name, SPEC_SUB_DIRECTORY)
        
        # Check if the document home directory exists
        if os.path.exists(specification_home):
            # Remove the contents of the document directory
            for item in os.listdir(specification_home):
                item_path = os.path.join(specification_home, item)
                if find_spec_file_rename_action(item_path, oms_object_name, action_identifier, action_name_new):
                    break
            return True  # Return True to indicate success
        else:
            return False  # Return False because the directory did not exist
    except Exception as e:
        # Handle any exception that occurs and print the error message
        print(f"An error occurred while deleting documents: {e}")
        return False  # Return False to indicate failure due to exception

def variable_rename(user_identifier, project_name, oms_object_name, variable_identifier, action_name_new):
    try:
        # Load environment variables from a .env file
        load_dotenv()
        
        # Get the environment variable for the application data home directory
        APP_DATA_HOME = os.getenv("APP_DATA_HOME")
        
        # Get the environment variable for the input document sub directory
        SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
        
        # Define the document home directory path
        specification_home = os.path.join(APP_DATA_HOME, user_identifier, project_name, SPEC_SUB_DIRECTORY)
        
        # Check if the document home directory exists
        if os.path.exists(specification_home):
            # Remove the contents of the document directory
            for item in os.listdir(specification_home):
                item_path = os.path.join(specification_home, item)
                if find_spec_file_rename_variable(item_path, oms_object_name, variable_identifier, action_name_new):
                    break
            return True  # Return True to indicate success
        else:
            return False  # Return False because the directory did not exist
    except Exception as e:
        # Handle any exception that occurs and print the error message
        print(f"An error occurred while deleting documents: {e}")
        return False  # Return False to indicate failure due to exception


def rename():
    return_element = st.session_state.app_state["navtree_return_element"]
    user_identifier = st.session_state.app_state["user_identifier"]
    project_name = return_element["project_name"]

    if return_element["node_type"] == "project":
        project_rename(user_identifier, st.session_state.app_state["node_old_name"], st.session_state.app_state["node_new_name"])
    
    elif return_element["node_type"] == "page":
        specification_oms_object_rename(user_identifier, project_name, st.session_state.app_state["node_old_name"], st.session_state.app_state["node_new_name"])
    
    elif return_element["node_type"] == "action":
        action_rename(user_identifier, project_name, return_element["node_oms_identifier"], st.session_state.app_state["node_new_name"])

    elif return_element["node_type"] == "variable":
        variable_rename(user_identifier, project_name, return_element["node_oms_identifier"], st.session_state.app_state["node_new_name"])


# "checked_elements": {               
#     "checked_projects": [],
#     "checked_documents": [],
#     "checked_specifications": [],
#     "checked_actions": [],
#     "checked_cars": [],
#     "checked_variables": [],
#     "checked_attributes": [],
#     "checked_states": [],
# }


def check():
    return_element = st.session_state.app_state["navtree_return_element"]
    user_identifier = st.session_state.app_state["user_identifier"]
    project_name = return_element["project_name"]

    if return_element["node_type"] == "project":
        st.session_state.app_state["checked_elements"]["checked_projects"].append(return_element)

    elif return_element["node_type"] == "documents":
        st.session_state.app_state["checked_elements"]["checked_documents"].append(return_element)
    
    elif return_element["node_type"] == "page":
        st.session_state.app_state["checked_elements"]["checked_specifications"].append(return_element)

    elif return_element["node_type"] == "action":
        st.session_state.app_state["checked_elements"]["checked_actions"].append(return_element)

    elif return_element["node_type"] == "car":
        st.session_state.app_state["checked_elements"]["checked_cars"].append(return_element)

    elif return_element["node_type"] == "variable":
        st.session_state.app_state["checked_elements"]["checked_variables"].append(return_element)

    elif return_element["node_type"] == "attribute":
        st.session_state.app_state["checked_elements"]["checked_attributes"].append(return_element)

    elif return_element["node_type"] == "state":
        st.session_state.app_state["checked_elements"]["checked_states"].append(return_element)


def delete():
    return_element = st.session_state.app_state["navtree_return_element"]
    user_identifier = st.session_state.app_state["user_identifier"]
    project_name = return_element["project_name"]

    if return_element["node_type"] == "project":
        project_delete(user_identifier, project_name)
    elif return_element["node_type"] == "page":
        specification_delete(user_identifier, project_name, return_element["node_new_name"])
    elif return_element["node_type"] == "action":
        action_delete(user_identifier, project_name, return_element["node_oms_identifier"])
    elif return_element["node_type"] == "variable":
        variable_delete(user_identifier, project_name, return_element["node_oms_identifier"])
    

file = {
    "file_name": "",
    "file_path": "",
    "file_status": "", # marked as pending_delete, deleted, updated, 
    "upload_timestamp":"", # time when the file uploaded
    "last_operation_timestamp": "", # 
    "user": ""
}

files = {
    "files": [file, file]
}

project = {
    "project_identifier": "",
    "project_name":"",
    "project_description":"",
    "user_identifier": "",
    "project_documents": files
}

projects = {
    "projects": []
}

def load_project_json(user_project_home_path, user_identifier):
    user_file = f"{user_identifier}.json"
    p = os.path.join(user_project_home_path, user_file)
    project_json = None
    if os.path.exists(p):
        project_json = seagent_file.oms_load(p)

    return project_json

def save_project_json(project_json, user_project_home_path, user_identifier):
    user_file = f"{user_identifier}.json"
    p = os.path.join(user_project_home_path, user_file)

    seagent_file.oms_save(p, project_json)


def get_projects(user_project_home_path, user_identifier):
    user_file = f"{user_identifier}.json"
    p = os.path.join(user_project_home_path, user_file)
    project_json = seagent_file.oms_load(p)

    list_of_projects = project_json["projects"]

    return list_of_projects

def add_file():
    pass

def add_project(project_name, project_identifier, project_description, user_identifier):
    load_dotenv()
    APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    user_file = f"{user_identifier}.json"
    p = os.path.join(APP_DATA_HOME, user_file)
    if not os.path.exists(p):
        os.mkdir(p)
        projects_json = {
            "projects": []
        }
    projects_json = seagent_file.oms_load(p)

    new_project = {
        "project_identifier": seagent_general.generate_uuid(),
        "project_name": project_name,
        "project_description": project_description,
        "user_identifier": user_identifier,
        "project_documents": []
    }

    projects_json["projects"].append(new_project)

    
    seagent_file.oms_save(p, projects_json)

def add_input_document_name_to_project_json(input_file_name, user_identifier, user_project_home_path, project_identifier):
    load_dotenv()
    INPUT_DOCUMENT_SUB_DIRECTORY = os.getenv("INPUT_DOCUMENT_SUB_DIRECTORY")
    p = os.path.join(user_project_home_path, user_identifier)
    q = os.path.join(p, INPUT_DOCUMENT_SUB_DIRECTORY)
    time_str = str(time.time())
    new_file = {
        "file_name": input_file_name,
        "file_path": p,
        "file_status": "added", # marked as pending_delete, deleted, updated, 
        "upload_timestamp": time_str, # time when the file uploaded
        "last_operation_timestamp": time_str, # 
        "user": ""
    }
    
    project_json = load_project_json(user_project_home_path, user_identifier)








