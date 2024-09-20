from pathlib import Path
from openai import OpenAI
import instructor, openai
from enum import Enum
import asyncio, json, os
from pydantic import BaseModel, Field
from typing import List
import seagent_file, seagent_general, seagent_validation
from dotenv import load_dotenv
import time
from typing import *
from pathlib import Path
import httpx

##########moonshot#####################################################################################
# 注意，单个用户最多只能上传 1000 个文件，单文件不超过 100MB，同时所有已上传的文件总和不超过 10G 容量。
# 如果您要抽取更多文件，需要先删除一部分不再需要的文件。文件解析服务限时免费，请求高峰期平台可能会有限流策略。
# https://platform.moonshot.cn/docs/api/files#%E4%B8%8A%E4%BC%A0%E6%96%87%E4%BB%B6
# #####################################################################################################

class CarModel(BaseModel):
    car_identifier: str = Field(..., description="The identifier of the car.")
    car_description: str = Field(..., description="A brief summary of what the car is about.")

class CarListModel(BaseModel):
    car_list: List[CarModel] = Field(default_factory=list, description="A list of cars.")

class PageModel(BaseModel):
    page_name: str = Field(..., description="The title of the registration page.")
    page_description: str = Field(..., description="A brief summary of what the registration page is about.")

class PageListModel(BaseModel):
    pages: List[PageModel] = Field(default_factory=list, description="A list of all registration page models.")

class ActionModel(BaseModel):
    action_name: str = Field(..., description="The name of an action to be taken on a web page.")
    action_description: str = Field(..., description="A detailed description of the action on a web page.")

class ActionsModel(BaseModel):
    action_list: List[ActionModel] = Field(default_factory=list, description="A list of the actions on a web page.")

class VariableModel(BaseModel):
    variable_name: str = Field(..., description="The name of the variable used by a specific action. It can be a variable of input, output or environment.")
    variable_description: str = Field(..., description="A detailed description of the variable used by a specific action.")
    variable_classification: str = Field(..., description="The classification of the variable, such as input, output, or environmental.")

class VariablesModel(BaseModel):
    variable_list: List[VariableModel] = Field(default_factory=list, description="A list of all variables used by a specific action.")

class DuplicatedEquivalenceClassIdentifiers(BaseModel):
    duplidate_list: List[str] = Field(default_factory=list, description="A list of equivalence class identifiers.")

class EquivalenceClassModel(BaseModel):
    equivalence_class_name: str = Field(..., description="The name of the equivalence class for a variable.")
    equivalence_class_description: str = Field(..., description="A description of the equivalence class.")

class EquivalenceClassesModel(BaseModel):
    equivalence_class_list: List[EquivalenceClassModel] = Field(default_factory=list, description="A list of all equivalence classes for an attribute.")

class AttributeModel(BaseModel):
    attribute_name: str = Field(..., description="The name of an attribute of a variable.")
    attribute_description: str = Field(..., description="A description of the attribute.")
    # equivalence_class_identifiers: List[str] = Field(default_factory=list, description="Identifiers for the equivalence classes related to this attribute.")

class AttributesModel(BaseModel):
    attribute_list: List[AttributeModel] = Field(default_factory=list, description="A list of all attributes of a variable.")


# for input documents
moonshot_client = OpenAI(
        api_key = "sk-hSBH7FZ89TBLfNFCeNfBa3url9v7EQY4NUVKIUPgvRIkm6WF",
        base_url = "https://api.moonshot.cn/v1",
    )

all_file_contents = []

project_messages = [
    {
        "role": "system",
        "content": "你是 Kimi，由 Moonshot AI 提供的软件工程师人工智能助手，你熟悉软件需求、代码分析、测试场景设计和生成、更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。",
    },
]

# for input documents
moonshot_output_spec_client = OpenAI(
        api_key = "sk-hSBH7FZ89TBLfNFCeNfBa3url9v7EQY4NUVKIUPgvRIkm6WF",
        base_url = "https://api.moonshot.cn/v1",
    )


output_spec_messages = [
    {
        "role": "system",
        "content": "你是 Kimi，由 Moonshot AI 提供的软件工程师人工智能助手，你熟悉软件需求、代码分析、测试场景设计和生成、更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。",
    },
]


# project_messages = [
#     {
#         "role": "system",
#         "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。",
#     },
#     {
#         "role": "system",
#         "content": all_file_contents,
#     },
#     {"role": "user", "content": "基于文件内容，回答我的问题。"},
# ]


def start_moonshot():
    global moonshot_client
    global project_messages

    file_list = moonshot_client.files.list()

    print(f"number of old files uploaded = {len(file_list.data)}")

    for file_object in file_list.data:
        print(f"{file_object}")
        moonshot_client.files.delete(file_id=file_object.id)

    # chat_with_moonshot("你好！")

def stop_moonshot():
    global moonshot_client
    for file in moonshot_client.files.list:
        moonshot_client.files.delete(file_id=file.id)

# def upload_files_to_moonshot_client(files: List[str], cache_tag: Optional[str] = None) -> List[Dict[str, Any]]:
#     global moonshot_client
#     global project_messages
#     messages = []
#     for file in files:
#         file_object = moonshot_client.files.create(file=Path(file), purpose="file-extract")
#         file_content = moonshot_client.files.content(file_id=file_object.id).text
#         messages.append({
#             "role": "system",
#             "content": file_content,
#         })
#     if cache_tag:
#         r = httpx.post(f"{moonshot_client.base_url}caching",
#                        headers={
#                            "Authorization": f"Bearer {moonshot_client.api_key}",
#                        },
#                        json={
#                            "model": "moonshot-v1",
#                            "messages": messages,
#                            "ttl": 300,
#                            "tags": [cache_tag],
#                        })
 
#         if r.status_code != 200:
#             raise Exception(r.text)
#         return [{
#         "role": "cache",
#         "content": f"tag={cache_tag};reset_ttl=300",
#         }]
#     else:
#         return messages
    


