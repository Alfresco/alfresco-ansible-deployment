#!/usr/bin/env python

"""Generate components version table in docs/README.md based on extra-vars.yml."""

import sys
import glob
import yaml


def get_acs_extra_vars_files():
    """Return list of extra-vars files in repository."""
    var_files = glob.glob("*-extra-vars.yml")[::-1]
    #move community to the end of list
    var_files.append(var_files.pop(var_files.index('community-extra-vars.yml')))
    var_files.insert(0, 'group_vars/all.yml')
    return var_files

def get_latest_acs_version():
    """Return version of current acs release."""
    with open("group_vars/all.yml", "r", encoding="utf-8") as stream:
        try:
            values = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)
    latest_version = values.get('acs', {}).get('version')
    return latest_version

def get_first_line_of_table():
    """Generate table header."""
    first_line = "| Component |"
    for values_file in get_acs_extra_vars_files():
        if values_file == 'group_vars/all.yml':
            acs_release = get_latest_acs_version()
            acs_release = f"{acs_release.split('.')[0]}.{acs_release.split('.')[1]} Enterprise"
        else:
            acs_release = values_file.replace('-extra-vars.yml', '')
            if acs_release == 'community':
                acs_release = acs_release.capitalize()
            else:
                acs_release+=" Enterprise"

        first_line+= f" {acs_release} |"
    return first_line


def get_components_versions(file_path):
    """Return dict of components version for given vars file."""
    with open(file_path, "r", encoding="utf-8") as stream:
        try:
            values = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

        components_versions = {
            'OpenJDK': values.get('dependencies_version', {}).get('jdk'),
            'Apache_Tomcat': values.get('dependencies_version', {}).get('tomcat'),
            'PostgreSQL': values.get('dependencies_version', {}).get('postgres_major_version'),
            'Apache_ActiveMQ': values.get('dependencies_version', {}).get('activemq'),
            'Repository': values.get('acs', {}).get('version'),
            'Share': values.get('acs', {}).get('version'),
            'Search_Services': values.get('search', {}).get('version'),
            'All-In-One_Transformation_Engine': values.get('transform', {}).get('version'),
            'AOS': values.get('amps', {}).get('aos_module', {}).get('version'),
            'GoogleDocs': values.get('amps', {}).get('googledrive_repo', {}).get('version'),
            'Digital_Workspace': values.get('adw', {}).get('version'),
            'Transform_Router': values.get('trouter', {}).get('version'),
            'Shared_File_Store': values.get('sfs', {}).get('version'),
            'Sync_Service': values.get('sync', {}).get('version'),
        }
        return components_versions


def get_content_of_new_table():
    """Generate content of new table."""
    end_table = ""
    first_line = get_first_line_of_table()
    end_table+=f"{first_line}\n"
    second_line = '|-|-|-|-|-|'
    end_table+=f"{second_line}\n"

    for component in list(get_components_versions("group_vars/all.yml").keys()):
        line_in_table = ''
        line_in_table+=f"| {component.replace('_', ' ')} | "

        for values_file in get_acs_extra_vars_files():
            components_versions = get_components_versions(values_file)
            version = (components_versions[component])

            if values_file == 'community-extra-vars.yml' and component in ['Digital_Workspace', 'Transform_Router', 'Shared_File_Store', 'Sync_Service']:
                version = 'N/A'
            elif values_file == 'community-extra-vars.yml' and component in ['AOS', 'GoogleDocs']:
                version = ''
            #use values from group_vars if None
            elif version is None:
                components_versions = get_components_versions(get_acs_extra_vars_files()[0])
                version = (components_versions[component])

            if component == 'PostgreSQL':
                version= str(version) + '.x'

            line_in_table+=f"{version} | "

        line_in_table=line_in_table[:-1]
        end_table+=f"{line_in_table}\n"
    return end_table

def modify_table():
    """Delete old table from README.md, and put new one."""
    delete_next_lines = False
    with open("docs/README.md", "r", encoding="utf-8") as old_file:
        lines = old_file.readlines()

    with open("docs/README.md", "w", encoding="utf-8") as new_file:
        for line in lines:

            if "| Sync Service | " in line.strip("\n"):
                delete_next_lines = False
                new_file.write(get_content_of_new_table())
            elif delete_next_lines is True:
                pass
            elif "| Component | " in line.strip("\n"):
                delete_next_lines = True
            else:
                new_file.write(line)

if __name__ == '__main__':
    modify_table()
    print("done")
