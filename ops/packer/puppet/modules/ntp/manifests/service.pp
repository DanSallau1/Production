# Class: ntp::service
#
#
class ntp::service {
	# resources
	service { 'ntp':
		enable      => true,
		ensure      => running,
		subscribe   => File['/etc/ntp.conf'],
		#hasrestart => true,
		#hasstatus  => true,
		#require    => Class["config"],
	}
}