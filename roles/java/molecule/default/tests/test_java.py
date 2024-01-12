"""Java Tests"""
import pytest
from hamcrest import contains_string, assert_that


# pylint: disable=redefined-outer-name
@pytest.fixture(scope="module")
def get_ansible_vars(host):
    """Define get_ansible_vars"""
    java_role = "file=../../vars/main.yml name=java_role"
    common_vars = "file=../../../common/vars/main.yml name=common_vars"
    common_defaults = "file=../../../common/defaults/main.yml name=common_defaults"
    group_vars = "file=../../../../group_vars/all.yml name=group_vars"
    ansible_vars = host.ansible(
            "include_vars",
            java_role
            )["ansible_facts"]["java_role"]
    ansible_vars.update(
            host.ansible(
                "include_vars", java_role
                )["ansible_facts"]["java_role"]
            )
    ansible_vars.update(
            host.ansible(
                "include_vars", common_vars
                )["ansible_facts"]["common_vars"]
            )
    ansible_vars.update(
            host.ansible(
                "include_vars", common_defaults
                )["ansible_facts"]["common_defaults"]
            )
    ansible_vars.update(
            host.ansible(
                "include_vars",
                group_vars
                )["ansible_facts"]["group_vars"]
            )
    return ansible_vars


def test_java_exists(host, get_ansible_vars):
    """Check that java executable exists"""
    java_version = get_ansible_vars["dependencies_version"]["java"]
    java_bin = host.file("/opt/openjdk-{}/bin/java".format(java_version))
    assert_that(java_bin.exists, True)


def test_java_version(host, get_ansible_vars):
    """Check that java version is correct"""
    java_version = get_ansible_vars["dependencies_version"]["java"]
    cmd = host.run("/opt/openjdk-{}/bin/java -version".format(java_version))
    assert_that(cmd.stderr, contains_string(java_version))


def test_java_home(host, get_ansible_vars):
    """Check that JAVA_HOME is environment variable is set"""
    java_version = get_ansible_vars["dependencies_version"]["java"]
    with host.sudo():
        cmd = host.run(
                ". {}/setenv.sh && echo $JAVA_HOME".format(
                    get_ansible_vars["config_folder"]
                    )
                )
    assert_that(
            cmd.stdout, contains_string("/opt/openjdk-{}".format(java_version))
            )


def test_keystore(host, get_ansible_vars):
    """Check the Java keytore is populated with certificate"""
    hostname = host.ansible.get_variables()["inventory_hostname"]
    java_version = get_ansible_vars["dependencies_version"]["java"]
    java_home = '/opt/openjdk-' + java_version
    keystore = java_home + '/lib/security/keystore/ansible.jceks'
    cmd_tpl = '{}/bin/keytool -list -keystore {} -storepass alfresco -alias {}'
    with host.sudo():
        cmd = host.run(
                cmd_tpl.format(
                    java_home,
                    keystore,
                    hostname
                    )
                )
    print(cmd.stdout)
    assert_that(cmd.rc == 0)


def test_keystore_seckey(host, get_ansible_vars):
    """Check the Java keytore is populated with certificate"""
    java_version = get_ansible_vars["dependencies_version"]["java"]
    java_home = '/opt/openjdk-' + java_version
    keystore = java_home + '/lib/security/keystore/ansible.jceks'
    cmd_tpl = '{}/bin/keytool -keypasswd -keystore {} -storepass alfresco -keypass "{}" -new "{}" -alias test'
    with host.sudo():
        cmd = host.run(
            cmd_tpl.format(
                java_home,
                keystore,
                "alfresco with space",
                "alfresco with space"
                )
            )
    print(cmd.stdout)
    assert_that(cmd.rc == 0)


def test_truststore(host, get_ansible_vars):
    """Check the Java truststore trusts the CA root signing certificate"""
    java_version = get_ansible_vars["dependencies_version"]["java"]
    cmd = host.run(
            "/opt/openjdk-{}/bin/keytool -list -cacerts".format(java_version)
            )
    print(cmd.stdout)
    assert_that(
            cmd.stdout,
            contains_string('alfresco ansible imported ca')
            )
