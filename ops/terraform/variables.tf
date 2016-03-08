variable "key_name" {
	default = "Panda-key"
}

variable "region" {
	default = "us-east-1"
}

variable "aws_access_key" {
	default = "{{env `AWS_ACCESS_KEY_ID`}}"
}

variable "aws_secret_key" {
	default = "{{env `AWS_SECRET_ACCESS_KEY`}}"
}

variable "atlas_token" {
	default = "{{env `ATLAS_TOKEN`}}"
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