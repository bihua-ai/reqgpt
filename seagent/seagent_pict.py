import instructor, openai
from enum import Enum
import asyncio
from pydantic import BaseModel, Field
from typing import List
import pypict.cmd
import seagent_llm, seagent_specs, seagent_file, seagent_general
import json
import itertools

# https://github.com/kmaehashi/pypict/blob/master/example/example.model

# pip install pypict

# Without {P1, P2, P3} @1, it is {P1, P2, P3} @2 -- pairwise


################INPUT####################
# OS: Windows, Ubuntu
# CPU: Intel, AMD
# DBMS: PostgreSQL, MySQL
# JavaVersion: 18, 19, 20
# DotNetVersion: 4.8, 4.8.1


#################OUTPUT##################
# OS          CPU     DBMS        JavaVersion     DotNetVersion
# Windows     AMD     PostgreSQL  18              4.8
# Windows     Intel   MySQL       20              4.8.1
# Ubuntu      Intel   PostgreSQL  19              4.8.1
# Ubuntu      AMD     MySQL       20              4.8
# Windows     AMD     MySQL       19              4.8
# Ubuntu      AMD     MySQL       18              4.8.1
# Windows     Intel   MySQL       18              4.8
# Ubuntu      Intel   PostgreSQL  20              4.8

# ['test#=12', 'DBMS', 'JavaVersion', 'DotNetVersion'], 
# [['Intel', 'PostgreSQL', '18', '4.8.1'], 
#  ['Intel', 'MySQL', '20', '4.8'], 
#  ['AMD', 'MySQL', '20', '4.8.1'], 
#  ['AMD', 'PostgreSQL', '20', '4.8'], 
#  ['Intel', 'PostgreSQL', '19', '4.8.1'], 
#  ['AMD', 'MySQL', '19', '4.8'], 
#  ['AMD', 'MySQL', '18', '4.8']]

# # PICT OUTPUT
# [
#     {
#         "OS": "Windows",
#         "CPU": "AMD",
#         "DBMS": "PostgreSQL",
#         "JavaVersion": "18",
#         "DotNetVersion": "4.8"
#     },
#     {
#         "OS": "Windows",
#         "CPU": "Intel",
#         "DBMS": "MySQL",
#         "JavaVersion": "20",
#         "DotNetVersion": "4.8.1"
#     },
#     ...
# ]

class VariableStateModel(BaseModel):
    Variable_identifier: str
    state_identifier_list: List[str] = []

class VariableStatesModel(BaseModel):
    variable_list: List[VariableStateModel] = []

class VariableModel(BaseModel):
    variable_name: str = Field(..., description="The name of the variable used by a specific action. It can be a variable of input, output or environment.")
    variable_identifier: str = Field(..., description="The identifier of this variable used by a specific action. It can be a variable of input, output or environment.")
    variable_description: str = Field(..., description="A detailed description of the variable used by a specific action.")
    variable_classification: str = Field(..., description="The classification of the variable, such as input, output, or environmental.")

class VariablesModel(BaseModel):
    variable_list: List[VariableModel] = Field(default_factory=list, description="A list of all variables used by a specific action.")


def convert_pict_output_to_json(pict_output):
    headers = pict_output[0]
    rows = pict_output[1]
    data = []
    for row in rows:
        data_dict = {headers[i]: row[i] for i in range(len(row))}
        data.append(data_dict)

    # Convert the list of dictionaries to a JSON string
    json_output = json.dumps(data, indent=4)
    return json_output

def replace_identifiers(new_state_with_identifiers, identifier_dictionary):
    for key, value in identifier_dictionary.items():
        # Replace the first occurrence of the key and update the string
        new_state_with_identifiers = str(new_state_with_identifiers).replace(key, value)
        # new_state_with_identifiers = new_state_with_identifiers.replace(key, value)
    
    return new_state_with_identifiers


