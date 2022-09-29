"""Repo Tests"""
import os
import time
import string
import random
import json
import pytest
from hamcrest import assert_that, contains_string, has_length

test_host = os.environ.get('TEST_HOST')


@pytest.fixture(scope="module")
def get_ansible_vars(host):
    """Define get_ansible_vars"""
    repository_role = "file=./vars/main.yml name=repository_role"
    tomcat_role = "file=../tomcat/vars/main.yml name=tomcat_role"
    java_role = "file=../java/vars/main.yml name=java_role"
    common_vars = "file=../common/vars/main.yml name=common_vars"
    common_defaults = "file=../common/defaults/main.yml name=common_defaults"
    group_vars = "file=../../group_vars/all.yml name=group_vars"
    ansible_vars = host.ansible("include_vars", group_vars)["ansible_facts"]["group_vars"]
    ansible_vars.update(host.ansible("include_vars", common_defaults)["ansible_facts"]["common_defaults"])
    ansible_vars.update(host.ansible("include_vars", common_vars)["ansible_facts"]["common_vars"])
    ansible_vars.update(host.ansible("include_vars", java_role)["ansible_facts"]["java_role"])
    ansible_vars.update(host.ansible("include_vars", tomcat_role)["ansible_facts"]["tomcat_role"])
    ansible_vars.update(host.ansible("include_vars", repository_role)["ansible_facts"]["repository_role"])
    return ansible_vars

def brute_lock_admin(host):
    """
    Force locking user after N auth failures
    """
    login_api_endpoint = '/alfresco/api/-default-/public/authentication/versions/1/tickets'
    api_headers = 'Content-Type: application/json'
    repovars = host.ansible.get_variables()
    iternum = int(repovars['repository_properties']['authentication']['protection']['limit'])
    for _ in range(iternum):
        login_payload = '{"userId":"admin","password":"' + ''.join(random.choice(string.ascii_lowercase) for i in range(3)) + '"}'
        host.run("curl http://{}:8080{} -H '{}' -d '{}'".format(
            test_host,
            login_api_endpoint,
            api_headers,
            login_payload
            )
        )


def test_bruteforce_mitigation(host):
    """
    Check wether bruteforce protection is properly configured
    """
    brute_lock_admin(host)
    login_api_endpoint = '/alfresco/api/-default-/public/authentication/versions/1/tickets'
    api_headers = 'Content-Type: application/json'
    login_payload = '{"userId":"admin","password": "admin"}'
    repovars = host.ansible.get_variables()
    cmd = host.run("curl http://{}:8080{} -H '{}' -d '{}'".format(test_host,
                   login_api_endpoint, api_headers, login_payload))
    assert_that(json.loads(cmd.stdout)['error']['errorKey'] == 'Login failed')
    time.sleep(repovars['repository_properties']['authentication']['protection']['periodSeconds'])
    cmd = host.run("curl http://{}:8080{} -H '{}' -d '{}'".format(test_host,
                   login_api_endpoint, api_headers, login_payload))
    assert_that(json.loads(cmd.stdout)['entry']['userId'] == 'admin')

def test_repo_service_is_running_and_enabled(host):
    """Check repository service"""
    repository = host.service("alfresco-content.service")
    assert_that(repository.is_running)
    assert_that(repository.is_enabled)

def test_alfresco_log_exists(host):
    "Check that alfresco.log exists in /var/log/alfresco"
    with host.sudo():
        assert_that(host.file("/var/log/alfresco/alfresco.log").exists)

def test_alfresco_context_200(host):
    "Check that /alfresco context is available and returns a HTTP 200 status code"
    with host.sudo():
        cmd = host.run("curl -iL --user admin:admin --connect-timeout 5 http://{}:8080/alfresco".format(test_host))
    assert_that(cmd.stdout, contains_string("Welcome to Alfresco"), test_host)
    assert_that(cmd.stdout, contains_string("HTTP/1.1 200"))

def test_alfresco_api(host):
    "Check the repository is installed correctly by calling the discovery API (/alfresco/api/discovery)"
    cmd = host.run("curl -L --user admin:admin --connect-timeout 5 http://{}:8080/alfresco/api/discovery".format(test_host))
    response = json.loads(cmd.stdout)
    acs_version = host.ansible.get_variables()['acs']['version']
    if '-' in acs_version:
        # Remove optional -Ax postfix in acs version
        acs_version_split = acs_version.split('-')
        acs_version = acs_version_split[:-1][0]
    assert_that(response['entry']['repository']['version']['display'], contains_string(acs_version))

def test_share_log_exists(host):
    "Check that share.log exists in /var/log/alfresco"
    with host.sudo():
        assert_that(host.file("/var/log/alfresco/share.log").exists)

def test_share_context_200(host):
    "Check that /share context is available and returns a HTTP 200 status code"
    cmd = host.run("curl -iL --user admin:admin --connect-timeout 5 http://{}:8080/share".format(test_host))
    assert_that(cmd.stdout, contains_string("Alfresco Share"))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 200"))

