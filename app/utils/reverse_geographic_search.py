import requests


class GeographicSearch:
    url = "https://api-adresse.data.gouv.fr/reverse/"

    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

    @staticmethod
    def geographic_search(longitude, latitude):
        try:
            result = requests.get(
                url=GeographicSearch.url,
                params={'lon': longitude, 'lat': latitude}
            )

            result.raise_for_status()

            data = result.json()

            return data["features"][0]["properties"]["city"]

        except requests.exceptions.HTTPError as e:
            print(f"Error HTTP: {e}")
            return None

        except requests.exceptions.JSONDecodeError:
            print("Error: Not valid JSON.")
            return result.text

        except Exception as e:
            print(f"Error: {e}")
            return None