def calculate_states_using_pict(page_spec_json):

    # if there are no variables at all, this can happen - there are only functions without input variables
    # just return, do nothing.
    number_of_variables = len(page_spec_json["omsObject"]["memberObjects"])
    if number_of_variables == 0:
        return page_spec_json

    # for each variable
    for i in range(len(page_spec_json["omsObject"]["memberObjects"])):

        # variable must have attributes, so we can proceed.
        identifier_dictionary = {}
        page_spec_json["omsObject"]["memberObjects"][i]["states"] = []
        # new_state = {
        #     "identifier": seagent_general.generate_uuid(),
        #     "name": "", 
        #     "attributeAndEquivalenceClasses": []
        # }
        pict_input_text = ""
        for j in range(len(page_spec_json["omsObject"]["memberObjects"][i]["attributes"])):
            attribute_identifier = page_spec_json["omsObject"]["memberObjects"][i]["attributes"][j]["identifier"]
            attribute_name = page_spec_json["omsObject"]["memberObjects"][i]["attributes"][j]["name"]
            identifier_dictionary[attribute_identifier] = attribute_name

            if len(page_spec_json["omsObject"]["memberObjects"][i]["attributes"][j]["equivalenceClasses"]) == 0:
                continue

            line = f"{attribute_identifier}:    "
            for k in range(len(page_spec_json["omsObject"]["memberObjects"][i]["attributes"][j]["equivalenceClasses"])):
                equivalence_class_id = page_spec_json["omsObject"]["memberObjects"][i]["attributes"][j]["equivalenceClasses"][k]["identifier"]
                equivalence_class_name = page_spec_json["omsObject"]["memberObjects"][i]["attributes"][j]["equivalenceClasses"][k]["name"]
                identifier_dictionary[equivalence_class_id] = equivalence_class_name

                line += f"{equivalence_class_id}, "
            line = line.rstrip(', ')
            pict_input_text += f"{line}\n"
        pict_input_text = pict_input_text.rstrip('\n')
        print("PICT:")
        print(pict_input_text)
        if len(pict_input_text) < 64:
            continue
        output = pypict.cmd.from_model(pict_input_text)
        # id-att          att     DBMS        JavaVersion     DotNetVersion
        # id-eq           eqc     PostgreSQL  18              4.8

        json_string = convert_pict_output_to_json(output)
        pict_json = json.loads(json_string)

        print("in pict states")
        print(len(pict_json))

        for m, dictionary in enumerate(pict_json):
            if m > 50:
                print("number of states is too high. use condition to reduce it.")
                break
            print(f"Dictionary {m}:")
            new_state = {
                "identifier": seagent_general.generate_uuid(),
                "name": "",
                "attributeAndEquivalenceClasses": []
            }
            # Iterate over each key-value pair in the dictionary
            for attribute_key, equivalence_class_value in dictionary.items():
                # print(f"  Key: {k}, Value: {v}")
                attributeAndEquivalenceClass = {
                                "attributeId": attribute_key,
                                "equivalenceClassId": equivalence_class_value
                            }
                new_state["attributeAndEquivalenceClasses"].append(attributeAndEquivalenceClass)

            new_state_copy = new_state
            new_state_with_names = replace_identifiers(new_state_copy, identifier_dictionary)

            variable_name_with_description = page_spec_json["omsObject"]["memberObjects"][i]["name"] + "(" + page_spec_json["omsObject"]["memberObjects"][i]["description"] + ")"
            instruction = f"下面json定义变量{variable_name_with_description}的一个状态，用中文给状态起个简短状态名(不多于20个字），不解释结果：{new_state_with_names}"
            description = seagent_llm.chat_with_moonshot_without_history(instruction)
            new_state["name"] = description
            page_spec_json["omsObject"]["memberObjects"][i]["states"].append(new_state)
            #done, one object
    return page_spec_json


def get_variable_list_for_action_car(spec_json, action_identifier):
    number_of_actions = len(spec_json["omsObject"]["actions"])
    for i in range(number_of_actions):
        if spec_json["omsObject"]["actions"][i]["identifier"] == action_identifier:
            return spec_json["omsObject"]["actions"][i]["variables"]
    return None

