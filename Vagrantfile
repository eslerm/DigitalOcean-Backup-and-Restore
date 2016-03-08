Vagrant.configure('2') do |config|

	config.vm.box = 'ubuntu/trusty64'

	config.vm.synced_folder ".", "/home/vagrant/do_starbound"

	config.vm.provider "virtualbox" do |v|
		v.name = "Starbound DigitalOcean Management"
		v.customize ["modifyvm", :id, "--memory", "1024", "--cpus", "1"]
	end

end
