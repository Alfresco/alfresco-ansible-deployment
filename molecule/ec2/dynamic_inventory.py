"""
Generate inventory from Molecule scenario
"""

import os
import yaml

with open(os.environ['MOLECULE_EPHEMERAL_DIRECTORY'] + "/instance_config.yml") as yamlfile:
    parsed_yaml_file = yaml.load(yamlfile, Loader=yaml.FullLoader)

with  open(os.path.dirname(os.path.abspath(__file__)) + "/../../inventory_ssh.yml", "r") as old_inventory:
    parsed_old_inventory = yaml.load(old_inventory, Loader=yaml.FullLoader)

with open(os.path.dirname(os.path.abspath(__file__)) + "/../../inventory_ssh.yml", "w") as new_inventory:
    inventoryfile = {'all': {'children':{}}}

    def add_if_key_not_exist(dict_obj, key, value):
        """ Add new key-value pair to dictionary only if
        key does not exist in dictionary. """
        if key not in dict_obj:
            dict_obj.update({key: value})

    address = parsed_yaml_file[0]['address']
    identity_file = parsed_yaml_file[0]['identity_file']

    for item in parsed_old_inventory['all']['children']:
        print(item)
        groupname = item + "_1"
        add_if_key_not_exist(inventoryfile['all']['children'], item, {})
        add_if_key_not_exist(inventoryfile['all']['children'][item], 'hosts', {})
        add_if_key_not_exist(inventoryfile['all']['children'][item]['hosts'], groupname, {})
        add_if_key_not_exist(inventoryfile['all']['children'][item]['hosts'][groupname], 'ansible_host', address)
        add_if_key_not_exist(inventoryfile['all']['children'][item]['hosts'][groupname], 'ansible_private_key_file', identity_file)
        add_if_key_not_exist(inventoryfile['all']['children'][item]['hosts'][groupname], 'ansible_ssh_common_args', "-o UserKnownHostsFile=/dev/null -o ControlMaster=auto -o ControlPersist=60s -o ForwardX11=no -o LogLevel=ERROR -o IdentitiesOnly=yes -o StrictHostKeyChecking=no")
        add_if_key_not_exist(inventoryfile['all']['children'][item]['hosts'][groupname], 'ansible_user', 'centos')
        add_if_key_not_exist(inventoryfile['all']['children'][item]['hosts'][groupname], 'connection', 'ssh')

    yaml.dump(inventoryfile, new_inventory)
