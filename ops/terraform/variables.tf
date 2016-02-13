variable "key_name" {
	default = "culturely"
}

variable "aws_access_key" {
	default = "{{{env `aws_access_key_id`}}"
}

variable "aws_secret_key" {
	default = "{{env `aws_secret_access_key`}}"
}

variable "atlas_token" {
	default = "{{env `ATLAS_TOKEN`}}"
}

variable "atlas_username" {
	default = "{{env `ATLAS_USERNAME`}}"
}

variable "consul_server_count" {
	default = 3
}