def calculate_cars_using_pict(page_spec_json):
    # variable_attribute_equivalence_class["attribute_description"] = page_spec_json["omsObject"]["memberObjects"][j]["attributes"][att_index]["description"]

    # for each action...if there is no action ( len = 0 ), it will not
    # get into the loop, just return the iput: page_spec_json
    page_name = page_spec_json["omsObject"]["name"]

    for i in range(len(page_spec_json["omsObject"]["actions"])):
        
        # install ["cars"] section
        page_spec_json["omsObject"]["actions"][i]["cars"] = []

        # action_car_description = {
        #     "action_name": "",
        #     "action_description": "",
        #     "car": {
        #         "car_name": "",
        #         "car_description": "",
        #         "condition": "",
        #         "state_descriptions": []
        #     }
        # }

        action_description = page_spec_json["omsObject"]["actions"][i]["description"]

        # if "相关变量部分" not in action_description:
        #     # this action does not have variables, we had added a default car, 
        #     # so skip this action, move on to other actions
        #     continue

        instruction = f"""
            从下面找出所有相关变量：
            {action_description}
        """
        condition_variable_list = seagent_llm.chat_with_moonshot_with_input_model(instruction, VariablesModel)
        action_identifier = page_spec_json["omsObject"]["actions"][i]["identifier"]
        condition_variable_id_list = get_variable_list_for_action_car(page_spec_json, action_identifier)
        condition_variable_list = []
        for x in range(len(condition_variable_id_list)):
                for y in range(len(page_spec_json["omsObject"]["memberObjects"])):
                    if condition_variable_id_list[x] == page_spec_json["omsObject"]["memberObjects"][y]["identifier"]:
                        condition_variable_list.append(page_spec_json["omsObject"]["memberObjects"][y])
                        break

        if len(condition_variable_list) == 0:
            continue # just in case the check failed

        # collect description
        state_description_list = []
 
        variable_states_list = []
        var_list = ""
        for var_index in range(len(condition_variable_list)):
            print(condition_variable_list)
            variable = condition_variable_list[var_index]
            
            for j in range(len(page_spec_json["omsObject"]["memberObjects"])):
                if page_spec_json["omsObject"]["memberObjects"][j]["identifier"] == variable["identifier"]:
                    variable_states = {
                        "variable_name": "",
                        "variable_identifier": "",
                        "variable_description": "",
                        "states": []
                    }
                    variable_states["variable_name"] = page_spec_json["omsObject"]["memberObjects"][j]["name"] = variable["name"]
                    variable_states["variable_identifier"] = page_spec_json["omsObject"]["memberObjects"][j]["identifier"] = variable["identifier"]
                    variable_states["variable_description"] = page_spec_json["omsObject"]["memberObjects"][j]["description"] = variable["description"]
                    variable_tmp = variable["name"]
                    var_list = var_list + f"{variable_tmp}, "

                    # collect descriptions        
                    for k in range(len(page_spec_json["omsObject"]["memberObjects"][j]["states"])):
                        state_item = {
                            "state_name":"",
                            "state_identifier": "",

                        }
                        state_item["state_name"] = page_spec_json["omsObject"]["memberObjects"][j]["states"][k]["name"]
                        state_item["state_identifier"] = page_spec_json["omsObject"]["memberObjects"][j]["states"][k]["identifier"]

                        state_description = {
                            "state_description": "",
                            "attributeAndEquivalenceClasses": []
                        }
                        state_description["state_description"] = page_spec_json["omsObject"]["memberObjects"][j]["states"][k]["name"]
                        att_len = len(page_spec_json["omsObject"]["memberObjects"][j]["attributes"])
                        print(att_len)
                        for att_index in range(att_len -1, -1, -1):
                            attributeId = page_spec_json["omsObject"]["memberObjects"][j]["states"][k]["attributeAndEquivalenceClasses"][att_index]["attributeId"]
                            if attributeId == page_spec_json["omsObject"]["memberObjects"][j]["attributes"][att_index]["identifier"]:                                    
                                eqc_len = len(page_spec_json["omsObject"]["memberObjects"][j]["attributes"][att_index]["equivalenceClasses"])
                                equivalenceClassId = page_spec_json["omsObject"]["memberObjects"][j]["states"][k]["attributeAndEquivalenceClasses"][att_index]["equivalenceClassId"]

                                for eqc_index in range(eqc_len -1, -1, -1):
                                    if equivalenceClassId == page_spec_json["omsObject"]["memberObjects"][j]["attributes"][att_index]["equivalenceClasses"][eqc_index]["identifier"]:
                                        variable_attribute_equivalence_class = {
                                            "variable_name": "",
                                            "variable_description": "",
                                            "attribute_description": "",
                                            "equivalence_class_description": ""
                                        }
                                        variable_attribute_equivalence_class["equivalence_class_description"] = page_spec_json["omsObject"]["memberObjects"][j]["attributes"][att_index]["equivalenceClasses"][eqc_index]["description"]
                                        variable_attribute_equivalence_class["variable_name"] = variable["name"]
                                        variable_attribute_equivalence_class["variable_description"] = variable["description"]
                                        variable_attribute_equivalence_class["attribute_description"] = page_spec_json["omsObject"]["memberObjects"][j]["attributes"][att_index]["description"]

                                        state_description["attributeAndEquivalenceClasses"].append(variable_attribute_equivalence_class)                    
                        state_description_list.append(state_description)  


                        variable_states["states"].append(state_item)
                    variable_states_list.append(variable_states)

        # now, we have built variable_states_list. next, build input for pict
        identifier_dictionary = {}
        pict_input_text = ""
        for m in range(len(variable_states_list)):
            temp_str = variable_states_list[m]["variable_identifier"]
            identifier_dictionary[temp_str] = variable_states_list[m]["variable_name"]
            line = f"{temp_str}:    "
            for n in range(len(variable_states_list[m]["states"])):
                temp_str1 = variable_states_list[m]["states"][n]["state_identifier"]
                temp_str2 = variable_states_list[m]["states"][n]["state_name"]
                line += f"{temp_str1}, "
                identifier_dictionary[temp_str1] = temp_str2
            line = line.rstrip(', ')
            pict_input_text += f"{line}\n"
        pict_input_text = pict_input_text.rstrip('\n')
        if len(pict_input_text) < 64:
            return page_spec_json
        output = pypict.cmd.from_model(pict_input_text)
        # id-OS          CPU     DBMS        JavaVersion     DotNetVersion
        # id-Windows     AMD     PostgreSQL  18              4.8

        json_string = convert_pict_output_to_json(output)
        pict_json = json.loads(json_string)

        page_spec_json["omsObject"]["actions"][i]["cars"] = []
        
        for m, dictionary in enumerate(pict_json):
            if m > 50:
                print("number if cars created is too high. use conditions to reduce it.")
                break
            print(f"Dictionary {m}:")
            new_car = {
                        "identifier": seagent_general.generate_uuid(),
                        "name": "",
                        "description": "",
                        "condition": {
                            "identifier": seagent_general.generate_uuid(),
                            "states": []
                        },
                        "result": {
                            "identifier": seagent_general.generate_uuid(),
                            "states": []
                        },
                        "nextCar": []
                    }
            
            # collect description
            new_action_car_description = {
                "action_name": "",
                "action_description": "",
                "car_name": "",
                "car_description": "",
                "condition_description": "",
                "state_descriptions": []
            }
            
            # Iterate over each key-value pair in the dictionary
            condition_states_names = []
            for variable_key, state_value in dictionary.items():
                # print(f"  Key: {k}, Value: {v}")
                condition = {
                                "identifier": seagent_general.generate_uuid(),
                                "description": "",
                                "states": []
                            }
                condition["states"].append(state_value)

                variable_state_pair = {
                    "variable_name": "",
                    "state_name": ""
                }
                variable_state_pair["variable_name"] = variable_key
                variable_state_pair["state_name"] = state_value
                condition_states_names.append(variable_state_pair)
                
            condition_states_names = replace_identifiers(condition_states_names, identifier_dictionary)
            action_name = page_spec_json["omsObject"]["actions"][i]["name"]
            instruction = f"下面json定义操作{action_name}的一个条件，用中文一句话（此条件...）给状态起个简短条件名(条件名必须不多于20个字），不解释结果：{condition_states_names}"
            description = seagent_llm.chat_with_moonshot_without_history(instruction)
            condition["description"] = description
            new_car["condition"] = condition
            new_car["name"] = f"场景{m+1}"

            # collect description
            new_action_car_description["action_name"] =  page_spec_json["omsObject"]["actions"][i]["name"]
            new_action_car_description["action_description"] =  page_spec_json["omsObject"]["actions"][i]["description"]
            new_action_car_description["car_name"] = new_car["name"]
            new_action_car_description["condition_description"] = description
            new_action_car_description["state_descriptions"] = state_description_list


            # process resulf for this car
            result = {
                "identifier": seagent_general.generate_uuid(),
                "description": "",
                "states": []
            }
            # calculate action's output
            result_instruction = f"""
                已有信息： 页面是{page_name}，此页面内要考虑的操作是{action_name}。{action_name}操作的输入变量是：{var_list}。
                一个CAR（缩写，Condition-Action-Result）代表一个特定操作条件和操作结果，定义在在此json对象中：{new_action_car_description}。

                基于上面的代码和已有信息， 以函数方式，构建此特定场景的{action_name}操作的伪代码。用变量方式表达操作函数的输出和操作影响结果列表。

                用一段中文自然语言总结描述输出和操作影响结果列表。不列要点，写一个段落。必须只输出此描述（不包括伪代码等，不解释结果。
                不要添加不确定的变量。如果找不到相关信息，就说找不到操作结果。
            """

            result_description = seagent_llm.chat_with_moonshot(result_instruction)

            result["description"] = result_description

            new_car["result"] = result

            car_instruction = f"""下面json定义操作{action_name}的一个CAR(条件-操作-结果，不是汽车），
                                用自然语言中文（此场景...）总结json内容，不解释结果：{new_action_car_description}
            """
            car_description = seagent_llm.chat_with_moonshot_without_history(car_instruction)
                    
            new_action_car_description["car_description"] = car_description

            print("car description")
            print(new_action_car_description)

            new_car["description"] = car_description
            page_spec_json["omsObject"]["actions"][i]["cars"].append(new_car)

    return page_spec_json