def add_file_content_to_project_messages(directory_of_files_temp, document_purpose, user = "system"):
    global moonshot_client
    global project_messages

    # file_messages = upload_files_to_moonshot_client(
    #     files=["upload_files.py"],
    #     cache_tag="upload_files",
    # )

    messages = [
        # 我们使用 * 语法，来解构 file_messages 消息，使其成为 messages 列表的前 N 条 messages。
        *file_messages,
        {
            "role": "system",
            "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，"
                       "准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不"
                       "可翻译成其他语言。",
        },
        {
            "role": "user",
            "content": "总结一下这些文件的内容。",
        },
    ]

    completion = moonshot_client.chat.completions.create(
        model="moonshot-v1-128k",
        messages=messages,
    )
 
    print(completion.choices[0].message.content)



    for filename in os.listdir(directory_of_files_temp):
        file_path = os.path.join(directory_of_files_temp, filename)
        with open(file_path, 'r') as file:
             code_content = file.read()
        project_messages.append({"role": "user", "content": code_content})





def add_file_content_to_output_spec_messages(directory_of_files_to_submit, document_purpose, user = "system"):
    global moonshot_output_spec_client
    global output_spec_messages

    file_list = moonshot_client.files.list()

    print(f"number of old files uploaded = {len(file_list.data)}")

    for file_object in file_list.data:
        print(f"{file_object}")
        moonshot_output_spec_client.files.delete(file_id=file_object.id)


    for filename in os.listdir(directory_of_files_to_submit):
        file_path = os.path.join(directory_of_files_to_submit, filename)
        with open(file_path, 'r') as file:
             code_content = file.read()
        output_spec_messages.append({"role": "user", "content": code_content})

def chat_with_moonshott_output_spec(instruction, user = "user"):

    global moonshot_output_spec_client
    global output_spec_messages

    output_spec_messages.append({"role": f"{user}", "content": instruction})

    while True:
        try:
            completion = moonshot_client.chat.completions.create(
                model="moonshot-v1-32k",
                messages=output_spec_messages,
                # max_tokens= 16000,
                temperature=0.3,
            )
            output_spec_messages.pop()
            return completion.choices[0].message.content
        except openai.RateLimitError as e:
            print("Rate limit exceeded. Waiting for 60 seconds...")
            time.sleep(60)
        except Exception as e:
            print(f"An error occurred in chat_with_moonshott_output_spec: {e}")
            break


def chat_with_moonshot_output_spec_partial_mode(instruction, user = "user"):
    global moonshot_output_spec_client
    global output_spec_messages

    print(instruction)


    output_spec_messages.append({"role": f"{user}", "content": instruction})
    output_spec_messages.append({"role": "assistant", "content": "{", "partial": True})

    while True:
        try:
            completion = moonshot_output_spec_client.chat.completions.create(
                model="moonshot-v1-32k",
                messages=output_spec_messages,
                # max_tokens= 16000,
                temperature=0.3,
            )
            msg1 = completion.choices[0].message.content
            msg = "{" + msg1
            output_spec_messages.pop()
            output_spec_messages.pop()
            return msg
        except openai.RateLimitError as e:
            print("Rate limit exceeded. Waiting for 60 seconds...")
            time.sleep(60)
        except Exception as e:
            print(f"An error occurred in chat_with_moonshot_output_spec_partial_mode: {e}")
            break


    
def upload_files_to_moonshot(directory_of_files_to_submit, document_purpose, user = "system"):

    global moonshot_client
    global project_messages

    for filename in os.listdir(directory_of_files_to_submit):
    # Construct full file path
        file_path = os.path.join(directory_of_files_to_submit, filename)
        files_to_submit = []
        file_object = moonshot_client.files.create(file=Path(file_path), purpose="file-extract")
        file_content = moonshot_client.files.content(file_id=file_object.id).text
        files_to_submit.append(file_content)

        instruction = f"{document_purpose}：{files_to_submit}"
        chat_with_moonshot(instruction, user)


def chat_with_moonshot_partial_mode(instruction, user = "user"):
    global moonshot_client
    global project_messages


    project_messages.append({"role": f"{user}", "content": instruction})
    project_messages.append({"role": "assistant", "content": "{", "partial": True})

    while True:
        try:
            completion = moonshot_client.chat.completions.create(
                model="moonshot-v1-32k",
                messages=project_messages,
                # max_tokens=16000,
                temperature=0.3,
            )
            msg1 = completion.choices[0].message.content
            msg = "{" + msg1
            project_messages.pop()
            project_messages.pop()
            return msg
        except openai.RateLimitError as e:
            print("Rate limit exceeded. Waiting for 60 seconds...")
            time.sleep(60)
        except Exception as e:
            print(f"An error occurred in chat_with_moonshot_partial_mode: {e}")
            break




    

def chat_with_moonshot_without_history(instruction, user = "user"):

    client = OpenAI(
        api_key = "sk-hSBH7FZ89TBLfNFCeNfBa3url9v7EQY4NUVKIUPgvRIkm6WF",
        base_url = "https://api.moonshot.cn/v1",
    )

    project_messages = [
        {
            "role": "system",
            "content": "你是 Kimi，由 Moonshot AI 提供的软件工程师人工智能助手，你熟悉软件需求、代码分析、测试场景设计和生成、更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。",
        },
    ]


    project_messages.append({"role": f"{user}", "content": instruction})

    while True:
        try:
            completion = moonshot_client.chat.completions.create(
                model="moonshot-v1-32k",
                messages=project_messages,
                # max_tokens= 16000,
                temperature=0.3,
            )  
            return completion.choices[0].message.content
        except openai.RateLimitError as e:
            print("Rate limit exceeded. Waiting for 60 seconds...")
            time.sleep(60)
        except Exception as e:
            print(f"An error occurred in chat_with_moonshot_without_history: {e}")
            break



