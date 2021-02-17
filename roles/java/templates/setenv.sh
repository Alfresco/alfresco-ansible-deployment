#!/bin/sh

export JAVA_HOME="{{ java_home }}"
export PATH="${JAVA_HOME}/bin:${PATH}"
chmod -R u+rwx,g+rw,o-rwx {{ logs_folder }}/