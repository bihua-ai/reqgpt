import os, uuid
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import seagent_general

# assume company first create enterprise
# then create an app from ui

# INSERT INTO `app_enterprise`(`id`, `app_id`, `enterprise_id`) VALUES ('[value-1]','[value-2]','[value-3]')
def sql_command(query, host= None, sql_user=None , password=None, database=None, sql_port = None):
    connection = None
    host = host or os.getenv("SQL_HOST")
    sql_user = sql_user or os.getenv("SQL_USER")
    password = password or os.getenv("SQL_PASSWORD")  # Corrected the spelling
    database = database or os.getenv("DATABASE")
    sql_port = sql_port or os.getenv("SQL_PORT")
    
    # if host == None:
    #     host = os.getenv("SQL_HOST")
    # if sql_user == None:
    #     sql_user = os.getenv("SQL_USER")
    # if password == None:
    #     password = os.getenv("SQL_PASWORD")
    # if database == None:
    #     database = os.getenv("DATABASE")
    # if sql_port == None:
    #     sql_port = os.getenv("SQL_PORT")

    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host=host,
            user=sql_user,
            password=password,
            database=database,
            port=int(sql_port)
        )
        if connection.is_connected():
            print("Successfully connected to the database.")
            
            # Create a cursor object using the connection
            cursor = connection.cursor()
            
            # Execute the query
            cursor.execute(query)
            
            # Fetch all the records and print them
            records = cursor.fetchall()
            for record in records:
                print(record)
            
            cursor.close()
        else:
            print("Failed to connect to the database.")
    except Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        if connection and connection.is_connected():
            connection.close()
            print("Database connection closed.")



def create_webapp(enterprise_id, module_name, type_value, domain, module_description=None, content=None):
    
    module_identifier = seagent_general.generate_uuid()


    insert_statement = f"""
        INSERT INTO app (identifier, name, type, domain, description, content)
        VALUES ('{module_identifier}', '{module_name}', '{type_value}', '{domain}', '{module_description}', '{content}');
    
        SELECT id INTO app_id_value FROM apps WHERE app_id = {module_identifier}

        INSERT INTO `app_enterprise`(`app_id`, `enterprise_id`)
        VALUES(app_id_value, {enterprise_id})

    """
    try:
        sql_command(insert_statement)
    except Exception as e:
                print(f"An error occurred in create_module: {e}")


def update_module(module_id, module_name, type_value, domain, module_description=None, content=None):
    try:
        if module_name is not None:
            update_statement = f"""
                UPDATE app
                SET name = {module_name}
                WHERE identifier = {module_id};
            """
            sql_command(update_statement)

        if module_name is not None:
            update_statement = f"""
                UPDATE app
                SET name = {module_description}
                WHERE identifier = {module_id};
            """
            sql_command(update_statement)

        if module_name is not None:
            update_statement = f"""
                UPDATE app
                SET name = {content}
                WHERE identifier = {module_id};
            """
            sql_command(update_statement)

        
    except Exception as e:
                print(f"An error occurred in update_module : {e}")

def delete_module(module_id, module_name, type_value, domain, module_description=None, content=None):

    delete_statement = f"""
        DELETE FROM app
        WHERE identifier = {module_id};
    """
    try:
        sql_command(delete_statement)
    except Exception as e:
                print(f"An error occurred in delete_module: {e}")

    



