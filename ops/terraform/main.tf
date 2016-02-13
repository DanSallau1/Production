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
# Security groups
#--------------------------------------------------------------
resource "aws_security_group" "web" {
	name = "web"
	description "access to the web"
	vpc_id = "${aws_vpc.culturely_vpc.id}"

	ingress {
		from_port = 0
		to_port   = 65535
		protocol  = "tcp"
		self      = true
	}

	ingress {
		from_port = 0
		to_port   = 65535
		protocol  = "udp"
		self      = true
	}

	ingress {
		from_port = 22
		to_port   = 22
		protocol  = "tcp"
		cidr_blocks = ["0.0.0.0/0"]
	}

	ingress {
		from_port = 80
		to_port   = 80
		protocol  = "tcp"
		cidr_blocks = ["0.0.0.0/0"]
	}

	ingress {
		from_port = 443
		to_port   = 443
		protocol  = "tcp"
		cidr_blocks = ["0.0.0.0/0"]
	}

	ingress {
		from_port = 1099
		to_port   = 1099
		protocol  = "tcp"
		cidr_blocks = ["0.0.0.0/0"]
	}

	ingress {
		from_port = 8080
		to_port   = 8080
		protocol  = "tcp"
		cidr_blocks = ["0.0.0.0/0"]
	}

	egress {
		from_port = 0
		to_port   = 0
		protocol  = "-1"
		cidr_blocks = ["0.0.0.0/0"]
	}
}

resource "aws_security_group" "consul-security" {
    name = "${var.security_group_name}"
    description = "Security Group ${var.security_group_name}"
    vpc_id = "${var.vpc_id}"

    // allows traffic from the SG itself for tcp
    ingress {
        from_port = 0
        to_port = 65535
        protocol = "tcp"
        self = true
    }

    // allows traffic from the SG itself for udp
    ingress {
        from_port = 0
        to_port = 65535
        protocol = "udp"
        self = true
    }

    // allow traffic for TCP 22 (SSH)
    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    // allow traffic for TCP 8300 (Server RPC)
    ingress {
        from_port = 8300
        to_port = 8300
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    // allow traffic for TCP 8301 (Serf LAN)
    ingress {
        from_port = 8301
        to_port = 8301
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    // allow traffic for UDP 8301 (Serf LAN)
    ingress {
        from_port = 8301
        to_port = 8301
        protocol = "udp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    // allow traffic for TCP 8400 (Consul RPC)
    ingress {
        from_port = 8400
        to_port = 8400
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    // allow traffic for TCP 8500 (Consul Web UI)
    ingress {
        from_port = 8500
        to_port = 8500
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    // allow traffic for TCP 8600 (Consul DNS Interface)
    ingress {
        from_port = 8600
        to_port = 8600
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    // allow traffic for UDP 8600 (Consul DNS Interface)
    ingress {
        from_port = 8600
        to_port = 8600
        protocol = "udp"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

#--------------------------------------------------------------
# elb
#--------------------------------------------------------------
resource "aws_elb" "elb" {
	name = "elb"
	subnets = ["${aws_subnet.public.id}", "${aws_subnet.private.id}"]
	security_groups = ["${aws_security_group.web.id}", "${aws_security_group.consul-security.id}"]

	listener {
		instance_port = 80
        instance_protocol = "http"
        lb_port = 80
        lb_protocol = "http"
	}
	health_check {
		healthy_threshold = 2
		unhealthy_threshold = 2
		timeout = 3
		target = "HTTP:80/"
		interval = 30
	}

	instances = ["${aws_instance.culturely-web.*.id}","${aws_instance.consul-web.*.id}"]

	lifecycle {
		create_before_destroy = true
	}
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


