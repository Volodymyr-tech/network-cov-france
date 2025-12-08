from django.db.models import Avg, IntegerField
from django.db.models.functions import Cast
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.models import MobileSite


class MobileSiteByCityView(APIView):
    """Returns an average coverage by city"""

    def get(self, request):
        city = request.query_params.get("q")
        if not city:
            return Response(
                {"error": "Missing ?q=city parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sites_by_operator = (
            MobileSite.objects.filter(location__city__exact=city)
            .values("operator__code", "operator__name")
            .annotate(
                avg_2g=Avg(Cast("has_2g", output_field=IntegerField())),
                avg_3g=Avg(Cast("has_3g", output_field=IntegerField())),
                avg_4g=Avg(Cast("has_4g", output_field=IntegerField())),
            )
            .order_by("operator__name")
        )

        COVERAGE_THRESHOLD = 0.5
        result_data = []

        for item in sites_by_operator:
            result_data.append(
                {
                    "operator": {
                        "code": item["operator__code"],
                        "name": item["operator__name"],
                    },
                    "coverage": {
                        "2g": item["avg_2g"] is not None and item["avg_2g"] >= COVERAGE_THRESHOLD,
                        "3g": item["avg_3g"] is not None and item["avg_3g"] >= COVERAGE_THRESHOLD,
                        "4g": item["avg_4g"] is not None and item["avg_4g"] >= COVERAGE_THRESHOLD,
                    },
                }
            )

        return Response(result_data, status=status.HTTP_200_OK)
