import os, json
from dotenv import load_dotenv
import seagent_llm

def oms_load(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        oms_data = json.load(file)
    return oms_data

def oms_save(file_path, oms_data):
    # print(oms_data)
    json_string = json.dumps(oms_data, sort_keys=True, ensure_ascii=False, indent=4)
    spec_json_str = json.loads(json_string)
    # print(json_string)
    with open(file_path, 'w', encoding='utf-8') as file:
         json.dump(spec_json_str, file, ensure_ascii=False, indent=4)

    # with open(file_path, 'w', encoding='utf-8') as file:
    #     json.dump(json_string, file, ensure_ascii=False, indent=4)

async def upload_files(input_documents):
    # put files to target folders, to avoid repeated upload
    load_dotenv()
    INPUT_DOCUMENT_PATH = os.getenv("INPUT_DOCUMENT_PATH")
    for file in input_documents:
        filename = file.filename
        file_content = await file.read()
        full_path = f"{INPUT_DOCUMENT_PATH}/{filename}"
        # Process the file as needed, e.g., save to disk or database
        # For example, saving the file to the current directory
        with open(full_path, "wb") as f:
            f.write(file_content)
        print(f"File {filename} uploaded successfully.")


    # upload to llm
    seagent_llm.upload_files(input_documents)
