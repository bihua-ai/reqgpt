from py2neo import Graph
import os
from dotenv import load_dotenv
import seagent_file


def cypher_execution(query, parameters=None):
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "sw2201!@#"))
    return graph.run(query, parameters)


def remove_project_from_gdb(project_name):
    query = """
    MATCH (n)
    WHERE n.project_name = $project_name
    DETACH DELETE n
    """
    cypher_execution(query, {'project_name': project_name})

def add_identifier_index():
    query = """
    CREATE INDEX car_identifier_index IF NOT EXISTS
    FOR (a:car)
    ON (a.identifier)
    """
    cypher_execution(query, parameters=None)

def create_action(project_name, parent_node_identifier, action_json):
    query = """
    CREATE (o:action {
        identifier: $identifier,
        name: $name,
        description: $description,
        project_name: $project_name
    })
    """
    cypher_execution(query, {
        'identifier': action_json["identifier"],
        'name': action_json["name"],
        'description': action_json["description"],
        'project_name': project_name
    })

    query = """
    MATCH (o:omsObject {identifier: $parent_node_identifier})
    MATCH (p:action {identifier: $identifier})
    CREATE (o)-[:CHILD]->(p)
    """
    cypher_execution(query, {
        'parent_node_identifier': parent_node_identifier,
        'identifier': action_json["identifier"]
    })

def create_car(project_name, parent_node_identifier, car_json):
    query = """
    CREATE (o:car {
        identifier: $identifier,
        name: $name,
        description: $description,
        project_name: $project_name
    })
    """
    cypher_execution(query, {
        'identifier': car_json["identifier"],
        'name': car_json["name"],
        'description': car_json["description"],
        'project_name': project_name
    })

    query = """
    MATCH (o:action {identifier: $parent_node_identifier})
    MATCH (p:car {identifier: $identifier})
    CREATE (o)-[:CHILD]->(p)
    """
    print("in create_car")
    print(parent_node_identifier)
    print(car_json["identifier"])

    cypher_execution(query, {
        'parent_node_identifier': parent_node_identifier,
        'identifier': car_json["identifier"]
    })


def create_condition(project_name, parent_node_identifier, condition_json):
    query = """
    CREATE (o:condition {
        identifier: $identifier,
        description: $description,
        project_name: $project_name
    })
    """
    cypher_execution(query, {
        'identifier': condition_json["identifier"],
        'description': condition_json["description"],
        'project_name': project_name
    })

    query = """
    MATCH (o:car {identifier: $parent_node_identifier})
    MATCH (p:condition {identifier: $identifier})
    CREATE (o)-[:CHILD]->(p)
    """
    cypher_execution(query, {
        'parent_node_identifier': parent_node_identifier,
        'identifier': condition_json["identifier"]
    })

def create_condition_states(project_name, parent_node_identifier, condition_states_json):
    number_of_states = len(condition_states_json)
    for i in range(number_of_states):
        query = """
        CREATE (o:condition_state {
            identifier: $identifier,
            project_name: $project_name
        })
        """
        cypher_execution(query, {
            'identifier': condition_states_json[i],
            'project_name': project_name
        })

        query = """
        MATCH (o:condition {identifier: $parent_node_identifier})
        MATCH (p:condition_state {identifier: $identifier})
        CREATE (o)-[:CHILD]->(p)
        """
        cypher_execution(query, {
            'parent_node_identifier': parent_node_identifier,
            'identifier': condition_states_json[i]
        })

def create_result(project_name, parent_node_identifier, result_json):
    query = """
    CREATE (o:result {
        identifier: $identifier,
        description: $description,
        project_name: $project_name
    })
    """
    cypher_execution(query, {
        'identifier': result_json["identifier"],
        'description': result_json["description"],
        'project_name': project_name
    })

    query = """
    MATCH (o:car {identifier: $parent_node_identifier})
    MATCH (p:result {identifier: $identifier})
    CREATE (o)-[:CHILD]->(p)
    """
    cypher_execution(query, {
        'parent_node_identifier': parent_node_identifier,
        'identifier': result_json["identifier"]
    })

def create_result_states(project_name, parent_node_identifier, result_states_json):
    number_of_states = len(result_states_json)
    for i in range(number_of_states):
        query = """
        CREATE (o:result_state {
            identifier: $identifier,
            project_name: $project_name
        })
        """
        cypher_execution(query, {
            'identifier': result_states_json[i],
            'project_name': project_name
        })

        query = """
        MATCH (o:result {identifier: $parent_node_identifier})
        MATCH (p:result_state {identifier: $identifier})
        CREATE (o)-[:CHILD]->(p)
        """
        cypher_execution(query, {
            'parent_node_identifier': parent_node_identifier,
            'identifier': result_states_json[i]
        })

