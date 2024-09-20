from neo4j import GraphDatabase
import os, json, re
import seagent_file
import subprocess
from dotenv import load_dotenv
from py2neo import Graph

# Define a class to manage Neo4j connection
class Neo4jClient:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query(self, cypher_query):
        with self.driver.session() as session:
            result = session.run(cypher_query)
            return [record for record in result]
        
# def escape_cypher_string(input_string):
#     # Escape backslashes by doubling them
#     escaped_string = re.sub(r'\\(?!["nrtbfav0\'"\\])', '\\\\', input_string)
    
#     # Escape double quotes by escaping the backslash before them
#     escaped_string = escaped_string.replace('\\"', '\\\\"')
    
#     return escaped_string

def cypher_execution(query):
    load_dotenv()
    NEO4J_URL = os.getenv("NEO4J_URL")
    NEO4J_USER = os.getenv("NEO4J_USER")
    NEO4J__PASSWORD = os.getenv("NEO4J__PASSWORD")

    # Instantiate the Neo4j client
    # client = Neo4jClient(NEO4J_URL)
    client = Neo4jClient(NEO4J_URL, NEO4J_USER, NEO4J__PASSWORD)

    # Define a Cypher query
    # query = "MATCH (n) RETURN n LIMIT 5"

    # Execute the query and print the results
    results = client.query(query)
    # for record in results:
    #     print(record)

    # Close the connection
    client.close()

def remove_project_from_gdb(project_name):
    # Define the Cypher query to delete nodes with the specific project_name attribute value
    query = f"""
    MATCH (n)
    WHERE n.project_name = '{project_name}'
    DETACH DELETE n
    """
    cypher_execution(query)

def add_identifier_index():
    query = """
    CREATE INDEX car_identifier_index IF NOT EXISTS
    FOR (a:car)
    ON (a.identifier)
    """
    cypher_execution(query)


def create_action(project_name, parent_node_identifier, action_json):
    identifier = action_json["identifier"]
    name = action_json["name"]
    description = action_json["description"]

    query = f"""
    CREATE (o:action {{
        identifier: '{identifier}',
        name: '{name}',
        description: '{description}',
        project_name: '{project_name}'
    }})
    """
    cypher_execution(query)

    query = f"""
    MATCH (o:omsObject {{identifier: '{parent_node_identifier}'}})
    MATCH (p:action {{identifier: '{identifier}'}})
    CREATE (o)-[:CHILD]->(p)
    """
    cypher_execution(query)

def create_car(project_name, parent_node_identifier, car_json):
    identifier = car_json["identifier"]
    name = car_json["name"]
    description = car_json["description"]

    query = f"""
    CREATE (o:car {{
        identifier: '{identifier}',
        name: '{name}',
        description: '{description}',
        project_name: '{project_name}'
    }})
    """
    cypher_execution(query)

    query = f"""
    MATCH (o:actin {{identifier: '{parent_node_identifier}'}})
    MATCH (p:car {{identifier: '{identifier}'}})
    CREATE (o)-[:CHILD]->(p)
    """
    cypher_execution(query)

def create_condition(project_name, parent_node_identifier, condition_json):
    identifier = condition_json["identifier"]
    description = condition_json["description"]

    query = f"""
    CREATE (o:condition {{
        identifier: '{identifier}',
        description: '{description}',
        project_name: '{project_name}'
    }})
    """
    cypher_execution(query)

    query = f"""
    MATCH (o:car {{identifier: '{parent_node_identifier}'}})
    MATCH (p:condition {{identifier: '{identifier}'}})
    CREATE (o)-[:CHILD]->(p)
    """
    cypher_execution(query)

def create_condition_states(project_name, parent_node_identifier, condition_states_json):
    number_of_states = len(condition_states_json)
    for i in range(number_of_states):
        identifier = condition_states_json[i]["identifier"]

        query = f"""
        CREATE (o:condition_state {{
            identifier: '{identifier}',
            project_name: '{project_name}'
        }})
        """
        cypher_execution(query)

        query = f"""
        MATCH (o:condition {{identifier: '{parent_node_identifier}'}})
        MATCH (p:condition_state {{identifier: '{identifier}'}})
        CREATE (o)-[:CHILD]->(p)
        """
        cypher_execution(query)

def create_result(project_name, parent_node_identifier, result_json):
    identifier = result_json["identifier"]
    description = result_json["description"]

    query = f"""
    CREATE (o:result {{
        identifier: '{identifier}',
        description: '{description}',
        project_name: '{project_name}'
    }})
    """
    cypher_execution(query)

    query = f"""
    MATCH (o:car {{identifier: '{parent_node_identifier}'}})
    MATCH (p:result {{identifier: '{identifier}'}})
    CREATE (o)-[:CHILD]->(p)
    """
    cypher_execution(query)

def create_result_states(project_name, parent_node_identifier, result_states_json):
    number_of_states = len(result_states_json)
    for i in range(number_of_states):
        identifier = result_states_json[i]["identifier"]

        query = f"""
        CREATE (o:result_state {{
            identifier: '{identifier}',
            project_name: '{project_name}'
        }})
        """
        cypher_execution(query)

        query = f"""
        MATCH (o:result {{identifier: '{parent_node_identifier}'}})
        MATCH (p:result_state {{identifier: '{identifier}'}})
        CREATE (o)-[:CHILD]->(p)
        """
        cypher_execution(query)

