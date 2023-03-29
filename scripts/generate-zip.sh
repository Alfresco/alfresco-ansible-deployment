#!/bin/bash -e

if [ -z "$VERSION" ]; then
    echo "VERSION must be set"
    exit 1
fi

# variables
REPO_ROOT_DIR="$(realpath $(dirname $0)/..)"
ARTIFACT_NAME="alfresco-ansible-deployment-${VERSION}"

echo "create distribution folder"
BUILD_DIR=$(mktemp -d)
pushd "$BUILD_DIR" && cp -a "${REPO_ROOT_DIR}" "$ARTIFACT_NAME"

echo "# Run the helper scripts/generate-secrets.sh to kick start your Ansible vault" \
	> "${ARTIFACT_NAME}/vars/secrets.yml"

echo "Generating ZIP file..."
find "$ARTIFACT_NAME" \( -type f \
	! -path './.*' \
	! -path './tests/*' \
	! -path '*/molecule/*' \
	! -name '*.puml' \
	! -path './scripts/*' \
	! -name alfresco-ansible.pem.enc \
	-o -path ./scripts/generate-secret.sh \
	-o -path ./scripts/vagrant_provision.sh \
	-o -name .envrc \) \
	-exec zip "${REPO_ROOT_DIR}/{ARTIFACT_NAME}.zip" {} +
