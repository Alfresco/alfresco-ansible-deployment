import importlib.util
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parents[2] / "playbooks" / "filter_plugins" / "artifact_server.py"
spec = importlib.util.spec_from_file_location("artifact_server", PLUGIN)
artifact_server_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(artifact_server_module)
artifact_server = artifact_server_module.artifact_server

BOUNDS = ["23.7.3", "25.5.2", "26.2.4"]


@pytest.mark.parametrize(
    "version, bounds, expected",
    [
        ("26.2.4", BOUNDS, "archive"),
        ("23.1.0", BOUNDS, "archive"),
        ("26.2.5", BOUNDS, "cloudsmith"),
        ("23.7.4", BOUNDS, "cloudsmith"),
        ("26.3.0-A.11", BOUNDS, "cloudsmith"),
        ("27.0.0", BOUNDS, "cloudsmith"),
        ("1.3.0-85", ["1.3.0-86"], "archive"),
        ("1.3.0-87", ["1.3.0-86"], "cloudsmith"),
        ("5.9.0", [], "cloudsmith"),
        ("5.9.0", None, "cloudsmith"),
        (26.2, ["26.2.4"], "archive"),
    ],
)
def test_artifact_server(version, bounds, expected):
    assert artifact_server(version, bounds) == expected
