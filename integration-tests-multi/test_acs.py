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
    transformers = "file=../../roles/transformers/vars/main.yml name=transformers"
    java_role = "file=../../roles/java/vars/main.yml name=java_role"
    tomcat_role = "file=../../roles/tomcat/vars/main.yml name=tomcat_role"
    repository_role = "file=../../roles/repository/vars/main.yml name=repository_role"
    solr_role = "file=../../roles/solr/vars/main.yml name=solr_role"
    common_role = "file=../../roles/common/vars/main.yml name=common_role"
    common_host_role = "file=../../inventory_acs/group_vars/all.yml name=common_host_role"
    ansible_vars = host.ansible("include_vars", adw_role)["ansible_facts"]["adw_role"]
    ansible_vars.update(host.ansible("include_vars", transformers)["ansible_facts"]["transformers"])
    ansible_vars.update(host.ansible("include_vars", java_role)["ansible_facts"]["java_role"])
    ansible_vars.update(host.ansible("include_vars", nginx_role)["ansible_facts"]["nginx_role"])
    ansible_vars.update(host.ansible("include_vars", tomcat_role)["ansible_facts"]["tomcat_role"])
    ansible_vars.update(host.ansible("include_vars", repository_role)["ansible_facts"]["repository_role"])
    ansible_vars.update(host.ansible("include_vars", solr_role)["ansible_facts"]["solr_role"])
    ansible_vars.update(host.ansible("include_vars", common_role)["ansible_facts"]["common_role"])
    ansible_vars.update(host.ansible("include_vars", common_host_role)["ansible_facts"]["common_host_role"])
    return ansible_vars

def test_solr_service_is_running_and_enabled(host, AnsibleVars):
    """Check solr service"""
    solr = host.service("solr.service")
    assert_that(solr.is_running)
    assert_that(solr.is_enabled)

def test_repo_service_is_running_and_enabled(host, AnsibleVars):
    """Check repository service"""
    repository = host.service("alfresco-content.service")
    assert_that(repository.is_running)
    assert_that(repository.is_enabled)

def test_postgres_is_installed(host, AnsibleVars):
    """Check postgres package"""
    postgres = host.package("postgresql11")
    assert_that(postgres.is_installed)

def test_postgres_running_and_enabled(host, AnsibleVars):
    """Check postgres service"""
    postgres = host.service("postgresql-11")
    assert_that(postgres.is_running)
    assert_that(postgres.is_enabled)

def test_activemq_running_and_enabled(host, AnsibleVars):
    """Check activemq service"""
    activemq = host.service("activemq.service")
    assert_that(activemq.is_running)
    assert_that(activemq.is_enabled)

def test_aio_service(host, AnsibleVars):
    "Check that Transform AIO is enabled and running"
    assert_that(host.service("alfresco-tengine-aio").is_running)
    assert_that(host.service("alfresco-tengine-aio").is_enabled)
    assert_that(host.service("alfresco-transform").is_running)
    assert_that(host.service("alfresco-transform").is_enabled)

def test_share_is_accesible(host, AnsibleVars):
    """Check share service"""
    timeout = time.time() + 10
    output = None
    command = False
    while not command or time.time() < timeout:
        run_command = host.run("curl -v -k --connect-timeout 5 --location --request GET 'http://{}/share/page/'".format(AnsibleVars['repo_host']))
        command = run_command.succeeded
        output = run_command.stdout
    assert_that(output,contains_string("2005-2020 Alfresco Software"))

def test_repository_root_is_accesible(host, AnsibleVars):
    """Check repository root service"""
    timeout = time.time() + 10
    output = None
    command = False
    while not command or time.time() < timeout:
        run_command = host.run("curl -v -k --connect-timeout 5 --location --request GET 'http://{}/'".format(AnsibleVars['repo_host']))
        command = run_command.succeeded
        output = run_command.stdout
    assert_that(output,contains_string("Alfresco Repository"))

def test_transformation_stats_is_accesible(host, AnsibleVars):
    """Check aio console """
    timeout = time.time() + 10
    output = None
    command = False
    while not command or time.time() < timeout:
        run_command = host.run("curl -v -k --connect-timeout 5 http://{}/aio/".format(AnsibleVars['repo_host']))
        command = run_command.succeeded
        output = run_command.stdout
    assert_that(output,contains_string("All in One"))

def test_adw_is_accesible(host, AnsibleVars):
    """Check adw console """
    timeout = time.time() + 10
    output = None
    command = False
    while not command or time.time() < timeout:
        run_command = host.run("curl -v -k --connect-timeout 5 http://{}/workspace/".format(AnsibleVars['repo_host']))
        command = run_command.succeeded
        output = run_command.stdout
    assert_that(output,contains_string("Alfresco Digital Workspace"))

def test_solr_stats_is_accesible(host, AnsibleVars):
    """Check solrstats service"""
    timeout = time.time() + 10
    output = None
    command = False
    while not command or time.time() < timeout:
        run_command = host.run("curl -v -k --connect-timeout 5 --user admin:admin http://{}/alfresco/s/api/solrstats".format(AnsibleVars['repo_host']))
        command = run_command.succeeded
        output = run_command.stdout
    assert_that(output,contains_string("queryInfo"))
