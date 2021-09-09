"""
Generate inventory from Molecule scenario
"""

import os
import re
import yaml

with open(os.environ['MOLECULE_EPHEMERAL_DIRECTORY'] + "/instance_config.yml", encoding='utf-8') as yamlfile:
    parsed_yaml_file = yaml.load(yamlfile, Loader=yaml.FullLoader)

with open(os.path.dirname(os.path.abspath(__file__)) + "/../../inventory_ssh.yml", "w", encoding='utf-8') as new_inventory:
    inventoryfile = {'all': {'children':{}}}

    def add_if_key_not_exist(dict_obj, key, value):
        """ Add new key-value pair to dictionary only if
        key does not exist in dictionary. """
        if key not in dict_obj:
            dict_obj.update({key: value})

    for item in parsed_yaml_file:
        print(item)
        groupname = re.sub(r'_.*', '', item['instance'])
        add_if_key_not_exist(inventoryfile['all']['children'], groupname, {})
        add_if_key_not_exist(inventoryfile['all']['children'][groupname], 'hosts', {})
        add_if_key_not_exist(inventoryfile['all']['children'][groupname]['hosts'], item['instance'], {
            'ansible_host': item['address'],
            'ansible_private_key_file': item['identity_file'],
            'ansible_ssh_common_args': "-o UserKnownHostsFile=/dev/null -o ControlMaster=auto -o ControlPersist=60s -o ForwardX11=no -o LogLevel=ERROR -o IdentitiesOnly=yes -o StrictHostKeyChecking=no",
            'ansible_user': 'centos',
            'connection': 'ssh'
        })

        if groupname=='nginx':
            add_if_key_not_exist(inventoryfile['all']['children'], 'adw', {})
            add_if_key_not_exist(inventoryfile['all']['children']['adw'], 'hosts', {})
            add_if_key_not_exist(inventoryfile['all']['children']['adw']['hosts'], 'adw_1', {
                'ansible_host': item['address'],
                'ansible_private_key_file': item['identity_file'],
                'ansible_ssh_common_args': "-o UserKnownHostsFile=/dev/null -o ControlMaster=auto -o ControlPersist=60s -o ForwardX11=no -o LogLevel=ERROR -o IdentitiesOnly=yes -o StrictHostKeyChecking=no",
                'ansible_user': 'centos',
                'connection': 'ssh'
            })

    yaml.dump(inventoryfile, new_inventory)
