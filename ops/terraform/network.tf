#--------------------------------------------------------------
# VPC Networking
#--------------------------------------------------------------
resource "aws_vpc" "culturely_vpc" {
	cidr_block = "10.0.0.0/16"
	enable_dns_support = true
	enable_dns_hostnames = true

	tags {
		Name = "culturely_vpc"
	}

	lifecycle {
		create_before_destroy = true
	}
}

resource "aws_subnet" "public" {
	vpc_id = "${aws_vpc.culturely_vpc.id}"
	cidr_block = "10.0.23.0/24"
	availability_zone = "us-east-1a"
	map_public_ip_on_launch = true

	tags {
		Name = "culturely_public_subnet"
	}

	lifecycle {
		create_before_destroy = true
	}
}

resource "aws_subnet" "private" {
	vpc_id = "${aws_vpc.culturely_vpc.id}"
	cidr_block = "10.0.24.0/24"
	availability_zone = "us-east-1a"

	tags {
		Name = "culturely_private_subnet"
	} 

	lifecycle {
		create_before_destroy = true
	}
}

resource "aws_internet_gateway" "culturely_gate" {
	vpc_id = "${aws_vpc.culturely_vpc.id}"

	lifecycle {
		create_before_destroy = true
	}
}

resource "aws_route_table" "public" {
	vpc_id = "${aws_vpc.culturely_vpc.id}"

	lifecycle {
		create_before_destroy = true
	}
}

resource "aws_route" "public_internet_gateway" {
	route_table_id = "${aws_route_table.public.id}"
	destination_cidr_block = "0.0.0.0/0"
	gateway_id = "${aws_internet_gateway.culturely_gate.id}"

	lifecycle {
		create_before_destroy = true
	}
}

resource "aws_route_table" "private" {
	vpc_id = "${aws_vpc.culturely_vpc.id}"

	route {
		cidr_block = "0.0.0.0/0"
		gateway_id = "${aws_internet_gateway.culturely_gate.id}"
	}

	lifecycle{
		create_before_destroy = true
	}
}

resource "aws_route_table_association" "private" {
	subnet_id = "${aws_subnet.private.id}"
	route_table_id = "${aws_route_table.private.id}"

	lifecycle {
		create_before_destroy = true
	}
}

resource "aws_route_table_association" "public" {
	subnet_id = "${aws_subnet.public.id}"
	route_table_id = "${aws_route_table.public.id}"

	lifecycle {
		create_before_destroy =true
	}
}
#--------------------------------------------------------------
# elb
#--------------------------------------------------------------
resource "aws_elb" "elb" {
	subnets = ["${aws_subnet.public.id}"]
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
# DNS(Route53)
#--------------------------------------------------------------
# resource "aws_route53_record" "dns" {
# 	zone_id = "{aws_route53_zone.primary.zone_id}"
# 	name    = "23.com"
# 	type = "CNAME"
# 	ttl = "300"
# 	records = ["${aws_elb.elb.dns_name}"]

# 	lifecycle {
# 		create_before_destroy = true
# 	}
# }