####################################################################################
def old_oms_calculate_car_without_ai_for_one_action_old(page_spec_json, action_identifier, variable_list):
    # variable_attribute_equivalence_class["attribute_description"] = page_spec_json["omsObject"]["memberObjects"][j]["attributes"][att_index]["description"]

    # for each action...if there is no action ( len = 0 ), it will not
    # get into the loop, just return the iput: page_spec_json
    page_name = page_spec_json["omsObject"]["name"]

    for i in range(len(page_spec_json["omsObject"]["actions"])):

        ########add this to filter out action_identifier#############
        if page_spec_json["omsObject"]["actions"][i]["identifier"] != action_identifier:
            continue
        #############################################################

        # install ["cars"] section
        page_spec_json["omsObject"]["actions"][i]["cars"] = []

        # action_car_description = {
        #     "action_name": "",
        #     "action_description": "",
        #     "car": {
        #         "car_name": "",
        #         "car_description": "",
        #         "condition": "",
        #         "state_descriptions": []
        #     }
        # }

        # action_description = page_spec_json["omsObject"]["actions"][i]["description"]

        # if "相关变量部分" not in action_description:
        #     # this action does not have variables, we had added a default car, 
        #     # so skip this action, move on to other actions
        #     continue

        #################################replace the following#################
        # instruction = f"""
        #     从下面找出所有相关变量：
        #     {action_description}
        # """
        # condition_variable_list = seagent_llm.chat_with_moonshot_with_input_model(instruction, VariablesModel)
        # if len(condition_variable_list.variable_list) == 0:
        #     continue # just in case the check failed
        ########################################################################
        # action_variables = page_spec_json["omsObject"]["actions"][i]["variables"]
        # if len(action_variables) == 0:
        #     continue # nothing to do

        # if len(variable_list) == 0:
        #     condition_variable_list = action_variables
        # else:
        #     condition_variable_list = variable_list

        condition_variable_list = variable_list
        # now we are sure condition_variable_list is not empty

        # collect description
        state_description_list = []
 
        variable_states_list = []
        var_list = ""
        for variable in condition_variable_list:
            
            for j in range(len(page_spec_json["omsObject"]["memberObjects"])):
                if page_spec_json["omsObject"]["memberObjects"][j]["identifier"] == variable.variable_identifier:


                    variable_states = {
                        "variable_name": "",
                        "variable_identifier": "",
                        "variable_description": "",
                        "states": []
                    }
                    variable_states["variable_name"] = page_spec_json["omsObject"]["memberObjects"][j]["name"]
                    variable_states["variable_identifier"] = page_spec_json["omsObject"]["memberObjects"][j]["identifier"]
                    variable_states["variable_description"] = page_spec_json["omsObject"]["memberObjects"][j]["description"]


                    var_list = var_list + f"{variable.variable_name}, "

                    # collect descriptions        
                    for k in range(len(page_spec_json["omsObject"]["memberObjects"][j]["states"])):
                        state_item = {
                            "state_name":"",
                            "state_identifier": "",

                        }
                        state_item["state_name"] = page_spec_json["omsObject"]["memberObjects"][j]["states"][k]["name"]
                        state_item["state_identifier"] = page_spec_json["omsObject"]["memberObjects"][j]["states"][k]["identifier"]

                        state_description = {
                            "state_description": "",
                            "attributeAndEquivalenceClasses": []
                        }
                        state_description["state_description"] = page_spec_json["omsObject"]["memberObjects"][j]["states"][k]["name"]
                        att_len = len(page_spec_json["omsObject"]["memberObjects"][j]["attributes"])
                        for att_index in range(att_len -1, -1, -1):
                            attributeId = page_spec_json["omsObject"]["memberObjects"][j]["states"][k]["attributeAndEquivalenceClasses"][att_index]["attributeId"]
                            if attributeId == page_spec_json["omsObject"]["memberObjects"][j]["attributes"][att_index]["identifier"]:                                    
                                eqc_len = len(page_spec_json["omsObject"]["memberObjects"][j]["attributes"][att_index]["equivalenceClasses"])
                                equivalenceClassId = page_spec_json["omsObject"]["memberObjects"][j]["states"][k]["attributeAndEquivalenceClasses"][att_index]["equivalenceClassId"]

                                for eqc_index in range(eqc_len -1, -1, -1):
                                    if equivalenceClassId == page_spec_json["omsObject"]["memberObjects"][j]["attributes"][att_index]["equivalenceClasses"][eqc_index]["identifier"]:
                                        variable_attribute_equivalence_class = {
                                            "variable_name": "",
                                            "variable_description": "",
                                            "attribute_description": "",
                                            "equivalence_class_description": ""
                                        }
                                        variable_attribute_equivalence_class["equivalence_class_description"] = page_spec_json["omsObject"]["memberObjects"][j]["attributes"][att_index]["equivalenceClasses"][eqc_index]["description"]
                                        variable_attribute_equivalence_class["variable_name"] = variable.variable_name
                                        variable_attribute_equivalence_class["variable_description"] = variable.variable_description
                                        variable_attribute_equivalence_class["attribute_description"] = page_spec_json["omsObject"]["memberObjects"][j]["attributes"][att_index]["description"]

                                        state_description["attributeAndEquivalenceClasses"].append(variable_attribute_equivalence_class)                    
                        state_description_list.append(state_description)  


                        variable_states["states"].append(state_item)
                    variable_states_list.append(variable_states)

        # now, we have built variable_states_list. next, build input for pict
        identifier_dictionary = {}
        pict_input_text = ""
        for m in range(len(variable_states_list)):
            temp_str = variable_states_list[m]["variable_identifier"]
            identifier_dictionary[temp_str] = variable_states_list[m]["variable_name"]
            line = f"{temp_str}:    "
            for n in range(len(variable_states_list[m]["states"])):
                temp_str1 = variable_states_list[m]["states"][n]["state_identifier"]
                temp_str2 = variable_states_list[m]["states"][n]["state_name"]
                line += f"{temp_str1}, "
                identifier_dictionary[temp_str1] = temp_str2
            line = line.rstrip(', ')
            pict_input_text += f"{line}\n"
        pict_input_text = pict_input_text.rstrip('\n')
        if len(pict_input_text) < 64:
            return page_spec_json
        output = pypict.cmd.from_model(pict_input_text)
        # id-OS          CPU     DBMS        JavaVersion     DotNetVersion
        # id-Windows     AMD     PostgreSQL  18              4.8

        json_string = convert_pict_output_to_json(output)
        pict_json = json.loads(json_string)

        page_spec_json["omsObject"]["actions"][i]["cars"] = []
        
        for m, dictionary in enumerate(pict_json):
            if m > 5:
                break
            print(f"Dictionary {m}:")
            new_car = {
                        "identifier": seagent_general.generate_uuid(),
                        "name": "",
                        "description": "",
                        "condition": {
                            "identifier": seagent_general.generate_uuid(),
                            "states": []
                        },
                        "result": {
                            "identifier": seagent_general.generate_uuid(),
                            "states": []
                        },
                        "nextCar": []
                    }
            
            # collect description
            new_action_car_description = {
                "action_name": "",
                "action_description": "",
                "car_name": "",
                "car_description": "",
                "condition_description": "",
                "state_descriptions": []
            }
            
            # Iterate over each key-value pair in the dictionary
            condition_states_names = []
            for variable_key, state_value in dictionary.items():
                # print(f"  Key: {k}, Value: {v}")
                condition = {
                                "identifier": seagent_general.generate_uuid(),
                                "description": "",
                                "states": []
                            }
                condition["states"].append(state_value)

                variable_state_pair = {
                    "variable_name": "",
                    "state_name": ""
                }
                variable_state_pair["variable_name"] = variable_key
                variable_state_pair["state_name"] = state_value
                condition_states_names.append(variable_state_pair)
                
            condition_states_names = replace_identifiers(condition_states_names, identifier_dictionary)
            action_name = page_spec_json["omsObject"]["actions"][i]["name"]
            # instruction = f"下面json定义操作{action_name}的一个条件，用中文一句话（此条件...）给状态起个简短条件名(不多于20个字），不解释结果：{condition_states_names}"
            # description = seagent_llm.chat_with_moonshot_without_history(instruction)
            # condition["description"] = description
            new_car["condition"] = condition
            new_car["name"] = f"场景{m+1}"

            # collect description
            new_action_car_description["action_name"] =  page_spec_json["omsObject"]["actions"][i]["name"]
            new_action_car_description["action_description"] =  page_spec_json["omsObject"]["actions"][i]["description"]
            new_action_car_description["car_name"] = new_car["name"]
            new_action_car_description["condition_description"] = ""
            new_action_car_description["state_descriptions"] = state_description_list


            # process resulf for this car
            result = {
                "identifier": seagent_general.generate_uuid(),
                "description": "",
                "states": []
            }
            # calculate action's output
            # result_instruction = f"""
            #     已有信息： 页面是{page_name}，此页面内要考虑的操作是{action_name}。{action_name}操作的输入变量是：{var_list}。
            #     一个CAR（缩写，Condition-Action-Result）代表一个特定操作条件和操作结果，定义在在此json对象中：{new_action_car_description}。

            #     基于上面的代码和已有信息， 以函数方式，构建此特定场景的{action_name}操作的伪代码。用变量方式表达操作函数的输出和操作影响结果列表。

            #     用一段中文自然语言总结描述输出和操作影响结果列表。不列要点，写一个段落。必须只输出此描述（不包括伪代码等，不解释结果。
            #     不要添加不确定的变量。如果找不到相关信息，就说找不到操作结果。
            # """

            # result_description = seagent_llm.chat_with_moonshot(result_instruction)

            result["description"] = ""

            new_car["result"] = result

            # car_instruction = f"""下面json定义操作{action_name}的一个CAR(条件-操作-结果，不是汽车），
            #                     用自然语言中文（此场景...）总结json内容，不解释结果：{new_action_car_description}
            # """
            # car_description = seagent_llm.chat_with_moonshot_without_history(car_instruction)
                    
            # new_action_car_description["car_description"] = "CAR描述"

            print("car description")
            print(new_action_car_description)

            new_car["description"] = "CAR描述"
            page_spec_json["omsObject"]["actions"][i]["cars"].append(new_car)

    return page_spec_json



