Vagrant.configure("2") do |config|
  config.vm.provision "shell", path: "./scripts/vagrant_provision.sh", env: {
    "NEXUS_USERNAME" => ENV['NEXUS_USERNAME'],
    "NEXUS_PASSWORD" => ENV['NEXUS_PASSWORD'],
  }
  config.vm.box = "ubuntu/jammy64"
  config.vm.provider "virtualbox" do |v|
    v.memory = 10240
  end
end
