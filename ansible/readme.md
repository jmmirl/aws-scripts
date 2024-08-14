***Ansible AWS Playbooks***

*This repo has some handy AWS Helper scripts for managing ec2 instances*

**install-cw-log-agent.yml** This Ansible script installs AWS Cloudwatch agents on an Ubuntu 

How to run this script on a single host, you can use the following example command   **ansible-playbook -i x.x.x.x, --user ubuntu --key-file ~/key-location/my-instance-keypair.pem install-cw-log-agent.yml** 
replace x.x.x.x with the IP or DNS name of the ec2-instance   
  <br/><br/>

**get-system-resources.yml** This ansible script collects system information from a remote host without having to login such as disk space, memory and top 10 processes 

How to run this script on a single host, you can use the following example command   **ansible-playbook -i x.x.x.x, --user ubuntu --key-file ~/key-location/my-instance-keypair.pem get-system-resources.yml** 
replace x.x.x.x with the IP or DNS name of the ec2-instance
