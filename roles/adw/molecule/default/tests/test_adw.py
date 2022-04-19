"""ADW Tests"""
import os
from hamcrest import assert_that, contains_string

test_host = os.environ.get('TEST_HOST')

def test_digital_workspace_200(host):
    "Check that ADW is available and returns a HTTP 200 status code"
    cmd = host.run("curl -iL --user admin:admin http://{}:8880/".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 200"))
