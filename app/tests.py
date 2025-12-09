from rest_framework import status
from rest_framework.test import APITestCase
from app.models import MobileSite, Operator, Location


class MobileSiteByCityViewTestCase(APITestCase):
    def setUp(self):
        self.operator = Operator.objects.create(code="20801", name="Orange")

        self.location_paris = Location.objects.create(city="Paris", x=12345, y=67890)
        self.location_lyon = Location.objects.create(city="Lyon", x=54321, y=98765)

        MobileSite.objects.create(
            has_2g=True,
            has_3g=True,
            has_4g=True,
            operator=self.operator,
            location=self.location_paris,
        )

        MobileSite.objects.create(
            has_2g=False,
            has_3g=True,
            has_4g=True,
            operator=self.operator,
            location=self.location_lyon,
        )

    def test_get_sites_by_city_success(self):
        url = "/api/coverage/?q=Paris"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["Orange"], {"2g": True, "3g": True, "4g": True})


    def test_get_sites_by_city_case_insensitive(self):
        url = "/api/coverage/?q=paris"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_sites_by_city_not_found(self):
        url = "/api/coverage/?q=Nice"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_sites_by_city_missing_param(self):
        url = "/api/coverage/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Missing ?q=city parameter")
