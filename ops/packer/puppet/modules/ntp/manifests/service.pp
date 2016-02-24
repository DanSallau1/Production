# Class: ntp::service
#
#
class ntp::service (
	$service_name = $npt::params::service_name

	) {
	# resources
	service { 'ntp':
		name        => $service_name,
		enable      => true,
		ensure      => running,
		require     => Package["ntp"],
	}

}