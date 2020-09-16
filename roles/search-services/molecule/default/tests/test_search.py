"""Solr Tests"""
import time
import pytest
from hamcrest import contains_string, assert_that

# pylint: disable=redefined-outer-name
@pytest.fixture()
def get_ansible_vars(host):
    """Define AnsibleVars"""
    java_role = "file=../../../java/vars/main.yml name=java_role"
    common_vars = "file=../../../common/vars/main.yml name=common_vars"
    common_defaults = "file=../../../common/defaults/main.yml name=common_defaults"
    search_services = "file=../../vars/main.yml name=search_services"
    ansible_vars = host.ansible("include_vars", java_role)["ansible_facts"]["java_role"]
    ansible_vars.update(host.ansible("include_vars", java_role)["ansible_facts"]["java_role"])
    ansible_vars.update(host.ansible("include_vars", common_vars)["ansible_facts"]["common_vars"])
    ansible_vars.update(host.ansible("include_vars", common_defaults)["ansible_facts"]["common_defaults"])
    ansible_vars.update(host.ansible("include_vars", search_services)["ansible_facts"]["search_services"])
    return ansible_vars

def test_solr_log_exists(host, get_ansible_vars):
    "Check that java executable exists"
    assert_that(host.file("{}/solr.log".format(get_ansible_vars["log_dir"])).exists, get_ansible_vars["log_dir"])

@pytest.mark.parametrize("svc", ["solr"])
def test_activemq_running_and_enabled(host, svc):
    """Check activemq service"""
    solr = host.service(svc)
    assert_that(solr.is_running)
    assert_that(solr.is_enabled)

def test_solr_stats_is_accesible(host, AnsibleVars):
    """Check solrstats service"""
    timeout = time.time() + 10
    output = None
    command = False
    while not command or time.time() < timeout:
        run_command = host.run("curl -v -k --connect-timeout 5 --user admin:admin http://localhost:8080/alfresco/s/api/solrstats")
        command = run_command.succeeded
        output = run_command.stdout
    assert_that(output,contains_string("queryInfo"))
