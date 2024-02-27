Vagrant.configure("2") do |config|
  config.vm.provision "shell", path: "./scripts/vagrant_provision.sh", env: {
    "NEXUS_USERNAME" => ENV['NEXUS_USERNAME'],
    "NEXUS_PASSWORD" => ENV['NEXUS_PASSWORD'],
  }
  config.vm.box = "ubuntu/jammy64"
  # config.vm.network "private_network", ip: "192.168.56.100"
  # config.vm.network "forwarded_port", guest: 80, host: 80
  config.vm.provider "virtualbox" do |v|
    v.memory = 8096
    v.cpus   = 1
  end
end
