user     = ENV['NEXUS_USERNAME']
pass     = ENV['NEXUS_PASSWORD']

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
  config.vm.network "private_network", ip: "192.168.56.100"
  config.vm.provider "virtualbox" do |v|
    v.memory = 10240
    v.cpus = 4
  end
  config.vm.provision "shell",
    inline: "echo -e 'export NEXUS_USERNAME=\""+user+"\"\nexport NEXUS_PASSWORD=\""+pass+"\"\n' >> /home/vagrant/.bashrc"
  config.vm.provision :ansible_local do |ansible|
    ansible.playbook = "playbooks/acs.yml"
    ansible.inventory_path = "inventory_local.yml"
    ansible.limit = "all"
    ansible.become = true
    ansible.install_mode = "pip_args_only"
    ansible.pip_args = "-r /vagrant/requirements.txt"
    ansible.pip_install_cmd = "sudo apt-get install -y python3 && curl -s https://bootstrap.pypa.io/get-pip.py | sudo python3"
    ansible.galaxy_role_file = "requirements.yml"
  end
end
