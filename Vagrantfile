Vagrant.configure("2") do |config|
  config.vm.provision "shell", path: "install_pipenv.sh"
  config.vm.box = "ubuntu/focal64"
  config.vm.network "private_network", ip: "192.168.56.100"
  config.vm.network "forwarded_port", guest: 80, host: 80
  config.vm.provider "virtualbox" do |v|
    v.memory = 10240
    v.cpus = 4
  end
  config.vm.provision :ansible_local do |ansible|
    ansible.playbook = "playbooks/acs.yml"
    ansible.inventory_path = "inventory_local.yml"
    ansible.limit = "all"
    ansible.become = true
    ansible.galaxy_role_file = "requirements.yml"
    ansible.extra_vars = {
      nexus_user: ENV['NEXUS_USERNAME'],
      nexus_password: ENV['NEXUS_PASSWORD'],
      autogen_unsecure_secrets: true
    }
  end
end