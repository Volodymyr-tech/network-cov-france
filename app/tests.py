from rest_framework import status
from rest_framework.test import APITestCase
from app.models import MobileSite, Operator


class MobileSiteByCityViewTestCase(APITestCase):
    def setUp(self):
        self.operator = Operator.objects.create(code="20801", name="Orange")

        self.site = MobileSite.objects.create(
            city="Paris",
            has_2g=True,
            has_3g=True,
            has_4g=True,
            operator=self.operator,
        )

        self.other_site = MobileSite.objects.create(
            city="Lyon",
            has_2g=False,
            has_3g=True,
            has_4g=True,
            operator=self.operator,
        )

    def test_get_sites_by_city_success(self):
        url = "/api/coverage/?q=Paris"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["city"], "Paris")


    def test_get_sites_by_city_case_insensitive(self):
        url = "/api/coverage/?q=paris"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_sites_by_city_not_found(self):
        url = "/api/coverage/?q=Nice"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_sites_by_city_missing_param(self):
        url = "/api/coverage/"  # no ?q= param
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Missing ?q=city parameter")
