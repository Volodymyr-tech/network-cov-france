from pyproj import Transformer
from django.db.models import Max
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.models import MobileSite
from app.serializers import MobileSiteSerializer
from app.utils.gps_by_city_name import get_gps_by_city_name
from app.utils.gps_to_lambert import gps_to_lambert93


class MobileSiteByCityView(APIView):
    def get(self, request):
        query = request.query_params.get("q")
        if not query:
            return Response({"error": "Missing ?q=city parameter"}, status=status.HTTP_400_BAD_REQUEST)

        lon, lat = get_gps_by_city_name(query)


        x_lambert, y_lambert = gps_to_lambert93(lon, lat)


        delta = 20

        sites  = MobileSite.objects.filter(
            x__gte=x_lambert - delta, x__lte=x_lambert + delta,
            y__gte=y_lambert - delta, y__lte=y_lambert + delta
        ).distinct("operator")

        serializer = MobileSiteSerializer(sites, many=True)

        return Response(serializer.data)
