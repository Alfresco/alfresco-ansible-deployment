#!/bin/bash
set -e

# find location of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# create dist folder
mkdir -p $SCRIPT_DIR/../dist
cd $SCRIPT_DIR/../dist

# read version from file
VERSION=`cat ../VERSION`

# create temporary folder with required files
echo "Copying required files to temporary folder..."
BUILD_FOLDER=alfresco-ansible-deployment-${VERSION}
mkdir -p $BUILD_FOLDER
echo "For more info on this project goto https://github.com/Alfresco/alfresco-ansible-deployment/blob/master/README.md" > $BUILD_FOLDER/README.txt
cp -r ../group_vars $BUILD_FOLDER
cp -r ../playbooks $BUILD_FOLDER
rsync -rvq --exclude molecule/ ../roles $BUILD_FOLDER
cp ../inventory_* $BUILD_FOLDER
cp ../LICENSE $BUILD_FOLDER
cp ../VERSION $BUILD_FOLDER
cp ../6.2.N-extra-vars.yml $BUILD_FOLDER
cp ../community-extra-vars.yml $BUILD_FOLDER
cp -r ../configuration_files $BUILD_FOLDER

# generate ZIP
echo "Generating ZIP file..."
zip -r alfresco-ansible-deployment-${VERSION}.zip $BUILD_FOLDER

# cleanup
echo "Removing temporary folder..."
rm -rf $BUILD_FOLDER