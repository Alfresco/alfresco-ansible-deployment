#!/bin/bash

export JAVA_HOME="{{ java_home }}"
export PATH="${JAVA_HOME}/bin:${PATH}"

export PATH=$PATH:{{ tomcat_instance }}/bin:$JAVA_HOME/bin
export TOMCAT_NATIVE_LIBDIR={{ tomcat_instance }}/native-jni-lib
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}$TOMCAT_NATIVE_LIBDIR