from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import MobileSite
from app.serializers import MobileSiteSerializer


class MobileSiteByCityView(APIView):
    def get(self, request):
        city = request.query_params.get('q')
        if not city:
            return Response({'error': 'Missing ?q=city parameter'}, status=status.HTTP_400_BAD_REQUEST)

        sites = MobileSite.objects.filter(city__iexact=city)
        serializer = MobileSiteSerializer(sites, many=True)
        return Response(serializer.data)
