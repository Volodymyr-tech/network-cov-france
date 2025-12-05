import requests
from rest_framework.response import Response
from rest_framework import status



def get_gps_by_city_name(query):
    # 1. Получаем координаты GPS через API
    geo_resp = requests.get(f"https://api-adresse.data.gouv.fr/search/?q={query}")

    if geo_resp.status_code != 200:
        return Response({"error": "Failed to get geolocation"}, status=status.HTTP_502_BAD_GATEWAY)

    features = geo_resp.json().get("features")
    if not features:
        return Response({"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND)

    lon, lat = features[0]["geometry"]["coordinates"]

    return round(lon), round(lat)