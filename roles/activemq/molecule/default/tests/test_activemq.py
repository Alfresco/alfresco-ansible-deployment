"""Java Tests"""
import pytest
from hamcrest import assert_that

# pylint: disable=redefined-outer-name
@pytest.fixture()
def get_ansible_vars(host):
    """Define AnsibleVars"""
    java_role = "file=../../vars/main.yml name=java_role"
    activemq_role = "file=../../vars/main.yml name=activemq_role"
    common_vars = "../../../common/vars/main.yml name=common_vars"
    common_defaults = "../../../common/defaults/main.yml name=common_defaults"
    ansible_vars = host.ansible("include_vars", java_role)["ansible_facts"]["java_role"]
    ansible_vars.update(host.ansible("include_vars", java_role)["ansible_facts"]["java_role"])
    ansible_vars.update(host.ansible("include_vars", common_vars)["ansible_facts"]["common_vars"])
    ansible_vars.update(host.ansible("include_vars", common_defaults)["ansible_facts"]["common_defaults"])
    ansible_vars.update(host.ansible("include_vars", activemq_role)["ansible_facts"]["activemq_role"])
    return ansible_vars

def test_activemq_exe_exists(host, get_ansible_vars):
    "Check that ActiveMQ executable exists"
    assert_that(host.file("/opt/apache-activemq-{}/bin/activemq".format(get_ansible_vars["activemq_version"])).exists, get_ansible_vars["activemq_home"])