def chat_with_moonshot(instruction, user = "user"):

    global moonshot_client
    global project_messages

    project_messages.append({"role": f"{user}", "content": instruction})

    while True:
        try:
            completion = moonshot_client.chat.completions.create(
                model="moonshot-v1-32k",
                messages=project_messages,
                # max_tokens= 16000,
                temperature=0.3,
            )
            project_messages.pop()
            return completion.choices[0].message.content
        except openai.RateLimitError as e:
            print("Rate limit exceeded. Waiting for 60 seconds...")
            time.sleep(60)
        except Exception as e:
            print(f"An error occurred in chat_with_moonshot: {e}")
            break

    

def chat_with_moonshot_with_input_model(content, data_model):
    try:
        client = instructor.from_openai(
            OpenAI(
                api_key = "sk-hSBH7FZ89TBLfNFCeNfBa3url9v7EQY4NUVKIUPgvRIkm6WF",
                base_url = "https://api.moonshot.cn/v1",
            ),
            mode=instructor.Mode.JSON,
        )

        # llamafamily/llama3-chinese-8b-instruct
        resp = client.chat.completions.create(
            model="moonshot-v1-32k",
            messages=[
                {
                    "role": "user",
                    "content": f"{content}",
                }
            ],
            response_model=data_model,
        )
        return resp
    except AssertionError:
        # client.close()
        print(f"{data_model}: AssertionError")
        return None


# from ollama import Client
def chat_with_llama3_with_input_model(content, data_model):

    code_content = content
    file_path = "/opt/bihua/reqgpt/seagent/tmp.txt"

    with open(file_path, "w") as file:
        file.write(content)

    with open(file_path, 'r') as file:
        temp_str = file.read()

    raw_content = f"r{repr(temp_str)}"


    # enables `response_model` in create call
    try:
        client = instructor.from_openai(
            OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama",  # required, but unused
            ),
            mode=instructor.Mode.JSON,
        )

        print("in chat_with_llama3_with_input_model")
        print(f"{content}\n")


        # llamafamily/llama3-chinese-8b-instruct
        resp = client.chat.completions.create(
            model="llamafamily/llama3-chinese-8b-instruct",
            messages=[
                {
                    "role": "user",
                    "content": f"{raw_content}",
                }
            ],
            response_model=data_model,
        )
        return resp
    except AssertionError:
        # client.close()
        print(f"{data_model}: AssertionError")
        return None


def chat_with_llama3_with_input_model_old(instruction, data_model):
    try:
        client = instructor.patch(openai.OpenAI(
            api_key = "ollama3", 
            base_url = "http://localhost:11434/v1"))
        
        model_retured = client.chat.completions.create(
            model="yi:6b",
            response_model=data_model,
            messages=[
                {"role": "user", "content": instruction},
            ],
        )
        # client.close()
        print(model_retured)
        assert isinstance(model_retured, data_model)

        return model_retured
    except AssertionError:
        # client.close()
        print(f"{data_model}: AssertionError")
        return None
    
##############Page######################

# class VariableStateModel(BaseModel):
#     Variable_identifier: str
#     state_identifier_list: List[str] = []

# class VariableStatesModel(BaseModel):
#     variable_list: List[VariableStateModel] = []



def extract_page_names_from_code():
    instruction = "根据附件代码, 找出软件的所有UI页面"
    resp = chat_with_moonshot(instruction)
    statement = f"在下文找出所有页面，一定用中文回答: {resp}"
    page_list_model = chat_with_moonshot_with_input_model(statement, PageListModel)
    return page_list_model
    
    # try:
    #     client = instructor.patch(openai.OpenAI(
    #         api_key = "ollama3", 
    #         base_url = "http://localhost:11434/v1"))
        
    #     model = client.chat.completions.create(
    #         model="llamafamily/llama3-chinese-8b-instruct",
    #         response_model=PageListModel,
    #         messages=[
    #             {"role": "user", "content": statement},
    #         ],
    #     )
    #     # client.close()
    #     assert isinstance(model, PageListModel)

    #     return model.pages

    # except AssertionError:
    #     # client.close()
    #     print("PageListModel: AssertionError")
    #     return None
    


def create_equivalence_class(equivalence_class_name, equivalence_class_description):
    new_equivalence_class = {
        "identifier": seagent_general.generate_uuid(),  
        "name": equivalence_class_name,  
        "description": equivalence_class_description
    }
    return new_equivalence_class


