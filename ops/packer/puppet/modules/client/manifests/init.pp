# Class: client
#
#
class client {
	# resources

	include dnsmasq

	dnsmasq::dnsserver { 'forward-zone-consul':
		domain => 'consul',
		ip     => '127.0.0.1',
		port   => '8600',
	}


	class { 'consul':
		manage_service => false,
		config_hash    => {
		'data_dir'         => '/opt/consul',
		'datacenter'       => 'east-aws',
		'log_level'        => 'INFO',
		'node_name'        => 'agent',

		}
	}

	# consul::service { 'web':
	# 	tags => ['service'],
	# 	port => 80,

	# }
}
