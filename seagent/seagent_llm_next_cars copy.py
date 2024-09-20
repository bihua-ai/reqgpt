
import os, json, re
from dotenv import load_dotenv
import seagent_llm, seagent_file
from openai import OpenAI
import instructor, openai
from enum import Enum
import asyncio, json, os
from pydantic import BaseModel, Field
from typing import List

# next cars
class CurrentNextCarModel(BaseModel):
    car_name: str
    car_identifier: str
    action_name: str = Field(..., description="The name of the action that owns this car.")
    page_name: str = Field(..., description="The name of the page that owns the car.")
    page_path: str = Field(..., description="The path of page file.")

class CurrentNextCarListModel(BaseModel):
    current_car: CurrentNextCarModel
    next_car_list: List[CurrentNextCarModel]

# next actions
class CurrentNextActionModel(BaseModel):
    action_name: str
    action_identifier: str
    page_name: str = Field(..., description="The name of the page that owns the action.")
    page_path: str

class CurrentNextActionListModel(BaseModel):
    current_action: CurrentNextActionModel
    next_action_list: List[CurrentNextActionModel]

# next pages
class CurrentNextPageModel(BaseModel):
    page_name: str
    page_path: str

class CurrentNextPageGroupModel(BaseModel):
    current_page: CurrentNextPageModel
    next_page_list: List[CurrentNextPageModel]

class CurrentNextPageGroupListModel(BaseModel):
    page_group_list: List[CurrentNextPageGroupModel]



        


def collect_potential_next_cars_from_all_actions(next_action_list:List[CurrentNextActionModel] ):
    page_action_car_json_list = []

    number_of_next_actions = len(next_action_list)
    for i in range(number_of_next_actions):
        spec_json = seagent_file.oms_load(next_action_list[i].page_path)
        number_of_actions = len(spec_json["omsObject"]["actions"])
        for j in range(number_of_actions):
            if next_action_list[i].action_identifier == spec_json["omsObject"]["actions"][i]["identifier"]:
                element = {
                    "page_name": next_action_list[i].page_name,
                    "action_name": next_action_list[i].action_name,
                    "action_identifier": next_action_list[i].action_identifier,
                    "cars": spec_json["omsObject"]["actions"][i]["cars"],
                }
                page_action_car_json_list.append(element)
    return page_action_car_json_list
    

def collect_potential_next_action_names_from_pages(page_group: List[CurrentNextPageGroupModel]):

    page_actions_list = []

    for page in page_group.next_page_list:
        spec_json = seagent_file.oms_load(page.page_path)
        number_of_actions = len(spec_json["omsObject"]["actions"])
        for i in range(number_of_actions):
            actions = []
            actions.append(spec_json["omsObject"]["actions"][i]["name"])

        page_actions = {
            "page_name": page.name,
            "actions": actions,
        }
        page_actions_list.append(page_actions)
    return page_actions_list


def get_all_next_cars(current_car_json, current_action_name, current_page_name, next_action_list:List[CurrentNextActionModel] ):

    page_action_car_json_list = collect_potential_next_cars_from_all_actions(next_action_list)
    
    # next_action_list_json = next_action_list.json()
    next_action_list_json = []
    for next_action in next_action_list:
        next_action_json = next_action.model_dump_json()
        next_action_list_json.append(next_action_json)

    statement = f"""
    CAR是Condition-Action-Result的缩写，代表的是在Condition之下，做操作Action，会得到Result。一个CAR由一个json对象定义。 
    我们的任务是在提供的操作定义里面，找到由下面json对象定义的CAR的所有代码和需求可行的CAR。
    这是{current_page_name}里面的操作{current_action_name}的一个CAR（{repr(current_car_json)}）。

    基于代码和Specifications，在{next_action_list_json}里面，找出这个CAR后续行动的ACR的：name， identifier, description，返回一个json对象。
    """
    car_list_json = seagent_llm.chat_with_moonshot_partial_mode(statement)
    next_cars_model_CurrentNextCarListModel = seagent_llm.chat_with_moonshot_with_input_model(car_list_json, CurrentNextCarListModel)
    return next_cars_model_CurrentNextCarListModel
 