def create_nextCars(project_name, parent_node_identifier, nextCars_json):
    number_of_nextCars = len(nextCars_json)
    for i in range(number_of_nextCars):
        identifier = nextCars_json[i]["identifier"]

        query = f"""
        CREATE (o:nextCar {{
            identifier: '{identifier}',
            project_name: '{project_name}'
        }})
        """
        cypher_execution(query)

        query = f"""
        MATCH (o:car {{identifier: '{parent_node_identifier}'}})
        MATCH (p:nextCar {{identifier: '{identifier}'}})
        CREATE (o)-[:NEXT]->(p)
        """
        cypher_execution(query)

def create_memberObject(project_name, parent_node_identifier, memberObject_json):
    identifier = memberObject_json["identifier"]
    name = memberObject_json["name"]
    description = memberObject_json["description"]

    query = f"""
    CREATE (o:memberObject {{
        identifier: '{identifier}',
        name: '{name}',
        description: '{description}',
        project_name: '{project_name}'
    }})
    """
    cypher_execution(query)

    query = f"""
    MATCH (o:omsObject {{identifier: '{parent_node_identifier}'}})
    MATCH (p:memberObject {{identifier: '{identifier}'}})
    CREATE (o)-[:CHILD]->(p)
    """
    cypher_execution(query)

def create_attribute(project_name, parent_node_identifier, attribute_json):
    identifier = attribute_json["identifier"]
    name = attribute_json["name"]
    description = attribute_json["description"]

    query = f"""
    CREATE (o:attribute {{
        identifier: '{identifier}',
        name: '{name}',
        description: '{description}',
        project_name: '{project_name}'
    }})
    """
    cypher_execution(query)

    query = f"""
    MATCH (o:memberObject {{identifier: '{parent_node_identifier}'}})
    MATCH (p:attribute {{identifier: '{identifier}'}})
    CREATE (o)-[:CHILD]->(p)
    """
    cypher_execution(query)

def create_equivalenceClass(project_name, parent_node_identifier, equivalenceClass_json):
    identifier = equivalenceClass_json["identifier"]
    name = equivalenceClass_json["name"]
    description = equivalenceClass_json["description"]

    query = f"""
    CREATE (o:equivalenceClass {{
        identifier: '{identifier}',
        name: '{name}',
        description: '{description}',
        project_name: '{project_name}'
    }})
    """
    cypher_execution(query)

    query = f"""
    MATCH (o:attribute {{identifier: '{parent_node_identifier}'}})
    MATCH (p:equivalenceClass {{identifier: '{identifier}'}})
    CREATE (o)-[:CHILD]->(p)
    """
    cypher_execution(query)

def create_state(project_name, parent_node_identifier, state_json):
    identifier = state_json["identifier"]
    name = state_json["name"]

    query = f"""
    CREATE (o:state {{
        identifier: '{identifier}',
        name: '{name}',
        project_name: '{project_name}'
    }})
    """
    cypher_execution(query)

    query = f"""
    MATCH (o:memberObject {{identifier: '{parent_node_identifier}'}})
    MATCH (p:state {{identifier: '{identifier}'}})
    CREATE (o)-[:CHILD]->(p)
    """
    cypher_execution(query)

# this is root node for a page
def create_omsObject(project_name, omsObject_json):
    # Extract the relevant information from the JSON
    oms_object = omsObject_json
    oms_object_id = omsObject_json["identifier"]
    oms_object_name = omsObject_json["name"]
    oms_object_description = omsObject_json["description"]
    oms_object_classification = omsObject_json["classification"]
    # oms_object_version = data.get("version")

    query = f"""
    CREATE (o:omsObject {{
        identifier: '{oms_object_id}',
        name: '{oms_object_name}',
        description: '{oms_object_description}',
        classification: '{oms_object_classification}',
        project_name: '{project_name}'
    }})
    """
    # CREATE (o:OmsObject {identifier: '12345', name: 'Object A', description: 'A description of Object A', classification: 'Type X', project_name: 'Project Alpha'})

    cypher_execution(query)

def create_one_oms(full_path_to_spec_json, user_identifier=None):
    spec_json = seagent_file.oms_load(full_path_to_spec_json)
    if user_identifier is None:
        project_name = spec_json["info"]["title"]
    else:
        project_name = spec_json["info"]["title"] + f"-{user_identifier}"

    # remove old data
    remove_project_from_gdb(project_name)

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
        create_action(project_name, spec_json["omsObject"]["actions"][index_actions])

        number_of_cars = len(spec_json["omsObject"]["actions"][index_actions]["cars"])    
        for index_cars in range(number_of_cars):
            create_car(project_name, spec_json["omsObject"]["actions"][index_actions]["identifier"], spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars])
            create_condition(project_name, spec_json["omsObject"]["actions"][index_actions]["identifier"], spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars]["condition"])
            create_condition_states(project_name, spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars]["identifier"], spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars]["condition"]["states"])

            create_result(project_name, spec_json["omsObject"]["actions"][index_actions]["identifier"], spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars]["result"])
            create_result_states(project_name, spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars]["identifier"], spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars]["result"]["states"])

            create_nextCars(project_name, spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars]["identifier"], spec_json["omsObject"]["actions"][index_actions]["cars"][index_cars]["nextCar"])



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
def inset_all_oms(oms_directory: str):
    
    entries = os.listdir(oms_directory)
    for entry in entries:
        full_path = os.path.join(oms_directory, entry)
        create_one_oms(full_path)
    
    add_identifier_index()


def generate_testcase_json():
    # get json output
    # produce excel
    # save excel
    pass

inset_all_oms("/opt/bihua/reqgpt/data/apps/安全文件上传与登录验证系统")