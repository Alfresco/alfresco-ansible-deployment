"""Postgresql Tests"""
import os
from hamcrest import assert_that


def test_postgresql_service(host):
    """Ensure postgres is up and basic functionality is working"""
    pghost = host.ansible.get_variables()['inventory_hostname']
    if os.environ['TEST_IMAGE'].startswith('ubuntu'):
        service_name = 'postgresql'
    else:
        service_name = 'postgresql-13'

    assert_that(host.service(service_name).is_running)
    assert_that(host.service(service_name).is_enabled)
    with host.sudo('postgres'):
        host.run_expect([0], "psql alfresco -c 'SELECT 1'")
        host.run_expect([0], "psql alfresco-sync -c 'SELECT 1'")

        host.run_expect([0], "PGPASSWORD=alfresco psql -h {} -U alfresco alfresco -c \"SELECT 1\"".format(pghost))
        host.run_expect([0], "PGPASSWORD=alfresco psql -h {} -U alfresco-sync alfresco-sync -c \"SELECT 1\"".format(pghost))

        host.run_expect([2], "PGPASSWORD=alfresco psql -h {} -U alfresco alfresco-sync -c \"SELECT 1\"".format(pghost))
