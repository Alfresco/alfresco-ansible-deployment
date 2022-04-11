"""Postgresql Tests"""
import os
from hamcrest import assert_that


def test_postgresql_service(host):
    """Ensure postgres is up and basic functionality is working"""
    if os.environ['TEST_IMAGE'].startswith('ubuntu'):
        service_name = 'postgresql'
    else:
        service_name = 'postgresql-13'

    assert_that(host.service(service_name).is_running)
    assert_that(host.service(service_name).is_enabled)

    host.run_expect([0], "su postgres -c 'psql alfresco -c \"SELECT 1\"'")
    host.run_expect([0], "su postgres -c 'psql alfresco-sync -c \"SELECT 1\"'")

    host.run_expect([0], "PGPASSWORD=alfresco psql -h localhost -U alfresco alfresco -c \"SELECT 1\"")
    host.run_expect([0], "PGPASSWORD=alfresco psql -h localhost -U alfresco-sync alfresco-sync -c \"SELECT 1\"")

    host.run_expect([0], "PGPASSWORD=alfresco psql -h localhost -U alfresco alfresco-sync -c \"SELECT 1\"")
