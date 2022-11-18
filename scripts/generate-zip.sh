#!/bin/bash -e

if [ -z "$VERSION" ]; then
    echo "VERSION must be set"
    exit 1
fi

# variables
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REPO_ROOT_DIR="${SCRIPT_DIR}/.."
ARTIFACT_DIR_NAME="alfresco-ansible-deployment-${VERSION}"
BUILD_DIR="${REPO_ROOT_DIR}/dist/${ARTIFACT_DIR_NAME}"
ARTIFACT_NAME="${ARTIFACT_DIR_NAME}.zip"

echo "create distribution folder"
mkdir -p "$BUILD_DIR"

cd "$REPO_ROOT_DIR"

echo "Adding main playbook resources"
echo "You can find full documentation on how to use the playbook for Enterprise deployments here https://docs.alfresco.com/content-services/latest/install/ansible and for Community deployments here https://docs.alfresco.com/content-services/community/install/ansible" > "$BUILD_DIR/README.txt"
cp -r configuration_files "$BUILD_DIR"
cp -r docs "$BUILD_DIR"
cp -r group_vars "$BUILD_DIR"
cp -r playbooks "$BUILD_DIR"
rsync -rvq --exclude molecule/ roles "$BUILD_DIR"
cp inventory_*.yml "$BUILD_DIR"
cp ./*.md "$BUILD_DIR"
cp LICENSE "$BUILD_DIR"
cp ./*-extra-vars.yml "$BUILD_DIR"

echo "Adding vagrant support"
cp Vagrantfile "$BUILD_DIR"
mkdir "$BUILD_DIR/scripts"
cp scripts/vagrant_provision.sh "$BUILD_DIR/scripts"

echo "Adding Ansible Galaxy support"
cp requirements.yml "$BUILD_DIR"

echo "Adding Pipenv support"
cp Pipfile Pipfile.lock "$BUILD_DIR"

echo ""
echo "Generating ZIP file..."
cd "$REPO_ROOT_DIR/dist"
zip -r "$ARTIFACT_NAME" "$ARTIFACT_DIR_NAME"

echo "Done"
