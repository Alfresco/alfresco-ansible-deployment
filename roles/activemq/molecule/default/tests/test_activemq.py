"""ActiveMQ Tests"""
import pytest
from hamcrest import assert_that, contains_string

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

def test_activemq_version(host, get_ansible_vars):
    "Check that ActiveMQ version is correct"
    cmd = host.run("source {}/setenv.sh && $ACTIVEMQ_HOME/bin/activemq --version".format(get_ansible_vars["config_folder"]))
    assert_that(cmd.stdout, contains_string("ActiveMQ {}".format(get_ansible_vars["activemq_version"])))

def test_activemq_home(host, get_ansible_vars):
    "Check that ActiveMQ home is set correctly"
    cmd = host.run("source {}/setenv.sh && echo $ACTIVEMQ_HOME".format(get_ansible_vars["config_folder"]))
    assert_that(cmd.stdout, contains_string("/opt/apache-activemq-{}".format(get_ansible_vars["activemq_version"])))

def test_activemq_service(host, get_ansible_vars):
    "Check that ActiveMQ is enabled and running"
    assert_that(host.service("activemq").is_running)
    assert_that(host.service("activemq").is_enabled)

def test_activemq_web_console(host, get_ansible_vars):
    "Check that ActiveMQ web console is available and returns a HTTP 200 for the home page"
    cmd = host.run("curl -iL --user admin:admin http://{}:8161".format(get_ansible_vars["activemq_host"]))
    assert_that(cmd.stdout, contains_string("Welcome to the Apache ActiveMQ!"))
    assert_that(cmd.stdout, contains_string("200 OK"))
