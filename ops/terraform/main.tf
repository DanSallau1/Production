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
    vpc_security_group_ids = ["${aws_security_group.web.id}", "${aws_security_group.consul-security.id}"]

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
    vpc_security_group_ids = ["${aws_security_group.web.id}", "${aws_security_group.consul-security.id}"]

    count = 2
	tags {
		Name = "consul_culturely"
	}

    lifecycle {
        create_before_destroy = true
    }
}
