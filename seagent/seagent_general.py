import uuid
import json, os
import re
from dotenv import load_dotenv

def generate_uuid():
    # Generate a random UUID
    new_uuid = uuid.uuid4()
    
    # Convert the UUID to a string without hyphens
    compact_uuid = new_uuid.hex
    
    return compact_uuid

def replace_identifiers_with_uuids(json_str):
    # Regular expression to find all 'identifier' values
    pattern = r'"identifier":\s*"([^"]+)"'
    
    # Replace all occurrences of 'identifier' with a new UUID
    updated_json_str = re.sub(pattern, lambda match: f'"identifier":"{generate_uuid()}"', json_str)
    
    return updated_json_str

def replace_state_identifiers_with_uuids(json_str):
    # Regular expression to find all 'identifier' values
    pattern = r'"identifier":\s*"state-[^"]*"'
    
    # Replace all occurrences of 'identifier' with a new UUID
    updated_json_str = re.sub(pattern, lambda match: f'"identifier":"{generate_uuid()}"', json_str)
    
    return updated_json_str

def replace_car_identifiers_with_uuids(json_str):
    # Regular expression to find all 'identifier' values
    pattern = r'"identifier":\s*"car-[^"]*"'
    
    # Replace all occurrences of 'identifier' with a new UUID
    updated_json_str = re.sub(pattern, lambda match: f'"identifier":"{generate_uuid()}"', json_str)
    
    return updated_json_str

def get_document_folders(user_id, project_name):
    load_dotenv()
    APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    INPUT_DOCUMENT_SUB_DIRECTORY = os.getenv("INPUT_DOCUMENT_SUB_DIRECTORY")
    SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")

    user_home = os.path.join(APP_DATA_HOME, user_id)
    if not os.path.exists(user_home):
        os.mkdir(user_home)
    # projiect_identifier = project_name
    project_folder = os.path.join(user_home, project_name)  
    if not os.path.exists(project_folder):
        os.mkdir(project_folder)
    input_document_folder = os.path.join(project_folder, INPUT_DOCUMENT_SUB_DIRECTORY)
    if not os.path.exists(input_document_folder):
        os.mkdir(input_document_folder)
    specification_folder = os.path.join(project_folder, SPEC_SUB_DIRECTORY)
    if not os.path.exists(specification_folder):
        os.mkdir(specification_folder)

    return input_document_folder, specification_folder