def create_equivalence_class_list(page_name, action_name, variable_name, attribute_name):
    if attribute_name == "value":
        print("here create_equivalence_class_list")
    instruction = f"""
        {variable_name} 是页面{page_name}的操作（action，{action_name}）的相关变量（variable）。
        {attribute_name} 是{variable_name}的一个attribute。

        基于上面的代码，找出 {attribute_name}  的所有等价类（有效等价类和无效等价类）。

        每个等价类对象有两个元素：
        equivalence class name（如果不是中文，添加名字中文翻译）, 和
        equivalence class description（一句话(此等价类...)解释等价类业务意义）。
        
        去掉输出内容的特殊字符，不解释结果。

    """
    equivalent_classes_string = chat_with_moonshot(instruction)
    # equivalent_classes_string = equivalent_classes_string.replace('"', '')
    # equivalent_classes_string = equivalent_classes_string.replace("'", "")
    statement = f"在下文找出所有等价类，一定用中文回答: {equivalent_classes_string}"
    
    equivalent_classes = chat_with_moonshot_with_input_model(equivalent_classes_string, EquivalenceClassesModel)

    if len(equivalent_classes.equivalence_class_list) == 0:
        # debug code
        print(f"{variable_name}  {attribute_name}")
        # debug ocde ends

        created_eqc_instruction = f"""
            既然代码没有提及变量属性，那就依照名字含义（页面名称（{page_name}）、
            操作名称（{action_name}）、变量名称（{variable_name}））、
            变量属性（{attribute_name}），
            给出此属性的等价类json对象表（此表包含一个正面有效等价类，一个无效等价类）。

            只输出变量{variable_name}的相关属性{attribute_name}的等价类json对象表，
            每个等价类对象有两个元素：
            equivalence class name（如果不是中文，添加名字中文翻译）, 和
            equivalence class description（一句话(此等价类...)解释等价类业务意义）。

            去掉输出内容的特殊字符，不解释结果。

        """
                    
        created_equivalent_classes_string = chat_with_moonshot_partial_mode(created_eqc_instruction)
        # created_equivalent_classes_string = equivalent_classes_string.replace('"', '')
        # created_equivalent_classes_string = equivalent_classes_string.replace("'", "")
        statement = f"在下文找出所有等价类，一定用中文回答: {created_equivalent_classes_string}"
        created_equivalent_classes = chat_with_moonshot_with_input_model(statement, EquivalenceClassesModel)
        
        if len(created_equivalent_classes.equivalence_class_list) == 0:
            new_equivalence_class_list = []
            new_equivalence_class = create_equivalence_class("临时等价类", 
                                                             "系统没找到合适等价类，暂时用这个替代。用户自己可以改。")
            new_equivalence_class_list.append(new_equivalence_class)
            return new_equivalence_class_list

        new_equivalence_class_list = []
        for created_equivalence_class in created_equivalent_classes.equivalence_class_list:
            new_equivalence_class = create_equivalence_class(created_equivalence_class.equivalence_class_name, 
                                                             created_equivalence_class.equivalence_class_description)
            
            new_equivalence_class_list.append(new_equivalence_class)

        return new_equivalence_class_list
    
    new_equivalence_class_list = []
    for equivalent_class in equivalent_classes.equivalence_class_list:
        new_equivalence_class = create_equivalence_class(equivalent_class.equivalence_class_name, 
                                                             equivalent_class.equivalence_class_description)
            
        new_equivalence_class_list.append(new_equivalence_class)
    return new_equivalence_class_list


def create_attribute(attribute_name, attribute_description):
    new_attribute = {
        "identifier": seagent_general.generate_uuid(),  
        "name": attribute_name,  
        "description": attribute_description,
        "equivalenceClasses": []
    }
    return new_attribute

def create_attribute_list(page_name, action_name, variable_name):
    instruction = f"""
        {variable_name} 是页面{page_name}的操作（action，{action_name}）的相关变量（variable）。
        基于上面的代码，找出页面提供的与此相关变量的所有属性（attribute）。
        这些属性每个都具有独立维度（同一变量不同属性不能有等价类没有重复），业务含义不重复。
        只输出变量{variable_name}的相关属性json对象表，每个对象有两个元素：
        attribute name（如果不是中文，添加名字中文翻译）, 
        attribute description（一句话(此属性...)解释属性业务意义）。
        去掉输出内容的特殊字符，不解释结果。
    """
    attributes_string = chat_with_moonshot_partial_mode(instruction)
    # attributes_string = attributes_string.replace('"', '')
    # attributes_string = attributes_string.replace("'", "")

    # attributes_string = " list of Input user name's attributes: length"
    statement = f"在下文找出所有属性，一定用中文回答: {attributes_string}"

    attributes = chat_with_moonshot_with_input_model(statement, AttributesModel)
    if len(attributes.attribute_list) == 0: # weird situation

        att_instruction = f"""
            既然代码没有提及变量属性，那就依照名字含义（页面名称（{page_name}）、
            操作名称（{action_name}）、变量名称（{variable_name}）），
            给出一个属性。例子，对于变量用户名，比如用户名的正确性。

            只输出变量{variable_name}的相关属性json对象表，每个对象有两个元素：
            attribute name（如果不是中文，添加名字中文翻译）, 
            attribute description（一句话(此属性...)解释属性业务意义）。
        """
        created_attributes = chat_with_moonshot_with_input_model(att_instruction, AttributesModel)
        created_attribute_index = 0
        new_attribute_list = []
        for created_attribute in created_attributes.attribute_list:
            new_attribute = create_attribute(created_attribute.attribute_name, created_attribute.attribute_description)
            new_attribute_list.append(new_attribute)
        return new_attribute_list
    
    new_attribute_list = []
    for attribute in attributes.attribute_list:
        new_attribute = create_attribute(attribute.attribute_name, attribute.attribute_description)
        new_attribute_list.append(new_attribute)

    return new_attribute_list


def create_variable(action_name, variable_name, variable_description, variable_classification):
    new_variable = {
        "identifier": seagent_general.generate_uuid(),  
        "name": variable_name,  
        "description": f"{variable_description}\n 是{action_name}操作的{variable_classification}变量。"
    }

    return new_variable


def create_variable_list(page_name, action_name):
    instruction = f"""
            基于上面的代码，
            构建属于{page_name}页面的操作{action_name} （action）的函数的伪代码。

            在函数伪代码中，找出输入变量：输入变量的name、classification（输入变量）、description
            
            只输出操作{action_name}的相关变量json对象表，每个对象有三个元素：
            variable name（如果不是中文，添加名字中文翻译）, 
            variable classification（中文表达）, 
            和variable description（一句话(此变量...)解释变量业务意义）。

            不要添加不确定的变量。如果找不到，就说此操作没有输入变量。
            去掉输出内容的特殊字符，不解释结果。
        """
    instruction = f"""


        """

    variables_string = chat_with_moonshot_partial_mode(instruction)
    # variables_string = variables_string.replace('"', '')
    # variables_string = variables_string.replace("'", "")

    raw_content = f"r{repr(variables_string)}"
    # variables_string = "list of Add User's inputs are: user name, password"
    statement = "在下文找出所有变量，一定用中文回答: " + raw_content

    variables = chat_with_moonshot_with_input_model(variables_string, VariablesModel)

    if len(variables.variable_list) == 0:
        return None

    new_variables = []
    for variable in variables.variable_list:
        new_variable = create_variable(action_name, variable.variable_name, 
                                              variable.variable_description, variable.variable_classification)
        new_variables.append(new_variable)

    return new_variables

def collect_states_for_car_result():
    pass

