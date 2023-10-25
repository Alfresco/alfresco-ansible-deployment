"""Transform Tests"""
import os
import pytest
from hamcrest import contains_string, assert_that, has_length

test_host = os.environ.get('TEST_HOST')


# pylint: disable=redefined-outer-name
@pytest.fixture(scope="module")
def get_ansible_vars(host):
    """Define get_ansible_vars"""
    java_role = "file=../java/vars/main.yml name=java_role"
    common_vars = "file=../../../common/vars/main.yml name=common_vars"
    common_defaults = "file=../../../common/defaults/main.yml name=common_defaults"
    common_hosts = "file=../../../common/vars/hosts.yml name=common_hosts"
    transform_services = "file=../../vars/main.yml name=transform_services"
    ansible_vars = host.ansible("include_vars", java_role)["ansible_facts"]["java_role"]
    ansible_vars.update(host.ansible("include_vars", java_role)["ansible_facts"]["java_role"])
    ansible_vars.update(host.ansible("include_vars", common_vars)["ansible_facts"]["common_vars"])
    ansible_vars.update(host.ansible("include_vars", common_hosts)["ansible_facts"]["common_hosts"])
    ansible_vars.update(host.ansible("include_vars", common_defaults)["ansible_facts"]["common_defaults"])
    ansible_vars.update(host.ansible("include_vars", transform_services)["ansible_facts"]["transform_services"])
    return ansible_vars

def test_aio_log_exists(host, get_ansible_vars):
    """Check that Transform AIO log exists"""
    with host.sudo(get_ansible_vars['username']):
        assert_that(host.file("{}/ats-ate-aio.log".format(get_ansible_vars["logs_folder"])).exists, get_ansible_vars["logs_folder"])

def test_aio_service(host):
    """Check that Transform AIO is enabled and running"""
    assert_that(host.service("alfresco-tengine-aio").is_running)
    assert_that(host.service("alfresco-tengine-aio").is_enabled)

def test_aio_config_api(host):
    """Check that Transform AIO transform/config api works"""
    cmd = host.run("curl -iL http://{}:8090/transform/config".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 200"))
    assert_that(cmd.stdout, contains_string("pdfRendererOptions"))
    assert_that(cmd.stdout, contains_string("archiveOptions"))
    assert_that(cmd.stdout, contains_string("imageMagickOptions"))
    assert_that(cmd.stdout, contains_string("tikaOptions"))
    assert_that(cmd.stdout, contains_string("pdfboxOptions"))
    assert_that(cmd.stdout, contains_string("textToPdfOptions"))
    assert_that(cmd.stdout, contains_string("stringOptions"))

def test_environment_jvm_opts(host):
    "Check that overwritten JVM_OPTS are taken into consideration"
    java_processes = host.process.filter(user="alfresco", comm="java")
    assert_that(java_processes, has_length(2))
    for java_process in java_processes:
        if 'imagemagick' in java_process.args:
            assert_that(java_process.args, contains_string('-Xmx900m'))
            assert_that(java_process.args, contains_string('-Xms512m'))

def test_libreoffice_install(host):
    """Check that libreoffice binary doesn't miss any dependencies"""
    p = host.run("/opt/libreoffice7.2/program/soffice.bin --version")
    assert_that(p.stdout, contains_string("LibreOffice 7.2.5.1 6d497ff5e83a906a307eb25cce314d40c0b8624f"))

def test_no_ghostscript(host):
    host.run_expect([127], "gs")
    host.run_expect([127], "ghostscript")