# chnage to create NEXT relation, not node
def create_nextCars(project_name, upstream_car_identifier, nextCars_json):
    number_of_next_cars = len(nextCars_json)

    for i in range(number_of_next_cars):
    # for car in nextCars_json:
        # query = """
        # CREATE (o:nextCar {
        #     identifier: $identifier,
        #     project_name: $project_name
        # })
        # """
        # cypher_execution(query, {
        #     'identifier': nextCars_json[i],
        #     'project_name': project_name
        # })

        # query = """
        # MATCH (o:car {identifier: $upstream_car_identifier})
        # MATCH (p:car {identifier: $identifier})
        # CREATE (o)-[:NEXT]->(p)
        # """
        query = """
        MATCH (o:car {identifier: $upstream_car_identifier})
        MATCH (p:car {identifier: $identifier})
        CREATE (o)-[:NEXT]->(p)
        """
        cypher_execution(query, {
            'upstream_car_identifier': upstream_car_identifier,
            'identifier': nextCars_json[i]
        })

def create_memberObject(project_name, parent_node_identifier, memberObject_json):
    query = """
    CREATE (o:memberObject {
        identifier: $identifier,
        name: $name,
        description: $description,
        project_name: $project_name
    })
    """
    cypher_execution(query, {
        'identifier': memberObject_json["identifier"],
        'name': memberObject_json["name"],
        'description': memberObject_json["description"],
        'project_name': project_name
    })

    query = """
    MATCH (o:omsObject {identifier: $parent_node_identifier})
    MATCH (p:memberObject {identifier: $identifier})
    CREATE (o)-[:CHILD]->(p)
    """
    cypher_execution(query, {
        'parent_node_identifier': parent_node_identifier,
        'identifier': memberObject_json["identifier"]
    })

def create_attribute(project_name, parent_node_identifier, attribute_json):
    query = """
    CREATE (o:attribute {
        identifier: $identifier,
        name: $name,
        description: $description,
        project_name: $project_name
    })
    """
    cypher_execution(query, {
        'identifier': attribute_json["identifier"],
        'name': attribute_json["name"],
        'description': attribute_json["description"],
        'project_name': project_name
    })

    query = """
    MATCH (o:memberObject {identifier: $parent_node_identifier})
    MATCH (p:attribute {identifier: $identifier})
    CREATE (o)-[:CHILD]->(p)
    """
    cypher_execution(query, {
        'parent_node_identifier': parent_node_identifier,
        'identifier': attribute_json["identifier"]
    })

def create_equivalenceClass(project_name, parent_node_identifier, equivalenceClass_json):
    query = """
    CREATE (o:equivalenceClass {
        identifier: $identifier,
        name: $name,
        description: $description,
        project_name: $project_name
    })
    """
    cypher_execution(query, {
        'identifier': equivalenceClass_json["identifier"],
        'name': equivalenceClass_json["name"],
        'description': equivalenceClass_json["description"],
        'project_name': project_name
    })

    query = """
    MATCH (o:attribute {identifier: $parent_node_identifier})
    MATCH (p:equivalenceClass {identifier: $identifier})
    CREATE (o)-[:CHILD]->(p)
    """
    cypher_execution(query, {
        'parent_node_identifier': parent_node_identifier,
        'identifier': equivalenceClass_json["identifier"]
    })

def create_state(project_name, parent_node_identifier, state_json):
    query = """
    CREATE (o:state {
        identifier: $identifier,
        name: $name,
        project_name: $project_name
    })
    """
    cypher_execution(query, {
        'identifier': state_json["identifier"],
        'name': state_json["name"],
        'project_name': project_name
    })

    query = """
    MATCH (o:memberObject {identifier: $parent_node_identifier})
    MATCH (p:state {identifier: $identifier})
    CREATE (o)-[:CHILD]->(p)
    """
    cypher_execution(query, {
        'parent_node_identifier': parent_node_identifier,
        'identifier': state_json["identifier"]
    })

def create_omsObject(project_name, omsObject_json):
    # project_name = "安全文件上传与登录验证系统_eric"
    query = """
    CREATE (o:omsObject {
        identifier: $identifier,
        name: $name,
        description: $description,
        classification: $classification,
        project_name: $project_name
    })
    """

    cypher_execution(query, {
        'identifier': omsObject_json["identifier"],
        'name': omsObject_json["name"],
        'description': omsObject_json["description"],
        'classification': omsObject_json["classification"],
        'project_name': project_name
    })


def create_omsObject1(project_name, omsObject_json):
    query = """
    CREATE (o:omsObject {
        identifier: $identifier,
        name: $name,
        description: $description,
        classification: $classification,
        project_name: $project_name
    })
    """

    cypher_execution(query, {
        'identifier': omsObject_json["identifier"],
        'name': omsObject_json["name"],
        'description': omsObject_json["description"],
        'classification': omsObject_json["classification"],
        'project_name': project_name
    })

# project name in chinese will cause problem

