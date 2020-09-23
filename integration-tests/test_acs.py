"""ACS Base Integration Tests"""
import time
import pytest
from hamcrest import contains_string, assert_that

# pylint: disable=redefined-outer-name
@pytest.fixture()
def AnsibleVars(host):
    """Define AnsibleVars"""
    nginx_role = "file=../../roles/nginx/vars/main.yml name=nginx_role"
    adw_role = "file=../../roles/adw/vars/main.yml name=adw_role"
    transformation_role = "file=../../roles/transformation-services/vars/main.yml name=transformation_role"
    java_role = "file=../../roles/java/vars/main.yml name=java_role"
    tomcat_role = "file=../../roles/tomcat/vars/main.yml name=tomcat_role"
    repository_role = "file=../../roles/repository/vars/main.yml name=repository_role"
    solr_role = "file=../../roles/solr/vars/main.yml name=solr_role"
    ansible_vars = host.ansible("include_vars", adw_role)["ansible_facts"]["adw_role"]
    ansible_vars.update(host.ansible("include_vars", transformation_role)["ansible_facts"]["transformation_role"])
    ansible_vars.update(host.ansible("include_vars", java_role)["ansible_facts"]["java_role"])
    ansible_vars.update(host.ansible("include_vars", nginx_role)["ansible_facts"]["nginx_role"])
    ansible_vars.update(host.ansible("include_vars", tomcat_role)["ansible_facts"]["tomcat_role"])
    ansible_vars.update(host.ansible("include_vars", repository_role)["ansible_facts"]["repository_role"])
    ansible_vars.update(host.ansible("include_vars", solr_role)["ansible_facts"]["solr_role"])
    return ansible_vars

def test_solr_service_is_running_and_enabled(host, AnsibleVars):
    """Check solr service"""
    solr = host.service("solr.service")
    assert_that(solr.is_running)
    assert_that(solr.is_enabled)

def test_repo_service_is_running_and_enabled(host, AnsibleVars):
    """Check repository service"""
    repository = host.service("tomcat_{}.service".format(AnsibleVars["instance_name"]))
    assert_that(repository.is_running)
    assert_that(repository.is_enabled)

def test_postgres_is_installed(host, pkg):
    """Check postgres package"""
    postgres = host.package("postgresql11")
    assert_that(postgres.is_installed)

def test_postgres_running_and_enabled(host, svc):
    """Check postgres service"""
    postgres = host.service("postgresql-11")
    assert_that(postgres.is_running)
    assert_that(postgres.is_enabled)

def test_activemq_running_and_enabled(host, AnsibleVars):
    """Check activemq service"""
    activemq = host.service("activemq.service")
    assert_that(activemq.is_running)
    assert_that(activemq.is_enabled)

def test_transformation_service_is_running_and_enabled(host, AnsibleVars):
    """Check aio service"""
    aio = host.service("aio.service")
    assert_that(aio.is_running)
    assert_that(aio.is_enabled)

def test_share_is_accesible(host, AnsibleVars):
    """Check share service"""
    timeout = time.time() + 10
    output = None
    command = False
    while not command or time.time() < timeout:
        run_command = host.run("curl -v -k --connect-timeout 5 --location --request GET 'https://{}/share/page/'".format(AnsibleVars['nginx_domain']))
        command = run_command.succeeded
        output = run_command.stdout
    assert_that(output,contains_string("Alfresco Identity Service"))

def test_transformation_stats_is_accesible(host, AnsibleVars):
    """Check aio console """
    timeout = time.time() + 10
    output = None
    command = False
    while not command or time.time() < timeout:
        run_command = host.run("curl -v -k --connect-timeout 5 https://{}/aio/".format(AnsibleVars['nginx_domain']))
        command = run_command.succeeded
        output = run_command.stdout
    assert_that(output,contains_string("All in One"))

def test_adw_is_accesible(host, AnsibleVars):
    """Check adw console """
    timeout = time.time() + 10
    output = None
    command = False
    while not command or time.time() < timeout:
        run_command = host.run("curl -v -k --connect-timeout 5 https://{}/".format(AnsibleVars['nginx_domain']))
        command = run_command.succeeded
        output = run_command.stdout
    assert_that(output,contains_string("Alfresco Digital Workspace"))

def test_solr_stats_is_accesible(host, AnsibleVars):
    """Check solrstats service"""
    timeout = time.time() + 10
    output = None
    command = False
    while not command or time.time() < timeout:
        run_command = host.run("curl -v -k --connect-timeout 5 --user admin:admin https://{}/alfresco/s/api/solrstats".format(AnsibleVars['nginx_domain']))
        command = run_command.succeeded
        output = run_command.stdout
    assert_that(output,contains_string("queryInfo"))
