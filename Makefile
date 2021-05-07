run:
	ANSIBLE_CFG=ansible.cfg ansible-playbook -i ansible/inventory.toml ansible/mongo.yml