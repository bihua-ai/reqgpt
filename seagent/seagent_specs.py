
import seagent_llm, seagent_general, seagent_file, seagent_pict
import json, os
from seagent_llm import PageListModel, PageModel
from dotenv import load_dotenv
import shutil


def create_one_spec_base_json_file(oms_file_location, object_name = "object name", object_description = "", 
               project_name="My Project", project_summary="A brief summary of the project.",
               project_description="A detailed description of the project.", 
               termsOfService="https://example.com/terms/", contact_name = "My Support Team",
               contact_url="https://www.example.com/support", contact_email="support@example.com",
               license_name = "MPL-2.0", license_url="https://opensource.org/licenses/MPL-2.0",
               license_version="1.0.0", oms_version="1.0.0"):
    
    # Generate a unique file name
    file_name = f"{project_name}_{seagent_general.generate_uuid()}.json"
    
    # Define the data structure
    oms_data = {
        "oms": oms_version,
        "info": {
            "title": project_name,
            "summary": project_summary,
            "description": project_description,
            "termsOfService": termsOfService,
            "contact": {
                "name": contact_name,
                "url": contact_url,
                "email": contact_email
            },
            "license": {
                "name": license_name,
                "url": license_url
            },
            "version": license_version
        },
        "omsObject": {
            "classification": "ui",
            "identifier": seagent_general.generate_uuid(),  # Generate a new UUID for the identifier
            "name": object_name,
            "description": object_description,
            "memberObjects": [],
            "attributes": [],
            "states": [],
            "actions":[]
        }
    }
    file_path = f"{oms_file_location}/{file_name}"
    seagent_file.oms_save(file_path, oms_data)
    return file_path
    
    # # Write the data to a new JSON file
    # file_path = f"{oms_file_location}/{file_name}"
    # with open(file_path, 'w', encoding='utf-8') as file:
    #     json.dump(oms_data, file, indent=4)
    
    return oms_data  # Return the name of the file that was created


# condition for calling this method: input files are uploaded
def create_all_webapp_page_specification_jsons(app_input_document_location, app_spec_file_target_location):

    # inreality, the following should be retrieved from sql database
    # create base ome json
    instruction = "基于附件项目文档，总结一下，用中文给项目起个简短项目名(不多于20个字），不解释结果。"
    project_name = seagent_llm.chat_with_moonshot(instruction)
    project_name = project_name.replace('"', '')
    project_name = project_name.replace("'", "")

    # load_dotenv()
    # APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    # project_document_home = os.path.join(APP_DATA_HOME, project_name)
    # if not os.path.exists(project_document_home):
    #     os.mkdir(project_document_home)
        
    # for item in os.listdir(input_document_location_tmp):
    #     source_item = os.path.join(input_document_location_tmp, item)
    #     destination_item = os.path.join(project_document_home, item)
    #     if os.path.isdir(source_item):
    #         shutil.copytree(source_item, destination_item)
    #     else:
    #         shutil.copy2(source_item, destination_item)

    # SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
    # project_app_specs_home = os.path.join(project_document_home, SPEC_SUB_DIRECTORY)
    project_app_specs_home = app_spec_file_target_location
    # if not os.path.exists(project_app_specs_home):
    #     os.mkdir(project_app_specs_home)

    # project_app_specs_home = os.path.join(apps_specs_home, project_name)
    # os.mkdir(project_app_specs_home)

    instruction = "基于附件项目文档，总结一下，用中文给项目做个描述，只输出项目描述，不解释结果。"
    project_description = seagent_llm.chat_with_moonshot(instruction)
    project_description = project_description.replace('"', '')
    project_description = project_description.replace("'", "")
    

    project_summary = project_description

    i = 1
    page_list = seagent_llm.extract_page_names_from_code()
    num_tries = 1
    while len(page_list.pages) == 0:
        page_list = seagent_llm.extract_page_names_from_code()
        num_tries = num_tries + 1
        print(f"number of tries: {num_tries}")

        if num_tries > 2:
            print(f"no pages after {num_tries} tries, stop.")
            return
    
    for page in page_list.pages:
        # create app_uuid.json for each page
        # page_spec_json_ful_path = os.path.join(project_app_specs_home, page.page_name)

        page_spec_json_ful_path = create_one_spec_base_json_file(project_app_specs_home, page.page_name,
                             page.page_description, project_name, project_summary, project_description)
        
        # seagent_file.oms_save("/opt/bihua/reqgpt/seagent/spec_page.json", spec_json)
        spec_json = seagent_file.oms_load(page_spec_json_ful_path)

        spec_json = seagent_llm.add_spec_info_till_equivalence_classes(spec_json) # states, cars will be done below
        seagent_file.oms_save(page_spec_json_ful_path, spec_json)

        # now use pict to add states and cars
        spec_json = seagent_pict.calculate_states_using_pict(spec_json)
        seagent_file.oms_save(page_spec_json_ful_path, spec_json)
                
        spec_json = seagent_pict.calculate_cars_using_pict(spec_json)
        seagent_file.oms_save(page_spec_json_ful_path, spec_json)

        print(f"final draft is done - {page_spec_json_ful_path}")
    return app_input_document_location, project_app_specs_home
        
        
def create_webapp_page_specifications(app_input_document_location, app_spec_file_target_location):

    seagent_llm.start_moonshot()

    # source_code_location = "/opt/bihua/reqgpt/data/input_documents"
    document_purpose = "附件输入文档，用于生成oms specifications："
    seagent_llm.add_file_content_to_project_messages(app_input_document_location, document_purpose)

    # apps_spec_home = "/opt/bihua/reqgpt/data/apps"
    
    # seagent_file.upload_files(input_document_location)
    project_document_home, project_app_specs_home = create_all_webapp_page_specification_jsons(app_input_document_location, app_spec_file_target_location)

    # seagent_llm.add_next_cars(project_app_specs_home)
    
    return project_document_home, project_app_specs_home