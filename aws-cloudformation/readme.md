# Collection of Cloudformation Templates
---
## CG-Net-add-to-vpc.yml  
This template adds some of the CGNat IP Ranges to an existing VPC and creates two subnets with 32k IPs per AZ, 
allowing for large deployments of Kubernetes worker nodes. This also deploys HA NATGWs into the public routable address space, allowing instances 
in the CG Network Range to access the internet or routable address space for updates and monitoring.

## AWS-BillingAlerts.yml 
This script creates multiple billing alerts and sends emails with these alerts to two different email addresses.