def test_vti_bin_context_200(host):
    "Check that /share context is available and returns a HTTP 200 status code"
    cmd = host.run("curl -iL --user admin:admin --connect-timeout 5 http://{}:8080/_vti_bin/".format(test_host))
    assert_that(cmd.stdout, contains_string("Welcome to Alfresco!"))
    assert_that(cmd.stdout, contains_string("This application does not provide a web interface in the browser."))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 200"))

def test_vti_inf_context_200(host):
    "Check that /share context is available and returns a HTTP 200 status code"
    cmd = host.run("curl -iL --user admin:admin --connect-timeout 5 http://{}:8080/_vti_inf.html".format(test_host))
    assert_that(cmd.stdout, contains_string("_vti_bin"))
    assert_that(cmd.stdout, contains_string("FrontPage Configuration Information"))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 200"))

def test_api_explorer_context_200(host):
    "Check that /api-explorer context is available and returns a HTTP 200 status code"
    cmd = host.run("curl -iL --user admin:admin http://{}:8080/api-explorer".format(test_host))
    assert_that(cmd.stdout, contains_string("Alfresco Content Services REST API Explorer"))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 200"))

def test_keytest_keystore_exists(host):
    "Check that the custom keystore exists in /var/opt/alfresco/content-services/keystore/keystest"
    with host.sudo():
        assert_that(host.file("/var/opt/alfresco/content-services/keystore/keystest").exists)

def test_ags_repo_is_installed_and_loaded(host, get_ansible_vars):
    """Check if rm amp is installed in repo war and loaded at startup"""
    java_version = get_ansible_vars["dependencies_version"]["java"]
    acs_version = get_ansible_vars["acs"]["version"]
    with host.sudo():
        cmd = host.run(
                "/opt/openjdk-" + java_version +
                "/bin/java -jar /opt/alfresco/content-services-" + acs_version +
                "/bin/alfresco-mmt.jar list /opt/alfresco/content-services-" + acs_version +
                "/web-server/webapps/alfresco.war"
                )
        getlog = host.file("/var/log/alfresco/alfresco.log")
        assert_that(getlog.contains("Installing module 'alfresco-rm-enterprise-repo' version 3.5.0"))
    assert_that(cmd.stdout, contains_string("AGS Repo\n   -    Version:      3.5.0"))

def test_ags_share_is_installed_and_loaded(host, get_ansible_vars):
    """Check if rm amp is installed in share war and loaded at startup"""
    java_version = get_ansible_vars["dependencies_version"]["java"]
    acs_version = get_ansible_vars["acs"]["version"]
    with host.sudo():
        cmd = host.run(
                "/opt/openjdk-" + java_version +
                "/bin/java -jar /opt/alfresco/content-services-" + acs_version +
                "/bin/alfresco-mmt.jar list /opt/alfresco/content-services-" + acs_version +
                "/web-server/webapps/share.war"
                )
        getlog = host.file("/var/log/alfresco/share.log")
        assert_that(getlog.contains("AGS Enterprise Share, 3.5.0, Alfresco Governance Services Enterprise Share Extension"))
    assert_that(cmd.stdout, contains_string("AGS Enterprise Share\n   -    Version:      3.5.0" ))

def test_environment_jvm_opts(host):
    "Check that overwritten JVM_OPTS are taken into consideration"
    java_processes = host.process.filter(user="alfresco", comm="java")
    assert_that(java_processes, has_length(2))
    for java_process in java_processes:
        if 'org.apache.catalina.startup.Bootstrap' in java_process.args:
            assert_that(java_process.args, contains_string('-Xmx900m'))
            assert_that(java_process.args, contains_string('-Xms350m'))

def test_mounting_storage(host):
    """Check wether Content Store has been properly mounted as per config."""
    dir_root='/var/opt/alfresco/content-services/content'
    repovars = host.ansible.get_variables()
    assert_that(host.mount_point(dir_root).exists == isinstance(repovars["cs_storage"]["device"], str))
    if repovars["cs_storage"]["type"]:
        assert_that(host.mount_point(dir_root).filesystem == repovars["cs_storage"]["type"])
    # Best effort options check: at least find one common option (options may not be returned as passed)
    if repovars["cs_storage"]["options"]:
        assert_that(set(host.mount_point(dir_root).options) & set(repovars["cs_storage"]["options"].split(',')))

def test_newly_added_properties_are_set(host):
    "Check that extra props exists in global properties file"
    with host.sudo():
        content = host.file("/etc/opt/alfresco/content-services/classpath/alfresco-global.properties").content
    assert_that(b'index.recovery.mode=NONE' in content)
    assert_that(b'index.subsystem.name=noindex' in content)
    assert_that(host.socket("tcp://0.0.0.0:1121").is_listening)

def test_no_ghostscript(host):
    p = host.run_expect([1], "command -v gs")
    p = host.run_expect([1], "command -v ghostscript")