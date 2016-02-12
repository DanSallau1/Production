# Class: ntp::ntpfile
#
#
class ntp::ntpfile {
	# resources
	file { '/etc/ntp.conf':
		ensure  => file,
		source  => 'puppet:///modules/ntp/ntp.conf',
		require => Package['ntp'],
		
	}

}