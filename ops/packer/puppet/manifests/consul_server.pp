Exec { path => "/usr/bin:/usr/sbin:/bin:/sbin" }

node default {
	class { 'consul':
	  #join_cluster => '172.20.20.10',
	  manage_service => false,
	  config_hash    => {
	    'bootstrap_expect' => 3,
	    'client_addr'      => '0.0.0.0',
	    'data_dir'         => '/opt/consul',
	    'datacenter'       => 'east-aws',
	    'log_level'        => 'INFO',
	    'node_name'        => 'server',
	    'server'           => true,
	    'ui_dir'           => '/opt/consul/ui',
	  }
	}
}