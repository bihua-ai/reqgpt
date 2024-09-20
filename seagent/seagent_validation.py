# pip install jsonschema

import os
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from dotenv import load_dotenv
import seagent_file, seagent_llm
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

validation_client = OpenAI(
        api_key = "sk-hSBH7FZ89TBLfNFCeNfBa3url9v7EQY4NUVKIUPgvRIkm6WF",
        base_url = "https://api.moonshot.cn/v1",
    )

validation_project_messages = [
    {
        "role": "system",
        "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。",
    },
]


def chat_with_moonshot(instruction, user = "user"):

    global validation_client
    global validation_project_messages

    validation_project_messages.append({"role": f"{user}", "content": instruction})
    completion = validation_client.chat.completions.create(
        model="moonshot-v1-32k",
        messages=validation_project_messages,
        temperature=0.3,
    )
    
    return completion.choices[0].message.content


def validate_spec_json(spec_json):
    load_dotenv()
    SPEC_SCHEMA_FILE_PATH = os.getenv("SPEC_SCHEMA_FILE_PATH")
    spec_schema_json = seagent_file.oms_load(SPEC_SCHEMA_FILE_PATH)
    try:
        validate(instance=spec_json, schema=spec_schema_json)
        print("The new specification is valid.")
        return None
    except ValidationError as e:
        print("The new specification is not valid. Error:", e)
        return e
    
def validate_and_correct(spec_json_file_path):
    global validation_client
    global validation_project_messages
    number_of_messages = len(validation_project_messages)

    final_draft_spec = seagent_file.oms_load(spec_json_file_path)

    status = validate_spec_json(final_draft_spec)
    i= 1
    max = 3
    while status is not None and i < max:
        instruction = f"请根据错误信息 {status} 修改 {final_draft_spec}，然后只返回修改后的specification json对象."
        final_draft_spec = seagent_llm.chat_with_moonshot(instruction)
        del validation_project_messages[number_of_messages - 1]

        status = validate_spec_json(final_draft_spec)
        if status is None:
            return final_draft_spec
        
        i = i + 1
        print(f"{spec_json_file_path} has error: {status}")

    return None

def validate_and_correct_all(directory_of_spec_jsons):
    global validation_client
    global validation_project_messages

    load_dotenv()
    SPEC_SCHEMA_FILE_PATH = os.getenv("SPEC_SCHEMA_FILE_PATH")
    schema_json = seagent_file.oms_load(SPEC_SCHEMA_FILE_PATH)
    instruction = f"上传schema json：{schema_json}"
    chat_with_moonshot(instruction, "user")

    for filename in os.listdir(directory_of_spec_jsons):
        file_path = os.path.join(directory_of_spec_jsons, filename)
        spec_returned = validate_and_correct(file_path)
        if spec_returned is not None:
            seagent_file.oms_save(file_path, spec_returned)

    file_list = validation_client.files.list()
    for file_object in file_list.data:
        print(f"{file_object}")
        validation_client.files.delete(file_id=file_object.id)