def collect_next_cars_for_car():
    pass

def create_car_for_action_without_inputs():
    new_car = {
        "identifier": seagent_general.generate_uuid(),
        "name": "void",
        "description": "为条件为空的行动设置的CAR",
        "condition": {
            "identifier": seagent_general.generate_uuid(),
            "description": "没有输入变量。条件为空",
            "states": []
        },
        "result": {
            "identifier": seagent_general.generate_uuid(),
            "description": "",
            "states": []
        },
        "nextCar": []
    }

    return new_car



def create_car_for_action_with_inputs(page_name, action_name, statte):
    new_car = {
        "identifier": seagent_general.generate_uuid(),
        "name": "",
        "description": "",
        "condition": {
            "identifier": seagent_general.generate_uuid(),
            "description": "",
            "states": []
        },
        "result": {
            "identifier": seagent_general.generate_uuid(),
            "description": "",
            "states": []
        },
        "nextCar": []
    }
    return new_car

def create_car_for_action(page_name, action_name, state_list = None):
    if state_list is None:
        create_car_for_action_without_inputs()
    else:
        create_car_for_action_with_inputs(page_name, action_name, state_list) # state_list is a json object ["states"] = [...]

# def create_car_list(variable_list):
#     new_car_list = []
#     new_car = create_car_for_action(page_name, action_name)


def create_action(action_name, action_description):
    new_action = {
            "identifier": seagent_general.generate_uuid(),  
            "name": action_name,  
            "description": action_description,
            "variables": []
        }
    return new_action


def create_action_list(page_name):
    instruction = f"""
        基于代码，找出{page_name}页面里能确定提供的操作（action）的name、description。
        输出为一个操作json对象表，每个对象有两个元素：action name和action description。
   
        不要添加不确定的操作。如果在此页面找不到操作，就不输出任何操作（action）。

        去掉输出内容的特殊字符，不解释结果。
    """
    actions_string = chat_with_moonshot_partial_mode(instruction)

    # actions_string = actions_string.replace('"', '')
    # actions_string = actions_string.replace("'", "")

    # actions_string = "list of actions: Add User"
    statement = f"在下文找出所有操作，一定用中文回答: {actions_string}"
    print("in create_action_list")
    print(statement)

    actions = chat_with_moonshot_with_input_model(statement, ActionsModel)
    new_actions = []

    if len(actions.action_list) == 0:
        new_action = create_action("打开页面", "打开此页面")
        new_actions.append(new_action)
        new_action = create_action("关闭页面", "关闭此页面")
        new_actions.append(new_action)
        return new_actions
    
    for action in actions.action_list:
        new_action = create_action(action.action_name, action.action_description)
        new_actions.append(new_action)

    return new_actions

def variable_information_to_action_description(index, name, identifier, description):
    if index == 0: # first
        var_info = f"""

        操作相关变量部分：
        variable name: {name}
        identifier: {identifier}
        description: {description}

        """
    else:
        var_info = f"""
        variable name: {name}
        identifier: {identifier}
        description: {description}

        """

    return var_info
    
# input documents used for this is in project_messages[]
# page_spec_json is the spec json to be updated. page_spec_json content will be saved to spec file.
def add_spec_info_till_equivalence_classes(page_spec_json):

    page_name = page_spec_json["omsObject"]["name"]

    # add actions
    action_list = create_action_list(page_name)
    page_spec_json["omsObject"]["actions"] = action_list

    # add variables
    for i in range(len(action_list)):
        variable_list = create_variable_list(page_name, action_list[i]["name"])

        variable_identifier_list = []
        for x in range(variable_list):
            variable_identifier_list.append(variable_list[x]["identifier"])

        # if variable_list is empty, it means the action is like f(), no arguments.
        # we will add one CAR to the action
        if variable_list is None:
            action_list[i]["cars"] = []
            new_car = create_car_for_action_without_inputs()
            action_list[i]["cars"].append(new_car)
            action_list[i]["variables"] = variable_identifier_list
            page_spec_json["omsObject"]["actions"] =  action_list
            # return page_spec_json

        # for actions with inputs, f(x), we will process the variables.
        for j in range(len(variable_list)):

            n0 = variable_list[j]["name"]
            print(f"var name = {n0}")

            attribute_list = create_attribute_list(page_name, action_list[i]["name"], variable_list[j]["name"])
            for k in range(len(attribute_list)):

                n1 = variable_list[j]["name"]
                n2 = attribute_list[k]["name"]
                print(f"var name = {n1}, {n2}")

                equivalence_class_list = create_equivalence_class_list(page_name, action_list[i]["name"], 
                                                                       variable_list[j]["name"], attribute_list[k]["name"])
                
                if len(equivalence_class_list) == 0:
                    print("got the empty eqc")
                
                # equivalence_class_list will not be empty. If empty, we will let LLM generate some basd on common sense.
                print(f"{len(equivalence_class_list)}")
                attribute_list[k]["equivalenceClasses"] = equivalence_class_list

            # check all attributes, delete overlapping attributes and equivalence classes
            instruction = f"""
                检查属性json对象{attribute_list}，找出重复等价类，输出等价类identifier列表。
            """
            identifiers = chat_with_moonshot_output_spec_partial_mode(instruction)

            identifier_list = chat_with_moonshot_with_input_model(identifiers, DuplicatedEquivalenceClassIdentifiers)

            copy_of_attribute_list = attribute_list.copy()

            for id in identifier_list.duplidate_list:
                for att_i in range(len(copy_of_attribute_list)):

                    eqc_len = len(copy_of_attribute_list[att_i]["equivalenceClasses"])
                    for eqc_index in range(eqc_len - 1, -1, -1):
                        if id == copy_of_attribute_list[att_i]["equivalenceClasses"][eqc_index]["identifier"]:
                            del attribute_list[att_i]["equivalenceClasses"][eqc_index]

            # now variable_list is not empty, so we add it in
            variable_list[j]["attributes"] = attribute_list
            page_spec_json["omsObject"]["memberObjects"].append(variable_list[j])

            # add this variable to action's description
            var_info = variable_information_to_action_description(j, variable_list[j]["name"],
                variable_list[j]["identifier"], variable_list[j]["description"]
            )
            description = page_spec_json["omsObject"]["actions"][i]["description"]
            page_spec_json["omsObject"]["actions"][i]["description"] = f"{description}{var_info}"

    page_spec_json["omsObject"]["actions"] =  action_list

    return page_spec_json


