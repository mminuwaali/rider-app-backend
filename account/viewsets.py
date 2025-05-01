from django.db.models import F, Q
from rideapp.models import RiderLocation
from . import models, filters, serializers
from rideapp.utils import calculate_distance
from rest_framework import viewsets, status, response, decorators

class RiderViewSet(viewsets.ReadOnlyModelViewSet):
    filterset_class = filters.RiderFilter
    
    def get_queryset(self):
        return models.Rider.objects.all()
    
    def get_serializer_class(self):
        return serializers.RiderSerializer
    
    @decorators.action(["POST"], False, "get-closest-riders")
    def get_closest_riders(self, request):
        user_location = request.data.get("location")
        destination = request.data.get("destination")
        service_type = request.data.get("service_type")

        print(user_location, destination)

        if not user_location or not destination:
            return response.Response(
                {"error": "Both 'user_location' and 'destination' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch online riders
        riders = RiderLocation.objects.filter(is_online=True).filter(Q(rider__rider__service_type=service_type)|Q(rider__rider__service_type="both")).select_related('rider')

        # Calculate distances
        results = []
        for rider_location in riders:
            rider_distance_to_user = calculate_distance(
                user_location,
                {"latitude": rider_location.latitude, "longitude": rider_location.longitude}
            )
            rider_distance_to_destination = calculate_distance(
                {"latitude": rider_location.latitude, "longitude": rider_location.longitude},
                destination
            )
            total_distance = rider_distance_to_user + rider_distance_to_destination

            print(serializers.RiderSerializer(rider_location.rider).data)

            # Build detailed rider data
            results.append({
                "total_distance": total_distance,
                "distance_to_user": rider_distance_to_user,
                "distance_to_destination": rider_distance_to_destination,
                "rider": serializers.RiderSerializer(rider_location.rider.rider).data,
                "location": {
                    "latitude": rider_location.latitude,
                    "longitude": rider_location.longitude
                },
            })

        # Sort by proximity to the user
        sorted_results = sorted(results, key=lambda x: x["distance_to_user"])
        return response.Response(sorted_results, status=status.HTTP_200_OK)
