;
;
; MANAGED BY TERRAFORM, DO NOT EDIT THIS FILE DIRECTLY.
; TO UPDATE, ADD YOUR CHANGES TO deployment/terraform/templates/ansible_inventory.tpl
;

app-server=app-server.${internal_zone_name}

[app-server]
app-server.${internal_zone_name}

[app-server:vars]
ansible_ssh_common_args="-o ProxyCommand='ssh ubuntu@bastion.${external_zone_name} -W %h:%p'"
ansible_user="ec2-user"