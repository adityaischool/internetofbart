import math

def distance_on_unit_sphere(lat1, long1, lat2, long2):

	# Convert latitude and longitude to
	# spherical coordinates in radians.
	degrees_to_radians = math.pi/180.0
		 
	# phi = 90 - latitude
	phi1 = (90.0 - float(lat1))*degrees_to_radians
	phi2 = (90.0 - float(lat2))*degrees_to_radians
		 
	# theta = longitude
	theta1 = float(long1)*degrees_to_radians
	theta2 = float(long2)*degrees_to_radians
	cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
	arc = math.acos( cos )
	return arc