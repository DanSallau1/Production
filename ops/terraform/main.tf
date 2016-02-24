#--------------------------------------------------------------
# Provider
#--------------------------------------------------------------
provider "aws" {
    access_key = "${var.aws_access_key}"
    secret_key = "${var.aws_secret_key}"
 	region = "us-east-1"
}

#--------------------------------------------------------------
# Artifact(s)
#--------------------------------------------------------------
resource "atlas_artifact" "culturely" {
	name = "Panda/culturely"
	type = "amazon.ami"
	version = "latest"
}

resource "atlas_artifact" "consul_culturely" {
	name = "Panda/consul_culturely"
	type = "amazon.ami"
	version = "latest"
}

#--------------------------------------------------------------
# Temaplates(s)
#--------------------------------------------------------------
resource "template_file" "consul_upstart" {
  template = "${file("scripts/consul_upstart.sh")}"

  vars {
    region = "${var.region}"
    atlas_token = "${var.atlas_token}"
    atlas_username = "${var.atlas_username}"
    atlas_environment = "${var.atlas_environment}"
    consul_bootstrap_expect = "${var.consul_bootstrap_expect}"
    }

    lifecycle {
        create_before_destroy = true
    }
}

#--------------------------------------------------------------
# Module(s)
#--------------------------------------------------------------
module "ssh_keys" {
	source = "./ssh_keys"
	name   = "${var.key_name}"
}

#--------------------------------------------------------------
# Instance(s)
#--------------------------------------------------------------
resource "aws_instance" "culturely-web" {
    ami = "${atlas_artifact.culturely.metadata_full.ami_id}"
    instance_type = "t1.micro"
    key_name = "${module.ssh_keys.key_name}"
    user_data = "${template_file.consul_upstart.rendered}"
    subnet_id = "${aws_subnet.public.id}"
    vpc_security_group_ids = ["${aws_security_group.web.id}", "${aws_security_group.consul-security.id}"]
    depends_on = ["aws_internet_gateway.culturely_gate"]

    count = 2
	tags {
		Name = "culturely-web"
	}

    lifecycle {
        create_before_destroy = true
    }
}

resource "aws_instance" "consul-web" {
    ami = "${atlas_artifact.consul_culturely.metadata_full.ami_id}"
    instance_type = "t1.micro"
    key_name = "${module.ssh_keys.key_name}"
    user_data = "${template_file.consul_upstart.rendered}"
    subnet_id = "${aws_subnet.public.id}"
    vpc_security_group_ids = ["${aws_security_group.web.id}","${aws_security_group.consul-security.id}"]
    depends_on = ["aws_internet_gateway.culturely_gate"]

    count = 3
	tags {
		Name = "consul_culturely"
	}

    lifecycle {
        create_before_destroy = true
    }
}