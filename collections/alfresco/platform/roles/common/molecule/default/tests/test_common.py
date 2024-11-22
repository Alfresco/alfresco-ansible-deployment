"""Common role Tests"""
import pytest
from hamcrest import assert_that, equal_to

# pylint: disable=redefined-outer-name
@pytest.fixture(scope="module")
def get_ansible_vars(host):
    """Define get_ansible_vars"""
    common_role = "file=../../vars/main.yml name=common_role"
    common_role_defaults = "file=../../defaults/main.yml name=common_role_defaults"
    ansible_vars = host.ansible("include_vars", common_role)["ansible_facts"]["common_role"]
    ansible_vars = host.ansible("include_vars", common_role_defaults)["ansible_facts"]["common_role_defaults"]
    ansible_vars.update(host.ansible("include_vars", common_role)["ansible_facts"]["common_role"])
    ansible_vars.update(host.ansible("include_vars", common_role_defaults)["ansible_facts"]["common_role_defaults"])
    return ansible_vars

def test_alfresco_user_exists(host, get_ansible_vars):
    """Check that alfresco user exists"""
    assert_that(host.user(get_ansible_vars["username"]).exists)

def test_alfresco_group_exists(host, get_ansible_vars):
    """Check that alfresco group exists"""
    assert_that(host.group(get_ansible_vars["group_name"]).exists)

def test_binaries_folder_exists(host, get_ansible_vars):
    """Check that binaries folder exists"""
    assert_that(host.file(get_ansible_vars["binaries_folder"]).exists)
    assert_that(host.file(get_ansible_vars["binaries_folder"]).user, equal_to(get_ansible_vars["username"]))

def test_config_folder_exists(host, get_ansible_vars):
    """Check that configuration folder exists"""
    assert_that(host.file(get_ansible_vars["config_folder"]).exists)
    assert_that(host.file(get_ansible_vars["config_folder"]).user, equal_to(get_ansible_vars["username"]))

def test_data_folder_exists(host, get_ansible_vars):
    """Check that daya folder exists"""
    assert_that(host.file(get_ansible_vars["data_folder"]).exists)
    assert_that(host.file(get_ansible_vars["data_folder"]).user, equal_to(get_ansible_vars["username"]))

def test_logs_folder_exists(host, get_ansible_vars):
    """Check that logs folder exists"""
    assert_that(host.file(get_ansible_vars["logs_folder"]).exists)
    assert_that(host.file(get_ansible_vars["logs_folder"]).user, equal_to(get_ansible_vars["username"]))
