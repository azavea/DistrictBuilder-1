#
# EC2 resources
#
data "template_file" "user_data" {
  template = "${file("templates/cloud-config.tpl")}"

  vars {
    zip_file_uri = "${var.remote_state_bucket_prefix}-${lower(var.environment)}-config-${var.aws_region}/docker_certs/server/${lower(var.state)}.zip"
    state        = "${upper(var.state)}"
    environment  = "${var.environment}"
  }
}

resource "aws_instance" "app_server" {
  ami = "${var.ami_id}"

  ebs_optimized = true

  iam_instance_profile                 = "${data.terraform_remote_state.core.app_server_instance_profile}"
  instance_initiated_shutdown_behavior = "stop"
  instance_type                        = "${var.app_server_instance_type}"
  key_name                             = "${data.terraform_remote_state.core.app_server_key_name}"
  monitoring                           = true
  subnet_id                            = "${data.terraform_remote_state.core.public_subnet_ids[0]}"
  vpc_security_group_ids               = ["${data.terraform_remote_state.core.app_server_security_group_ids}"]
  user_data                            = "${data.template_file.user_data.rendered}"

  tags {
    Name        = "AppServer"
    Project     = "${var.project}"
    Environment = "${var.environment}"
  }
}

resource "null_resource" "provision_app_server" {
  triggers {
    uuid = "${uuid()}"
  }

  provisioner "file" {
    source      = "${path.root}/../user-data"
    destination = "/home/ec2-user/"

    connection {
      type        = "ssh"
      host        = "${aws_instance.app_server.private_ip}"
      user        = "ec2-user"
      private_key = "${file(pathexpand("${var.ssh_identity_file_path}"))}"

      bastion_host        = "${data.terraform_remote_state.core.bastion_hostname}"
      bastion_user        = "ec2-user"
      bastion_private_key = "${file(pathexpand("${var.ssh_identity_file_path}"))}"
    }
  }

  provisioner "remote-exec" {
    inline = [
      "sudo mkdir -p /opt/district-builder/user-data",
      "sudo mv /home/ec2-user/user-data/* /opt/district-builder/user-data",
      "sudo chown -R ec2-user:ec2-user /opt/district-builder/",
      "touch /opt/district-builder/user-data/config_settings.py",
    ]

    connection {
      type        = "ssh"
      host        = "${aws_instance.app_server.private_ip}"
      user        = "ec2-user"
      private_key = "${file(pathexpand("${var.ssh_identity_file_path}"))}"

      bastion_host        = "${data.terraform_remote_state.core.bastion_hostname}"
      bastion_user        = "ec2-user"
      bastion_private_key = "${file(pathexpand("${var.ssh_identity_file_path}"))}"
    }
  }

  depends_on = [
    "aws_instance.app_server",
  ]
}
