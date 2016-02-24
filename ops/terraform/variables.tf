variable "key_name" {
	default = "Panda-key"
}

variable "region" {
	default = "us-east-1"
}

variable "aws_access_key" {
	default = "{{{env `AWS_ACCESS_KEY_ID`}}"
}

variable "aws_secret_key" {
	default = "{{env `AWS_SECRET_ACCESS_KEY`}}"
}

variable "atlas_token" {
	default = "alJTHeHJmK77EQ.atlasv1.rg6W1p75CKDW1O4kLbOVkNRNcXsSrcUCTC1kQtkoWdpr9ZRCgafQlz1LM7Ab13PJ1JA"
}

variable "atlas_username" {
	default = "Panda"
}

variable "consul_bootstrap_expect" {
	default = 5
}

variable "atlas_environment" {
	default = "Panda/culturely"
}