def oms_calculate_car_without_ai_for_one_action(page_spec_json, action_identifier, variable_list):

    # find the action that needs the car table
    action_index = -1
    for i in range(len(page_spec_json["omsObject"]["actions"])):
        if page_spec_json["omsObject"]["actions"][i]["identifier"] == action_identifier:
            action_index = i
            break
    # initialise the cars, clear it.
    page_spec_json["omsObject"]["actions"][action_index]["cars"] = []


    # collect variable_states_list
    number_of_variable_identifiers = len(variable_list)
    variable_states_list = []
    for i in range(number_of_variable_identifiers):
        number_of_oms_variables = len(page_spec_json["omsObject"]["memberObjects"])
        for j in range(number_of_oms_variables):
            if variable_list[i] == page_spec_json["omsObject"]["memberObjects"][j]["identifier"]:
                variable_states_list.append(page_spec_json["omsObject"]["memberObjects"][j])
                break


    # use pict to calculate condition list
    identifier_dictionary = {}
    # pict_input_text = ""
    # for m in range(len(variable_states_list)):
    #     temp_str = variable_states_list[m]["identifier"]
    #     line = f"{temp_str}:    "
    #     for n in range(len(variable_states_list[m]["states"])):
    #         temp_str1 = variable_states_list[m]["states"][n]["identifier"]
    #         line += f"{temp_str1}, "
    #     line = line.rstrip(', ')
    #     pict_input_text += f"{line}\n"
    # pict_input_text = pict_input_text.rstrip('\n')
    pict_input_text = ""

    for variable_state in variable_states_list:
        temp_str = variable_state["identifier"]
        line = f"{temp_str}:    "
        
        # Collect all state identifiers in a list
        states = [state["identifier"] for state in variable_state["states"]]

        if len(states) == 0:
            continue
        
        # Join them with ', ' and append to the line
        line += ", ".join(states)
        
        # Append the line to the result with a newline
        pict_input_text += f"{line}\n"

    # Remove the last newline
    pict_input_text = pict_input_text.rstrip('\n')

    ############

    
    if len(pict_input_text) < 64:
        return page_spec_json
    output = pypict.cmd.from_model(pict_input_text)
    # id-OS          CPU     DBMS        JavaVersion     DotNetVersion
    # id-Windows     AMD     PostgreSQL  18              4.8

    json_string = convert_pict_output_to_json(output)
    pict_json = json.loads(json_string)
        
    # build car
    for m, dictionary in enumerate(pict_json):
        # if m > 5:
        #     break
        # print(f"Dictionary {m}:")
        new_car = {
            "identifier": seagent_general.generate_uuid(),
            "name": "",
            "description": "",
            "condition": {
                "identifier": seagent_general.generate_uuid(),
                "states": []
            },
            "result": {
                "identifier": seagent_general.generate_uuid(),
                "states": []
            },
            "nextCar": []
        }
        
        # Iterate over each key-value pair in the dictionary
        condition = {
            "identifier": seagent_general.generate_uuid(),
            "description": "",
            "states": []
        }
        for variable_key, state_value in dictionary.items():
            # print(f"  Key: {k}, Value: {v}")
            condition["states"].append(state_value)

        new_car["condition"] = condition
        new_car["name"] = f"场景{m+1}"

        # process resulf for this car
        result = {
            "identifier": seagent_general.generate_uuid(),
            "description": "",
            "states": []
        }

        result["description"] = ""
        new_car["result"] = result
        new_car["description"] = "CAR描述"
        page_spec_json["omsObject"]["actions"][action_index]["cars"].append(new_car)

    print("finished building car table and add to action")
    return page_spec_json



