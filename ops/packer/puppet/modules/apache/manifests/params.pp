# Class: apache::params
#
#
class apache::params {
	# specify server name for vhost config files
	
	# enter puppet code
	if ($::fqdn) {
		$servername = $::fqdn
	} else {
		$servername = $::hostname
	}


	$document_root = "/var/www/html"
	$log_dir = "/var/log/apache"

	$package_name = "apache2"
	$service_name = "apache2"
	$conf_dir     = "/etc/apache2"
	$vhost_dir    = "/etc/apache2/sites-available/"
	$webapp_dir   = "/var/www/html"
	$managerepo   = true

}