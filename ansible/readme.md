***Ansible AWS Playbooks***

*This repo has some handy AWS Helper scripts for managing ec2 instances*

install-cw-log-agent.yml This script installs AWS Cloudwatch agents on an Ubuntu 

How to run this script on a single host, you can use the following example command   **ansible-playbook -i x.x.x.x, --user ubuntu --key-file ~/key-location/my-instance-keypair.pem install-cw-log-agent.yml** 
replace x.x.x.x with the IP or DNS name of the ec2-instance
