from math import pi, sin, cos, atan2, sqrt

def calculate_distance(point1, point2):
    """Utility function to calculate the Haversine distance between two points."""
    earth_radius_km = 6371
    to_radian = lambda x: x * (pi / 180)

    delta_lat = to_radian(point2['latitude'] - point1['latitude'])
    delta_lng = to_radian(point2['longitude'] - point1['longitude'])

    lat1 = to_radian(point1['latitude'])
    lat2 = to_radian(point2['latitude'])

    a = (
        sin(delta_lat / 2) * sin(delta_lat / 2) +
        sin(delta_lng / 2) * sin(delta_lng / 2) * cos(lat1) * cos(lat2)
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return earth_radius_km * c