Vagrant.configure("2") do |config|
  config.vm.provision "shell", path: "./scripts/vagrant_provision.sh"
  config.vm.box = "ubuntu/focal64"
  config.vm.network "private_network", ip: "192.168.56.100"
  config.vm.network "forwarded_port", guest: 80, host: 80
  config.vm.provider "virtualbox" do |v|
    v.memory = 10240
    v.cpus = 4
  end
end
