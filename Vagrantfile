user     = ENV['NEXUS_USERNAME']
pass     = ENV['NEXUS_PASSWORD']

Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"
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
  end
end
