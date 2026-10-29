from ansible.module_utils.compat.version import LooseVersion


def artifact_server(version, archive_bounds):
    """Return 'archive' when version was published on the archive server, else 'cloudsmith'.

    archive_bounds holds the last archived version of each release line, matched on major version.
    """
    version = str(version)
    major = version.split(".")[0]
    for bound in archive_bounds or []:
        bound = str(bound)
        if bound.split(".")[0] == major and LooseVersion(version) <= LooseVersion(bound):
            return "archive"
    return "cloudsmith"


class FilterModule:
    def filters(self):
        return {"artifact_server": artifact_server}
