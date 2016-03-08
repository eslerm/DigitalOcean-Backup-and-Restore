Vagrant.configure('2') do |config|

    config.vm.box = 'ubuntu/trusty64'

    config.vm.synced_folder '.', '/home/vagrant/do_starbound'

    # Temporarily required due to Vagrant/Ansible2.0 ansible-galaxy status codes bug.
    config.vm.synced_folder '.', '/vagrant'

    config.vm.provider 'virtualbox' do |v|
        v.name = 'Starbound DigitalOcean Management'
        v.customize ['modifyvm', :id, '--memory', '1024', '--cpus', '1']
    end

    # Temporarily required due to Vagrant/Ansible2.0 bug, REMOVE ASAP.
    config.vm.provision "shell" do |s|
        s.inline = '[[ ! -f $1 ]] || grep -F -q "$2" $1 || sed -i "/__main__/a \\    $2" $1'
        s.args = ['/usr/bin/ansible-galaxy', "if sys.argv == ['/usr/bin/ansible-galaxy', '--help']: sys.argv.insert(1, 'info')"]
    end 

    config.vm.provision 'ansible_local' do |ansible|
        ansible.playbook = 'provision/playbook.yml'
        ansible.sudo = true
    end

end