def add_next_cars_1(oms_json_file_path):

    # load all specs
    reason = "specifications"
    add_file_content_to_output_spec_messages(oms_json_file_path, reason)

    for filename in os.listdir(oms_json_file_path):
        file_path = os.path.join(oms_json_file_path, filename)
        spec_json = seagent_file.oms_load(file_path)
        for action_index in range(len(spec_json["omsObject"]["actions"])):       
            for car_index in range(len(spec_json["omsObject"]["actions"][action_index]["cars"])):
                description = spec_json["omsObject"]["actions"][action_index]["cars"][car_index]["description"]
                car_identifier = spec_json["omsObject"]["actions"][action_index]["cars"][car_index]["identifier"]

                car_instruction = f"""
                    1. 找出identifier={car_identifier}的CAR的所在页面和CAR所属行动
                    2. 找出identifier={car_identifier}的CAR的所在页面的后续页面（操作实现跳转）
                    3. 找出identifier={car_identifier}的CAR所属行动的后续行动
                    4. 在后续行动的CAR之中，通过CAR描述（description)、语义和业务逻辑判断（而不是文件内容），
                       找出可以后续连接identifier={car_identifier}的CAR的CAR

                    只输出符合条件的后续连接CAR信息（此连接CAR所属页面，此连接CAR所属行动，CAR identifier, CAR description），
                    并在一个 JSON 对象中输出，不解释思考、过程和结果。不要添加自我想象，没有结果就说找不到后续连接CAR。

                """
                next_cars_json = chat_with_moonshot_output_spec_partial_mode(car_instruction)
                print(next_cars_json)
                cars = chat_with_moonshot_with_input_model(next_cars_json, CarListModel)
                new_nextCar = {
                    "identifier":seagent_general.generate_uuid(),
                    "name": "",
                    "description": "",
                    "cars":[]
                }
                for car in cars.car_list:
                    new_nextCar["cars"].append(car.car_identifier)
                spec_json["omsObject"]["actions"][action_index]["cars"][car_index]["nexCar"] = new_nextCar
        seagent_file.oms_save(file_path, spec_json)

        







# def add_spec_info_till_equivalence_classes_old(page_spec_json):

#     page_name = page_spec_json["omsObject"]["name"]

#     # add actions to specification
#     instruction = f"""
#         基于代码，找出{page_name}页面里能确定提供的操作（action）的name、description。
#         输出为一个json对象表，每个对象有两个元素：action name和action description。
   
#         不要添加不确定的操作。如果在此页面找不到操作，就添加下面连个操作：打开页面，关闭页面。
#         去掉输出内容的特殊字符，不解释结果
#     """
#     actions_string = chat_with_moonshot(instruction)
#     actions_string = actions_string.replace('"', '')
#     actions_string = actions_string.replace("'", "")

#     # actions_string = "list of actions: Add User"

#     actions = chat_with_llama3_with_input_model(actions_string, ActionsModel)
#     if len(actions.action_list) == 0:

#         return page_spec_json




#     for action in actions.action_list:
#         # put into spec
#         new_action = {
#             "identifier": seagent_general.generate_uuid(),  
#             "name": action.action_name,  
#             "description": action.action_description
#         }
#         page_spec_json["omsObject"]["actions"].append(new_action)
#         seagent_file.oms_save("/opt/bihua/reqgpt/seagent/spec_tmp.json", page_spec_json)

#         instruction = f"""
#             基于上面的代码，
#             构建属于{page_name}页面的操作{action.action_name} （action）的函数的伪代码。

#             在函数伪代码中，找出输入变量：输入变量的name、classification（输入变量）、description
            
#             只输出操作{action.action_name}的相关变量对象表，每个对象有三个元素：variable name,variable classification, 和variable description。

#             不要添加不确定的变量。如果找不到，就说此操作没有输入变量。
#             去掉输出内容的特殊字符，不解释结果。
#         """

#         # instruction = f"""
#         #     基于上面的代码，找出属于{page_name}页面的操作{action.action_name} （action）的所有相关变量的name、
#         #     classification（输入变量，输出变量，环境变量）、description
#         #     每个变量输出格式为一行：name, description
#         #     不要添加不确定的变量。如果找不到，就说此操作没有输入变量。
#         #     去掉输出内容的特殊字符，不解释结果。
#         # """

#         variables_string = chat_with_moonshot(instruction)
#         variables_string = variables_string.replace('"', '')
#         variables_string = variables_string.replace("'", "")

#         # variables_string = "list of Add User's inputs are: user name, password"

#         variables = chat_with_llama3_with_input_model(variables_string, VariablesModel)
#         if len(variables.variable_list) > 0:
#             for variable in variables.variable_list:
#                 for_action_description = f"相关变量："
#                 for_action_description += f"{variable.variable_name} ({variable.variable_classification}), "
#             new_action["description"] += for_action_description
#         else:
#             new_action["description"] += f"相关变量：此操作（action）没有作为条件的相关变量。"
#             return page_spec_json

#         variable_index = 0
#         for variable in variables.variable_list:
#             new_variable = {
#                 "identifier": seagent_general.generate_uuid(),  
#                 "name": variable.variable_name,  
#                 "description": f"{variable.variable_description}\n 是操作 {action.action_name}的{variable.variable_classification}变量。"
#             }
#             page_spec_json["omsObject"]["memberObjects"].append(new_variable)