def calculate_states_without_ai_for_one_variable(page_spec_json, variable_identifier):
    # if there are no variables at all, this can happen - there are only functions without input variables
    # just return, do nothing.
    number_of_variables = len(page_spec_json["omsObject"]["memberObjects"])
    if number_of_variables == 0:
        return page_spec_json

    # for each variable
    for i in range(len(page_spec_json["omsObject"]["memberObjects"])):

        if variable_identifier != page_spec_json["omsObject"]["memberObjects"][i]["identifier"]:
            continue

        # variable must have attributes, so we can proceed.
        identifier_dictionary = {}
        page_spec_json["omsObject"]["memberObjects"][i]["states"] = []
        # new_state = {
        #     "identifier": seagent_general.generate_uuid(),
        #     "name": "", 
        #     "attributeAndEquivalenceClasses": []
        # }
        pict_input_text = ""
        for j in range(len(page_spec_json["omsObject"]["memberObjects"][i]["attributes"])):
            attribute_identifier = page_spec_json["omsObject"]["memberObjects"][i]["attributes"][j]["identifier"]
            attribute_name = page_spec_json["omsObject"]["memberObjects"][i]["attributes"][j]["name"]
            identifier_dictionary[attribute_identifier] = attribute_name

            if len(page_spec_json["omsObject"]["memberObjects"][i]["attributes"][j]["equivalenceClasses"]) == 0:
                continue

            line = f"{attribute_identifier}:    "
            for k in range(len(page_spec_json["omsObject"]["memberObjects"][i]["attributes"][j]["equivalenceClasses"])):
                equivalence_class_id = page_spec_json["omsObject"]["memberObjects"][i]["attributes"][j]["equivalenceClasses"][k]["identifier"]
                equivalence_class_name = page_spec_json["omsObject"]["memberObjects"][i]["attributes"][j]["equivalenceClasses"][k]["name"]
                identifier_dictionary[equivalence_class_id] = equivalence_class_name

                line += f"{equivalence_class_id}, "
            line = line.rstrip(', ')
            pict_input_text += f"{line}\n"
        pict_input_text = pict_input_text.rstrip('\n')
        print("PICT:")
        print(pict_input_text)
        if len(pict_input_text) < 64:
            continue
        output = pypict.cmd.from_model(pict_input_text)
        # id-att          att     DBMS        JavaVersion     DotNetVersion
        # id-eq           eqc     PostgreSQL  18              4.8

        json_string = convert_pict_output_to_json(output)
        pict_json = json.loads(json_string)

        print("in pict states")
        print(len(pict_json))

        for m, dictionary in enumerate(pict_json):
            # if m > 5:
            #     break
            print(f"Dictionary {m}:")
            new_state = {
                            "identifier": seagent_general.generate_uuid(),
                            "name": f"状态{m+1}",
                            "attributeAndEquivalenceClasses": []
                        }
            # Iterate over each key-value pair in the dictionary
            for attribute_key, equivalence_class_value in dictionary.items():
                # print(f"  Key: {k}, Value: {v}")
                attributeAndEquivalenceClass = {
                                "attributeId": attribute_key,
                                "equivalenceClassId": equivalence_class_value
                            }
                new_state["attributeAndEquivalenceClasses"].append(attributeAndEquivalenceClass)

            # new_state_copy = new_state
            # new_state_with_names = replace_identifiers(new_state_copy, identifier_dictionary)

            # variable_name = attribute_name = page_spec_json["omsObject"]["memberObjects"][i]["name"]
            # instruction = f"下面json定义变量{variable_name}的一个状态，用中文给状态起个简短状态名(不多于20个字），不解释结果：{new_state_with_names}"
            # description = seagent_llm.chat_with_moonshot_without_history(instruction)
            # new_state["name"] = description
            page_spec_json["omsObject"]["memberObjects"][i]["states"].append(new_state)
            #done, one object
    return page_spec_json

