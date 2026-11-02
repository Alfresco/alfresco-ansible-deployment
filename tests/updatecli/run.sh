#!/usr/bin/env bash
# Check every Maven source of the bump pipeline uses the selected artifact server.
set -euo pipefail

cd "$(dirname "$0")/../.."

archive_repo='nexus-user:nexus-pass@nexus.alfresco.com/nexus/repository/private'
cloudsmith_repo='cloudsmith-user:cloudsmith-key@artifacts.hyland.dev/basic/alfresco-private/maven'

render() {
  updatecli manifest show --config .github/updatecli/updatecli_maven.tpl \
    -v tests/updatecli/matrix.yml \
    -v .github/updatecli/updatecli_maven_values.yml "$@"
}

check() {
  local label=$1 expected=$2 manifest=$3
  local sources
  sources=$(grep -c '^ *repository: ' <<<"$manifest" || true)
  if [ "$sources" -eq 0 ]; then
    echo "FAIL $label: no maven source rendered" >&2
    exit 1
  fi
  local other
  other=$(grep '^ *repository: ' <<<"$manifest" | grep -vc "repository: $expected\$" || true)
  if [ "$other" -ne 0 ]; then
    echo "FAIL $label: expected all $sources sources on $expected" >&2
    grep '^ *repository: ' <<<"$manifest" | sort | uniq -c >&2
    exit 1
  fi
  echo "OK   $label ($sources sources)"
}

for version_file in .github/updatecli/updatecli_maven_*_values.yml; do
  export NEXUS_USERNAME=nexus-user NEXUS_PASSWORD=nexus-pass
  unset CLOUDSMITH_USERNAME CLOUDSMITH_API_KEY
  check "archive $version_file" "$archive_repo" "$(render -v "$version_file")"

  export CLOUDSMITH_USERNAME=cloudsmith-user CLOUDSMITH_API_KEY=cloudsmith-key
  unset NEXUS_USERNAME NEXUS_PASSWORD
  check "cloudsmith $version_file" "$cloudsmith_repo" "$(render -v "$version_file" -v tests/updatecli/cloudsmith.yml)"
done
