import json
from traceback import print_list
import psycopg2
from config import config


JSON_FILE = "json_files/configClear_v2.json"


def create_table_and_insert_data(data):
    """ Create tables in the PostgreSQL database and insert data.
    Data variable contains a list of all neccessary data comes from JSON_FILE.
    """
    table = (
        """
        CREATE TABLE final_table (
            id SERIAL PRIMARY KEY,
            connection INTEGER,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            config json,
            type VARCHAR(50),
            infra_type VARCHAR(50),
            port_channel_id INTEGER,
            max_frame_size INTEGER
        )
        """)
    sql = "INSERT INTO final_table(id, name, description, config, port_channel_id, max_frame_size) VALUES(%s, %s, %s, %s, %s, %s)"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(table)
        cur.executemany(sql, data)

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_interfaces_dictionary():
    """Read json file and go through the keys and get their values.
    Return variable interfaces_and_content is a nested dictionary of all
    values from specific level of dictionary and specific keys.
    """
    with open(JSON_FILE) as access_json:
        read_content = json.load(access_json)

    topology_content = read_content["frinx-uniconfig-topology:configuration"]
    cisco_IOS_XE_native_content = topology_content["Cisco-IOS-XE-native:native"]
    interfaces_and_content = cisco_IOS_XE_native_content["interface"]
    return interfaces_and_content


def get_specific_interface_and_name(*interfaces):
    """Arguments options: ("BDI", "Loopback", "Port-channel", "TenGigabitEthernet", "GigabitEthernet")
    Get individual interface based upon arguments.
    All content data are append to list variable all_content_data.
    Based upod the interface and value of key "name" is create a list variable name_list.
    """
    all_content_data = []
    name_list = []
    interfaces_and_content = get_interfaces_dictionary()
    for interface in interfaces:
        content_data = interfaces_and_content[interface]
        all_content_data.append(content_data)
        for name in content_data:
            int_name = name["name"]
            converted_name_to_string = str(int_name)
            final_name = interface + converted_name_to_string
            name_list.append(final_name)
    return all_content_data, name_list


def get_description_values(all_content_data, description = "description"):
    """Get description value from all_content_data list variable.
    Input of the fucntion is a nested list of all content data in specific interfaces.
    Itterating throught the level of list get dictionary
    where according to the key, get a description value = description_parameter_list.
    If statement checks if description key has a value.
    """
    description_parameter_list = []
    for parameter_data_list in all_content_data:
        for parameter_data in parameter_data_list:
            if description in parameter_data:
                name_parameter = parameter_data[description]
                description_parameter_list.append(name_parameter)
            else:
                name_parameter = None
                description_parameter_list.append(name_parameter)
    return description_parameter_list


def get_mtu_values(all_content_data, mtu = "mtu"):
    """Get mtu value from all_content_data list variable.
    Input of the fucntion is a nested list of all content data in specific interfaces.
    Itterating throught the level of list get dictionary
    where according to the key, get a mtu value = mtu_parameter_list
    If statement checks if mtu key has a value.
    """
    mtu_parameter_list = []
    for parameter_data_list in all_content_data:
        for parameter_data in parameter_data_list:
            if mtu in parameter_data:
                name_parameter = parameter_data[mtu]
                mtu_parameter_list.append(name_parameter)
            else:
                name_parameter = None
                mtu_parameter_list.append(name_parameter)
    return mtu_parameter_list


def get_whole_configuration_json(all_content_data):
    """Get whole configuration in a json format from all_content_data list variable.
    Input of the fucntion is a nested list of all content data in specific interfaces.
    Itterating throught the level of list gets list of whole configuration
    which is stored to final_configuration_list variable
    """
    final_configuration_list = []
    for configuration in all_content_data:
        for conf in configuration:
            final_configuration_list.append(conf)
    return final_configuration_list


def get_json_objects(final_configuration_list):
    """final_configuration_list variable contains a list of json object."""
    json_object_list = []
    for json_data in final_configuration_list:
        json_object = json.dumps(json_data, indent = 4)
        json_object_list.append(json_object)
    return json_object_list


def create_id_list(input_data_temp):
    """Iterate through the list of data and get cout"""
    id = 0
    ids_list = []
    row_count = len(input_data_temp)
    for id in range(row_count):
        id += 1
        ids_list.append(id)
    return ids_list


def get_id_based_on_name(input_data):
    """Use comprehension list to filter input data and pair seachning name to the unique id. 
    """
    searching_name = "Port-channel20"
    filtered_list = [tup for tup in input_data if searching_name in tup]
    for port_channel_id in filtered_list:
        (port_channel_id, name, description, json, mtu) = port_channel_id
        return port_channel_id


def get_port_channel_id_list(all_content_data,  port_channel_id, configuration = "Cisco-IOS-XE-ethernet:channel-group"):
    """Check if data contains configuration. If yes, create a list of corespondet ids as port_channel_id.
       If data does not contains a configuration, create "null". 
    """
    port_channel_id_list = []
    for parameter_data_list in all_content_data:
        for parameter_data in parameter_data_list:
            if configuration in parameter_data:
                if parameter_data[configuration]:
                    port_channel_id_list.append(port_channel_id)
            else:
                name_parameter = None
                port_channel_id_list.append(name_parameter)
    return port_channel_id_list

def  main():
    #Get Interfaces which want to be parsed from JSON_DATA
    all_content_data, name_list = get_specific_interface_and_name("Port-channel", "TenGigabitEthernet", "GigabitEthernet")

    #Get all of the values which could be parsed from JSON_DATA
    description_parameter_list = get_description_values(all_content_data)
    mtu_parameter_list = get_mtu_values(all_content_data)
    final_configuration_list = get_whole_configuration_json(all_content_data)

    #Make json object from configuration dictionaries
    json_object_list = get_json_objects(final_configuration_list)

    #Get ids based upon number of records
    input_data_temp = list(zip(name_list, description_parameter_list, final_configuration_list, mtu_parameter_list))
    ids_list = create_id_list(input_data_temp)

    #Link Ethernet interfaces to Port-channel under port_channel_id 
    input_data = list(zip(ids_list, name_list, description_parameter_list, final_configuration_list, mtu_parameter_list)) 
    port_channel_id = get_id_based_on_name(input_data)
    port_channel_id_list = get_port_channel_id_list(all_content_data, port_channel_id)
 
    #Prepare final data for insert to postreSQL database
    data = list(zip(ids_list, name_list, description_parameter_list, json_object_list,  port_channel_id_list, mtu_parameter_list))
    
    #Create a table and insert data to final_table in postreSQL database
    create_table_and_insert_data(data)
  
    print("The data has been successfully stored to the PostgreSQL database.")

if __name__ == "__main__":
    main()