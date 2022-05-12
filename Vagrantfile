Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.network "private_network", ip: "192.168.56.100"
  config.vm.provider "virtualbox" do |v|
    v.memory = 10240
    v.cpus = 4
  end
  config.vm.provision :ansible_local do |ansible|
    ansible.playbook = "playbooks/acs.yml"
    ansible.inventory_path = "inventory_local.yml"
    ansible.limit = "all"
    ansible.become = true
    ansible.install_mode = "pip_args_only"
    ansible.pip_args = "-r /vagrant/requirements.txt"
    ansible.pip_install_cmd = "sudo apt-get install -y python3-pip python-is-python3 haveged && sudo ln -s -f /usr/bin/pip3 /usr/bin/pip"
    ansible.galaxy_role_file = "requirements.yml"
    ansible.extra_vars = {
      nexus_user: ENV['NEXUS_USERNAME'],
      nexus_password: ENV['NEXUS_PASSWORD'],
      test_environment: true
    }
  end
end
