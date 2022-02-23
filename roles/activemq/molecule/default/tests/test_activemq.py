"""ActiveMQ Tests"""
import os
import pytest
from hamcrest import assert_that, contains_string

# pylint: disable=redefined-outer-name
@pytest.fixture(scope="module")
def get_ansible_vars(host):
    """Define get_ansible_vars"""
    java_role = "file=../java/vars/main.yml name=java_role"
    activemq_role = "file=./vars/main.yml name=activemq_role"
    common_vars = "file=../common/vars/main.yml name=common_vars"
    common_defaults = "file=../common/defaults/main.yml name=common_defaults"
    common_hosts = "file=../common/vars/hosts.yml name=common_hosts"
    group_vars = "file=../../group_vars/all.yml name=group_vars"
    ansible_vars = host.ansible("include_vars", java_role)["ansible_facts"]["java_role"]
    ansible_vars.update(host.ansible("include_vars", java_role)["ansible_facts"]["java_role"])
    ansible_vars.update(host.ansible("include_vars", common_vars)["ansible_facts"]["common_vars"])
    ansible_vars.update(host.ansible("include_vars", common_hosts)["ansible_facts"]["common_hosts"])
    ansible_vars.update(host.ansible("include_vars", common_defaults)["ansible_facts"]["common_defaults"])
    ansible_vars.update(host.ansible("include_vars", activemq_role)["ansible_facts"]["activemq_role"])
    ansible_vars.update(host.ansible("include_vars", group_vars)["ansible_facts"]["group_vars"])
    return ansible_vars

test_host = os.environ.get('TEST_HOST')

def test_activemq_exe_exists(host, get_ansible_vars):
    "Check that ActiveMQ executable exists"
    assert_that(host.file("/opt/apache-activemq-{}/bin/activemq".format(get_ansible_vars["dependencies_version"]["activemq"])).exists, get_ansible_vars["activemq_home"])

def test_activemq_version(host, get_ansible_vars):
    "Check that ActiveMQ version is correct"
    cmd = host.run(". {}/setenv.sh && $ACTIVEMQ_HOME/bin/activemq --version".format(get_ansible_vars["config_folder"]))
    assert_that(cmd.stdout, contains_string("ActiveMQ {}".format(get_ansible_vars["dependencies_version"]["activemq"])))

def test_activemq_home(host, get_ansible_vars):
    "Check that ActiveMQ home is set correctly"
    cmd = host.run(". {}/setenv.sh && echo $ACTIVEMQ_HOME".format(get_ansible_vars["config_folder"]))
    assert_that(cmd.stdout, contains_string("/opt/apache-activemq-{}".format(get_ansible_vars["dependencies_version"]["activemq"])))

def test_activemq_service(host, get_ansible_vars):
    "Check that ActiveMQ is enabled and running"
    assert_that(host.service("activemq").is_running)
    assert_that(host.service("activemq").is_enabled)

def test_activemq_web_console(host, get_ansible_vars):
    "Check that ActiveMQ web console is available and returns a HTTP 200 for the home page"
    cmd = host.run("curl -iL --user admin:admin http://{}:8161".format(test_host))
    assert_that(cmd.stdout, contains_string("Welcome to the Apache ActiveMQ!"))
    assert_that(cmd.stdout, contains_string("200 OK"))

def test_environment_jvm_opts(host, get_ansible_vars):
    "Check that overwritten JVM_OPTS are taken into consideration"
    pid = host.run("/opt/openjdk*/bin/jps -lV | grep activemq | awk '{print $1}'")
    process_map = host.run("/opt/openjdk*/bin/jhsdb jmap --heap --pid {}".format(pid.stdout))
    assert_that(process_map.stdout, contains_string("MaxHeapSize              = 943718400 (900.0MB)"))
