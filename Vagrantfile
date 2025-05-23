Vagrant.configure("2") do |config|
  acs_major_version = ENV.fetch('VAGRANT_ACS_MAJOR_VERSION', "25").to_i
  config.vm.provision "shell", path: "./scripts/vagrant_provision.sh", privileged: false, env: {
    "NEXUS_USERNAME" => ENV['NEXUS_USERNAME'],
    "NEXUS_PASSWORD" => ENV['NEXUS_PASSWORD'],
    "VAGRANT_ACS_MAJOR_VERSION" => acs_major_version,
    "ANSIBLE_PIPELINING" => "true",
  }
  config.vm.box = acs_major_version <= 23 ? "bento/ubuntu-22.04" : "bento/ubuntu-24.04"
  config.vm.network "private_network", ip: "192.168.56.100"
  config.vm.network "forwarded_port", guest: 80, host: 80
  config.vm.provider "virtualbox" do |v|
    v.memory = 10240
    v.cpus = 4
  end
end
