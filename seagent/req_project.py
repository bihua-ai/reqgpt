import os, re, seagent_file, seagent_general
from dotenv import load_dotenv
import time

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

def create_project_name(user_identifier):
    project_name_base = "项目"
    APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    project_home_path = os.path.join(APP_DATA_HOME, user_identifier)

    # Initialize the maximum found serial number to 0
    max_serial_number = 0

    # Check if the project directory exists
    if os.path.exists(project_home_path):
        # Iterate over all files and directories in the project home path
        for name in os.listdir(project_home_path):
            # Match the pattern "项目" followed by an integer
            match = re.match(f"{project_name_base}(\\d+)", name)
            if match:
                # Extract the number and convert to an integer
                serial_number = int(match.group(1))
                # Update the maximum found serial number
                if serial_number > max_serial_number:
                    max_serial_number = serial_number

    # Form the new project name with the next serial number
    project_name = f"{project_name_base}{max_serial_number + 1}"

    return project_name, project_home_path


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



projects_tree = []

def build_project_tree_json(user_id):
    # build project tree
    load_dotenv()
    APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
    INPUT_DOCUMENT_SUB_DIRECTORY = os.getenv("INPUT_DOCUMENT_SUB_DIRECTORY")

    user_root_path = os.path.join(APP_DATA_HOME, user_id) # data/apps/user_id
    # projects are sub folders under user_id, collect directory name, eahc folder is a project

    projects_tree = {}
    projects_tree["id"] = seagent_general.generate_uuid()
    projects_tree["node_type"] = "user" # same as projects
    projects_tree["name"] = user_id
    projects_tree["children"] = []

    # seagent_file.oms_save("/opt/bihua/reqgpt/seagent/test8.json", projects_tree)

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

                # seagent_file.oms_save("/opt/bihua/reqgpt/seagent/test8.json", projects_tree)

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

                # seagent_file.oms_save("/opt/bihua/reqgpt/seagent/test8.json", projects_tree)

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

                        # seagent_file.oms_save("/opt/bihua/reqgpt/seagent/test8.json", projects_tree)

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

                # seagent_file.oms_save("/opt/bihua/reqgpt/seagent/test8.json", projects_tree)
                
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

                        # seagent_file.oms_save("/opt/bihua/reqgpt/seagent/test8.json", projects_tree)

                        action_len = len(spec_json["omsObject"]["actions"])
                        for j in range(action_len):
                            new_action = {
                                "name": spec_json["omsObject"]["actions"][j]["name"],
                                "id": spec_json["omsObject"]["actions"][j]["identifier"],
                                "node_type": "action",
                                "children": [] 
                            }
                            projects_tree["children"][project_index]["children"][1]["children"][j]["children"].append(new_action)

                            # seagent_file.oms_save("/opt/bihua/reqgpt/seagent/test8.json", projects_tree)

            project_index = project_index + 1
    all_projects_for_one_user = []
    all_projects_for_one_user.append(projects_tree)
    # seagent_file.oms_save("/opt/bihua/reqgpt/seagent/test8.json", all_projects_for_one_user)
    return all_projects_for_one_user






























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








