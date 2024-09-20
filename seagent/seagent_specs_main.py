
import seagent_specs, seagent_llm


def create_webapp_page_specifications(input_document_location_tmp):

    seagent_llm.start_moonshot()

    # source_code_location = "/opt/bihua/reqgpt/data/input_documents"
    document_purpose = "附件输入文档，用于生成oms specifications："
    seagent_llm.add_file_content_to_project_messages(input_document_location_tmp, document_purpose)

    apps_spec_home = "/opt/bihua/reqgpt/data/apps"
    
    # seagent_file.upload_files(input_document_location)
    project_document_home, project_app_specs_home = seagent_specs.create_all_webapp_page_specification_jsons(input_document_location_tmp)
    
    return project_document_home, project_app_specs_home
 