def get_all_next_actions(current_action_name, current_page_name, next_page_list:List[CurrentNextPageModel] ):
    page_next_actions_list_json = collect_potential_next_action_names_from_pages(next_page_list)
    # get all action names, ask llm which one are the 
    all_next_pages = ""
    for page in next_page_list:
        all_next_pages = all_next_pages + page.page_name + "、"
    all_next_pages = all_next_pages.rstrip("、")

    statement = f"""
    这些是{current_page_name}里面的操作{current_action_name}之后会进入的下面包含操作的页面：{repr(page_next_actions_list_json)}
    根据附件代码，在Specifications中，依照模型，找出这些后续页面里，操作{current_action_name}之后可以进行的操作，比如，登录操作成功后，可以选择商品。

    在Specifications里面，找出这些后续行动的：name， identifier, description，返回一个json对象。
    """
    action_list_json = seagent_llm.chat_with_moonshot_partial_mode(statement)
    next_actions_model_CurrentNextActionListModel = seagent_llm.chat_with_moonshot_with_input_model(action_list_json, CurrentNextActionListModel)
    return next_actions_model_CurrentNextActionListModel

def all_curent_next_pages_NextPageGroupListModel(specifications_path):
    pages = []
    page_name_list = ""
    for filename in os.listdir(specifications_path):
        spec_json_full_path = os.path.join(specifications_path, filename)
        spec_json = seagent_file.oms_load(spec_json_full_path)
        pase_name = spec_json["omsObject"]["name"]     
        page_name_list = page_name_list + " " + pase_name
        new_page = {
            "page_name": pase_name,
            "page_path": spec_json_full_path,
        }
        pages.append(new_page)

    statement = f"""
    下面是一个表， 表单每个元素是一个页面和页面文件路径： {repr(pages)}。
    根据附件代码和Specifications，依照模型，将这些页面之间的关系内容梳理清楚：
    页面关系例子：个人首页页面的下游页面（next pages）是购买页面和退货页面。
    给出每个页面以及所有后续页面。每个页面的信息包括：名字，页面文件路径。返回一个json对象。
    """
    page_list_json = seagent_llm.chat_with_moonshot_partial_mode(statement)
    page_model = seagent_llm.chat_with_moonshot_with_input_model(page_list_json, CurrentNextPageGroupListModel)
    return page_model

def add_next_cars_to_all_cars_in_all_specs_in_folder(user_id, project_name):
    # reset the moonshot llm
    seagent_llm.start_moonshot()
    load_dotenv()
    APP_DATA_HOME = os.getenv("APP_DATA_HOME")
    SPEC_SUB_DIRECTORY = os.getenv("SPEC_SUB_DIRECTORY")
    INPUT_DOCUMENT_SUB_DIRECTORY = os.getenv("INPUT_DOCUMENT_SUB_DIRECTORY")

    # load input documents
    input_document_path = os.path.join(APP_DATA_HOME, user_id, project_name, INPUT_DOCUMENT_SUB_DIRECTORY)
    seagent_llm.add_file_content_to_project_messages(input_document_path, document_purpose="requirements")
    specifications_path = os.path.join(APP_DATA_HOME, user_id, project_name, SPEC_SUB_DIRECTORY)
    seagent_llm.add_file_content_to_project_messages(specifications_path, document_purpose="specifications")

    # iterate all pages in the folder
    all_page_groups_CurrentNextPageGroupListModel = all_curent_next_pages_NextPageGroupListModel(specifications_path)

    for page_group in all_page_groups_CurrentNextPageGroupListModel.page_group_list:
        current_page_json = seagent_file.oms_load(page_group.current_page.page_path)
       
        number_of_actions_in_current_page = len(current_page_json["omsObject"]["actions"])
        for i in range(number_of_actions_in_current_page):
            current_action = current_page_json["omsObject"]["actions"][i]

            all_action_groups_CurrentNextActionListModel = get_all_next_actions(current_action["name"], 
                                                                                page_group.current_page.page_name, 
                                                                                page_group.next_page_list)
            
            number_of_next_actions = len(all_action_groups_CurrentNextActionListModel.next_action_list)
            for j in range(number_of_next_actions):
                number_of_cars = len(current_page_json["omsObject"]["actions"][i]["cars"])
                action_name = current_action["name"]
                status = f"{action_name} {number_of_cars}"
                print(status)

                if number_of_cars == 0:
                    continue
                current_car = current_page_json["omsObject"]["actions"][i]["cars"][j]
                # prepare next cars
                car_json_list = []
                for i in range(number_of_cars):
                    all_car_groups_CurrentNextActionListModel = get_all_next_cars(current_car, current_action["name"], page_group.current_page.page_name, 
                                                                                all_action_groups_CurrentNextActionListModel.next_action_list)
                
                for car in all_car_groups_CurrentNextActionListModel.next_car_list:
                    current_page_json["omsObject"]["actions"][i]["cars"][j].append(car.car_identifier)

        seagent_file.oms_save(page_group.current_page.page_path, current_page_json)

add_next_cars_to_all_cars_in_all_specs_in_folder("eric", "bookstore")
 







