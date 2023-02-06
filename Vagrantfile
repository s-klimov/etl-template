# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"

  config.vm.network "forwarded_port", guest: 8000, host: 8001
  config.vm.network "forwarded_port", guest: 5432, host: 5433
  config.vm.provider "virtualbox" do |v|
    v.customize ["modifyvm", :id, "--uart1", "0x3F8", "4"]
    v.customize ["modifyvm", :id, "--uartmode1", "file", File::NULL]
    v.memory = 2048
  end

  # ansible_local
  config.vm.provision "ansible_local" do |ansible|
    ansible.verbose = "vv"
    ansible.galaxy_role_file = 'vagrant/requirements.yml'
    ansible.galaxy_roles_path = '/home/vagrant/.ansible/roles'
    ansible.galaxy_command = 'ansible-galaxy install --ignore-errors --force --role-file=%{role_file}'
    ansible.playbook = "vagrant/playbook.yml"
  end
end