def calculate_states_without_ai(page_spec_json):

    # if there are no variables at all, this can happen - there are only functions without input variables
    # just return, do nothing.
    number_of_variables = len(page_spec_json["omsObject"]["memberObjects"])
    if number_of_variables == 0:
        return page_spec_json

    # for each variable
    for i in range(len(page_spec_json["omsObject"]["memberObjects"])):

        # variable must have attributes, so we can proceed.
        identifier_dictionary = {}
        page_spec_json["omsObject"]["memberObjects"][i]["states"] = []
        # new_state = {
        #     "identifier": seagent_general.generate_uuid(),
        #     "name": "", 
        #     "attributeAndEquivalenceClasses": []
        # }
        pict_input_text = ""
        for j in range(len(page_spec_json["omsObject"]["memberObjects"][i]["attributes"])):
            attribute_identifier = page_spec_json["omsObject"]["memberObjects"][i]["attributes"][j]["identifier"]
            attribute_name = page_spec_json["omsObject"]["memberObjects"][i]["attributes"][j]["name"]
            identifier_dictionary[attribute_identifier] = attribute_name

            if len(page_spec_json["omsObject"]["memberObjects"][i]["attributes"][j]["equivalenceClasses"]) == 0:
                continue

            line = f"{attribute_identifier}:    "
            for k in range(len(page_spec_json["omsObject"]["memberObjects"][i]["attributes"][j]["equivalenceClasses"])):
                equivalence_class_id = page_spec_json["omsObject"]["memberObjects"][i]["attributes"][j]["equivalenceClasses"][k]["identifier"]
                equivalence_class_name = page_spec_json["omsObject"]["memberObjects"][i]["attributes"][j]["equivalenceClasses"][k]["name"]
                identifier_dictionary[equivalence_class_id] = equivalence_class_name

                line += f"{equivalence_class_id}, "
            line = line.rstrip(', ')
            pict_input_text += f"{line}\n"
        pict_input_text = pict_input_text.rstrip('\n')
        print("PICT:")
        print(pict_input_text)
        if len(pict_input_text) < 64:
            continue
        output = pypict.cmd.from_model(pict_input_text)
        # id-att          att     DBMS        JavaVersion     DotNetVersion
        # id-eq           eqc     PostgreSQL  18              4.8

        json_string = convert_pict_output_to_json(output)
        pict_json = json.loads(json_string)

        print("in pict states")
        print(len(pict_json))

        for m, dictionary in enumerate(pict_json):
            if m > 5:
                break
            print(f"Dictionary {m}:")
            new_state = {
                            "identifier": seagent_general.generate_uuid(),
                            "name": "",
                            "attributeAndEquivalenceClasses": []
                        }
            # Iterate over each key-value pair in the dictionary
            for attribute_key, equivalence_class_value in dictionary.items():
                # print(f"  Key: {k}, Value: {v}")
                attributeAndEquivalenceClass = {
                                "attributeId": attribute_key,
                                "equivalenceClassId": equivalence_class_value
                            }
                new_state["attributeAndEquivalenceClasses"].append(attributeAndEquivalenceClass)

            # new_state_copy = new_state
            # new_state_with_names = replace_identifiers(new_state_copy, identifier_dictionary)

            # variable_name = attribute_name = page_spec_json["omsObject"]["memberObjects"][i]["name"]
            # instruction = f"下面json定义变量{variable_name}的一个状态，用中文给状态起个简短状态名(不多于20个字），不解释结果：{new_state_with_names}"
            # description = seagent_llm.chat_with_moonshot_without_history(instruction)
            # new_state["name"] = description
            page_spec_json["omsObject"]["memberObjects"][i]["states"].append(new_state)
            #done, one object
    return page_spec_json