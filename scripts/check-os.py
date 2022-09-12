import platform

supported_distribution = ["RHEL", "CentOS", "Ubuntu"]
supported_versions_rhel = ["8.4", "8.2", "7.7", "7.6"]
supported_versions_centos = ["7 x64",]
supported_versions_ubuntu = ["20.04", "18.04"]

distro = platform.release()
version = platform.version()
if distro in supported_distribution:
    temp = supported_distribution[distro]
    if temp == 0:
        if version[0:3] not in supported_versions_rhel:
            print("You are on not supported RHEL version")
        else:
            pass
    elif temp == 1:
        if version[0:5] not in supported_versions_centos:
            print("You are on not supported CentOS version")
        else:
            pass
    elif temp == 2:
        if version[0:6] not in supported_versions_ubuntu:
            print("You are on not supported Ubuntu version")
else: 
    print("You are on not supported OS distribution!")