def insert_one_oms_in_gdb(full_path_to_spec_json, project_name, user_identifier=None):
    spec_json = seagent_file.oms_load(full_path_to_spec_json)

    # if user_identifier is None:
    #     project_name = spec_json["info"]["title"]
    # else:
    #     project_name = spec_json["info"]["title"] + f"_{user_identifier}"

    # print(f"insert_one_oms_in_gdb = {project_name}  {len(project_name)}")

    # remove old data
    # remove_project_from_gdb(project_name)

    create_omsObject(project_name, spec_json["omsObject"])

    number_of_memberObjects = len(spec_json["omsObject"]["memberObjects"])
    for index_memberObjects in range(number_of_memberObjects):

        create_memberObject(project_name, spec_json["omsObject"]["identifier"], spec_json["omsObject"]["memberObjects"][index_memberObjects])

        number_of_attributes = len(spec_json["omsObject"]["memberObjects"][index_memberObjects]["attributes"])
        for index_attributes in range(number_of_attributes):
            create_attribute(project_name, spec_json["omsObject"]["memberObjects"][index_memberObjects]["identifier"], spec_json["omsObject"]["memberObjects"][index_memberObjects]["attributes"][index_attributes])

            number_of_equivalenceClasses = len(spec_json["omsObject"]["memberObjects"][index_memberObjects]["attributes"][index_attributes]["equivalenceClasses"])
            for index_equivalenceClasses in range(number_of_equivalenceClasses):
                create_equivalenceClass(project_name, spec_json["omsObject"]["memberObjects"][index_memberObjects]["attributes"][index_attributes]["identifier"], spec_json["omsObject"]["memberObjects"][index_memberObjects]["attributes"][index_attributes]["equivalenceClasses"][index_equivalenceClasses])

        number_of_states = len(spec_json["omsObject"]["memberObjects"][index_memberObjects]["states"])
        for index_states in range(number_of_states):
            create_state(project_name, spec_json["omsObject"]["memberObjects"][index_memberObjects]["identifier"], spec_json["omsObject"]["memberObjects"][index_memberObjects]["states"][index_states])

    number_of_actions = len(spec_json["omsObject"]["actions"])
    for index_actions in range(number_of_actions):
        create_action(project_name, spec_json["omsObject"]["identifier"], spec_json["omsObject"]["actions"][index_actions])

        number_of_cars = len(spec_json["omsObject"]["actions"][index_actions]["cars"])    
        for index_cars in range(number_of_cars):
            create_car(project_name, spec_json["omsObject"]["actions"][index_actions]["identifier"], spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars])

            create_nextCars(project_name, spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars]["identifier"], spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars]["nextCar"])

            create_condition(project_name, spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars]["identifier"], spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars]["condition"])

            create_condition_states(project_name, spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars]["condition"]["identifier"], spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars]["condition"]["states"])

            create_result(project_name, spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars]["identifier"], spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars]["result"])

            create_result_states(project_name, spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars]["result"]["identifier"], spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars]["result"]["states"])

    # return project_name

    # spec_json["omsObject"]["actions"]
    # spec_json["omsObject"]["actions"][i]["cars"]
    # spec_json["omsObject"]["actions"][i]["cars"][j]["condition"]
    # spec_json["omsObject"]["actions"][i]["cars"][j]["condition"]["states"]
    # spec_json["omsObject"]["actions"][i]["cars"][j]["condition"]["states"][k] # list of identifiers

    # spec_json["omsObject"]["actions"][i]["cars"][j]["result"]
    # spec_json["omsObject"]["actions"][i]["cars"][j]["result"]["states"]
    # spec_json["omsObject"]["actions"][i]["cars"][j]["nextCar"] # list of identifiers


    # # spec_json["omsObject"]["memberObjects"]
    # spec_json["omsObject"]["memberObjects"][i]["attributes"]
    # spec_json["omsObject"]["memberObjects"][i]["attributes"][j]["equivalenceClasses"]
    # spec_json["omsObject"]["memberObjects"][i]["states"]

    # for i in range(len(spec_json["omsObject"]["actions"])):
    #     if action_identifier == spec_json["omsObject"]["actions"][i]["identifier"]:
    #         action_description = spec_json["omsObject"]["actions"][i]["description"]


# all projects are in the same database with name n eo4j
def insert_all_oms_to_gdb(oms_directory: str, user_identifier=None): 
    deleted = False   
    spec_json = None
    entries = os.listdir(oms_directory)
    project_name = None
    for entry in entries:
        full_path = os.path.join(oms_directory, entry)
        spec_json = seagent_file.oms_load(full_path)
        project_name = spec_json["info"]["title"]
        if user_identifier is None:
            project_name = spec_json["info"]["title"]
        else:
            project_name = spec_json["info"]["title"] + f"_{user_identifier}"
        if deleted == False: 
            remove_project_from_gdb(project_name)
            deleted = True
        insert_one_oms_in_gdb(full_path, project_name, user_identifier=user_identifier)
    add_identifier_index()
    return project_name

def get_start_cars():
    pass
def generate_testset_json(project_path, user_id, testcase_scope):
    # get start cars - 
    project_name = os.path.basename(os.path.normpath(project_path))
    get_start_cars(project_name)

    # get end cars

    # generate paths - json

    pass

# insert_all_oms("/opt/bihua/reqgpt/data/apps/安全文件上传与登录验证系统", "eric")