#             instruction = f"""
#                 {variable.variable_name} 是页面{page_name}的操作（action，{action.action_name}）的相关变量（variable）。
#                 基于上面的代码，找出页面提供的与此相关变量的所有属性（attribute）。
#                 每个变量的输出格式为一行：变量名：属性1，属性2，...
#                 去掉输出内容的特殊字符，不解释结果。
#             """
#             # variable_index = variable_index + 1

#             attributes_string = chat_with_moonshot(instruction)
#             attributes_string = attributes_string.replace('"', '')
#             attributes_string = attributes_string.replace("'", "")

#             # attributes_string = " list of Input user name's attributes: length"

#             attributes = chat_with_llama3_with_input_model(attributes_string, AttributesModel)
#             if len(attributes.attribute_list) == 0: # weird situation, 
#                 # 依照常设，添加一个属性和等价类
#                 att_instruction = f"""
#                                     既然代码没有提及变量属性，那就依照名字含义（页面名称（{page_name}）、
#                                     操作名称（{action.action_name}）、变量名称（{variable.variable_name}）），
#                                     给出一个属性。

#                                     只输出变量{variable.variable_name}的相关属性对象表，每个对象有两个元素：attribute name, 和attribute description。
#                                   """
#                 created_attributes = chat_with_llama3_with_input_model(att_instruction, AttributesModel)
#                 created_attribute_index = 0
#                 page_spec_json["omsObject"]["memberObjects"][variable_index]["attributes"] = []
#                 for created_attribute in created_attributes.attribute_list:
#                     new_attribute = {
#                         "identifier": seagent_general.generate_uuid(),  
#                         "name": created_attribute.attribute_name,  
#                         "description": created_attribute.attribute_description,
#                         "equivalenceClasses": []
#                     }
#                     # 属性的两个等价类（一个正面有效等价类，一个无效等价类）
#                     created_eqc_instruction = f"""
#                         既然代码没有提及变量属性，那就依照名字含义（页面名称（{page_name}）、
#                         操作名称（{action.action_name}）、变量名称（{variable.variable_name}））、
#                         变量属性（{created_attribute.attribute_name}），
#                         给出此属性的等价类json对象表（此表包含一个正面有效等价类，一个无效等价类）。

#                         只输出变量{variable.variable_name}的相关属性{created_attribute.attribute_name}的等价类json对象表，
#                         每个等价类对象有两个元素：equivalence class name, 和equivalence class description。
#                     """
                    
#                     created_equivalent_classes_string = chat_with_moonshot(created_eqc_instruction)
#                     created_equivalent_classes_string = equivalent_classes_string.replace('"', '')
#                     created_equivalent_classes_string = equivalent_classes_string.replace("'", "")

#                     created_equivalent_classes = chat_with_llama3_with_input_model(created_equivalent_classes_string, EquivalenceClassesModel)
#                     created_equivalence_class_index = 0
#                     for created_equivalence_class in created_equivalent_classes.equivalence_class_list:
#                         new_equivalence_class = {
#                             "identifier": seagent_general.generate_uuid(),  
#                             "name": created_equivalence_class.equivalence_class_name,  
#                             "description": created_equivalence_class.equivalence_class_description
#                         }
#                         page_spec_json["omsObject"]["memberObjects"][variable_index]["attributes"][created_attribute_index]["equivalenceClasses"].append(new_equivalence_class)
#                         created_equivalence_class_index = created_equivalence_class_index + 1
#                     page_spec_json["omsObject"]["memberObjects"][variable_index]["attributes"].append(new_attribute)
#                     created_attribute_index = created_attribute_index + 1

#             else:
#                 attribute_index = 0
#                 for attribute in attributes.attribute_list:
#                     new_attribute = {
#                         "identifier": seagent_general.generate_uuid(),  
#                         "name": attribute.attribute_name,  
#                         "description": attribute.attribute_description
#                     }
#                     if variable_index < len(page_spec_json["omsObject"]["memberObjects"]):
#                         page_spec_json["omsObject"]["memberObjects"][variable_index]["attributes"] = []
#                     page_spec_json["omsObject"]["memberObjects"][variable_index]["attributes"].append(new_attribute)
#                     # attribute_index = attribute_index + 1

#                     instruction = f"""
#                         {variable.variable_name} 是页面{page_name}的操作（action，{action.action_name}）的相关变量（variable）。
#                         {attribute.attribute_name} 是{variable.variable_name}的一个attribute。

#                         基于上面的代码，找出 {attribute.attribute_name}  的所有等价类（有效等价类和无效等价类）。

#                         只输出变量{variable.variable_name}的相关属性{attribute.attribute_name}的等价类json对象表，
#                         每个等价类对象有两个元素：equivalence class name, 和equivalence class description。
#                     """
#                     equivalent_classes_string = chat_with_moonshot(instruction)
#                     equivalent_classes_string = equivalent_classes_string.replace('"', '')
#                     equivalent_classes_string = equivalent_classes_string.replace("'", "")

#                     # equivalent_classes_string = "list of equivalent_classes of attribute length: less than 5, between 5 abd 10, greater than 10."

# ######################
#                     equivalent_classes = chat_with_llama3_with_input_model(equivalent_classes_string, EquivalenceClassesModel)
#                     if len(equivalent_classes.equivalence_class_list) == 0:
# ###################
#                         created_eqc_instruction = f"""
#                         既然代码没有提及变量属性，那就依照名字含义（页面名称（{page_name}）、
#                         操作名称（{action.action_name}）、变量名称（{variable.variable_name}））、
#                         变量属性（{created_attribute.attribute_name}），
#                         给出此属性的等价类json对象表（此表包含一个正面有效等价类，一个无效等价类）。

#                         只输出变量{variable.variable_name}的相关属性{created_attribute.attribute_name}的等价类json对象表，
#                         每个等价类对象有两个元素：equivalence class name, 和equivalence class description。
#                     """
                    
#                     created_equivalent_classes_string = chat_with_moonshot(created_eqc_instruction)
#                     created_equivalent_classes_string = equivalent_classes_string.replace('"', '')
#                     created_equivalent_classes_string = equivalent_classes_string.replace("'", "")

