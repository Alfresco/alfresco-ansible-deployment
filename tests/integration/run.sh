#!/usr/bin/env bash
# Check every Alfresco artifact routes to the expected server and credentials.
set -euo pipefail

cd "$(dirname "$0")"

export NEXUS_USERNAME=nexus-user NEXUS_PASSWORD=nexus-pass
export CLOUDSMITH_USERNAME=cloudsmith-user CLOUDSMITH_API_KEY=cloudsmith-key

run() {
  ansible-playbook -i inventory.yml test.yml "$@"
}

for major in 23 25 26; do
  run -e acs_play_major_version="$major"
done
run -e acs_play_repository_acs_edition=Community
run -e @newer-versions.yml -e expected_server=cloudsmith
run -e @newer-versions.yml -e expected_server=cloudsmith -e acs_play_repository_acs_edition=Community
