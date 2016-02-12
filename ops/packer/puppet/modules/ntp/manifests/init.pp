# Class: ntp
#
#
class ntp {
	# resources

	package { 'ntp':
		ensure => installed,
	}

	include ntp::ntpfile
	include ntp::service
	
}