#                     created_equivalent_classes = chat_with_llama3_with_input_model(created_equivalent_classes_string, EquivalenceClassesModel)
#                     created_equivalence_class_index = 0
#                     for created_equivalence_class in created_equivalent_classes.equivalence_class_list:
#                         new_equivalence_class = {
#                             "identifier": seagent_general.generate_uuid(),  
#                             "name": created_equivalence_class.equivalence_class_name,  
#                             "description": created_equivalence_class.equivalence_class_description
#                         }
#                         page_spec_json["omsObject"]["memberObjects"][variable_index]["attributes"][created_attribute_index]["equivalenceClasses"].append(new_equivalence_class)
#                         created_equivalence_class_index = created_equivalence_class_index + 1
#                     page_spec_json["omsObject"]["memberObjects"][variable_index]["attributes"].append(new_attribute)
#                     created_attribute_index = created_attribute_index + 1                      


#                         return page_spec_json

#                     equivalen_classes_i = 0
#                     for equivalence_class in equivalent_classes.equivalence_class_list:
#                         new_equivalence_class = {
#                             "identifier": seagent_general.generate_uuid(),  
#                             "name": equivalence_class.equivalence_class_name,  
#                             "description": f"{equivalence_class.equivalence_class_description}"
#                         }
#                         if attribute_index < len(page_spec_json["omsObject"]["memberObjects"][variable_index]["attributes"]):
#                             page_spec_json["omsObject"]["memberObjects"][variable_index]["attributes"][attribute_index]["equivalenceClasses"] = []
#                         page_spec_json["omsObject"]["memberObjects"][variable_index]["attributes"][attribute_index]["equivalenceClasses"].append(new_equivalence_class)

#                     equivalen_classes_i = equivalen_classes_i + 1
#                 attribute_index = attribute_index + 1
#         variable_index = variable_index + 1
#         seagent_file.oms_save("/opt/bihua/reqgpt/seagent/spec_tmp.json", page_spec_json)

#     seagent_file.oms_save("/opt/bihua/reqgpt/seagent/spec_tmp.json", page_spec_json)
#     return page_spec_json

# def process_next_car_for_one_spec(oms_spec_json):
    
#     for action_index in range(len(oms_spec_json["omsObject"]["actions"])):
        
#         for car_index in range(len(oms_spec_json["omsObject"]["actions"][action_index]["cars"])):

#             car_instruction = f""
#             next_cars_json = chat_with_moonshot(car_instruction)
#             cars = chat_with_moonshot_with_input_model(next_cars_json, model)
#             for car in cars:
#                 oms_spec_json["omsObject"]["actions"][action_index]["cars"][car_index]["nexCars"].append(car.identifier)






    
  
        







# def update_car_results(oms_json_file_path):

#     #收集所有oms specification, uoload
#     reason = "为本项目所生成的所有Specifications"
#     add_file_content_to_project_messages(oms_json_file_path, reason)

#     #上传oms schema
#     load_dotenv()
#     SPEC_SCHEMA_PATH = os.getenv("SPEC_SCHEMA_PATH")
#     # spec_schema_json = seagent_file.oms_load(SPEC_SCHEMA_PATH)
#     reason = "specification必须遵守的oms schema。"
#     add_file_content_to_project_messages(SPEC_SCHEMA_PATH, reason)

#     for filename in os.listdir(oms_json_file_path):
#         file_path = os.path.join(oms_json_file_path, filename)
#         spec_json = seagent_file.oms_load(file_path)


#         instructiono = f"""
#             基于所附文档，以及sample specification json，将相关内容填入specification： {spec_json}；只返还 specification json。
#             对于specification的每个car（car为文件特殊用语，不是车）：
#             1）找出此car的result的states，把state的identifier放到此car的result里面。
#             2）找出此car的所允许的所有next_car，把car的identifier放到此car的next_car里面。
#             3）更新此car的name和description 。
#             4）以json对象形式，返还满足oms schema的specification。

#             去掉输出内容的特殊字符。

#         """
#         # final_draft_spec = chat_with_moonshot(instructiono)
#         final_draft_spec =chat_with_moonshot_partial_mode(instructiono)
#         seagent_file.oms_save(file_path, final_draft_spec)


# def update_car_results_old(oms_json_file_path):
#     global moonshot_client
#     global project_messages

#     # Loop through all files in the directory
#     # put sample specification into this folder
#     all_spec_json_file_contents = []
#     for filename in os.listdir(oms_json_file_path):
#         file_path = os.path.join(oms_json_file_path, filename)

#         file_object = moonshot_client.files.create(file=Path(file_path), purpose="file-extract")
#         file_content = moonshot_client.files.content(file_id=file_object.id).text
#         file_content = moonshot_client.files.content()
#         all_spec_json_file_contents.append(file_content)


    # project_messages.append({"role": "system", "content": f"Specification files: {all_spec_json_file_contents}"})
    # project_messages.append({"role": "user", "content": "基于文件内容，回答我的问题。"})

    # # loop all files
    # for filename in os.listdir(oms_json_file_path):
    #     if str(filename).startswith("sample") or not str(filename).endswith(".json"):
    #         continue
    #     file_path = os.path.join(oms_json_file_path, filename)
    #     spec_json = seagent_file.oms_load(file_path)

    #     order = f"""
    #         基于所附文档，以及sample specification json，将相关内容填入specification： {spec_json}；只返还 specification json。
    #         对于specification的每个car（car为文件特殊用语，不是车）：
    #         1）找出此car的result的states，把state的identifier放到此car的result里面。
    #         2）找出此car的所允许的所有next_car，把car的identifier放到此car的next_car里面。
    #         3）更新此car的name和description 。

    #         去掉输出内容的特殊字符。

    #     """

    #     final_draft_spec = chat_with_moonshot(order)

    #     seagent_validation.validate_spec_json(final_draft_spec)

            








