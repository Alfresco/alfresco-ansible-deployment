"""Java Tests"""
import pytest
from hamcrest import contains_string, assert_that

@pytest.fixture()
def get_ansible_vars(host):
    """Define AnsibleVars"""
    java_role = "file=../../roles/java/vars/main.yml name=java_role"
    ansible_vars = host.ansible("include_vars", java_role)["ansible_facts"]["java_role"]
    ansible_vars.update(host.ansible("include_vars", java_role)["ansible_facts"]["java_role"])
    return ansible_vars

def test_java_exists(host, ansible_vars):
    "Check that java executable exists"
    cmd = host.run("[ -f /opt/openjdk-{}/bin/java ] && echo \"File exists\" || echo \"File does not exists\"".format(ansible_vars["jdk_version"]))
    assert_that(cmd.stdout, contains_string("File exists"))

def test_java_version(host, ansible_vars):
    "Check that java version is correct"
    cmd = host.run("/opt/openjdk-{}/bin/java -version".format(ansible_vars["jdk_version"]))
    assert_that(cmd.stderr, contains_string(ansible_vars["jdk_version"]))

def test_java_home(host, ansible_vars):
    "Check that JAVA_HOME is environment variable is set"
    cmd = host.run("source {}/setenv.sh && echo $JAVA_HOME".format(ansible_vars["config_dir"]))
    assert_that(cmd.stdout, contains_string("/opt/openjdk-{}".format(ansible_vars["jdk_version"])))
