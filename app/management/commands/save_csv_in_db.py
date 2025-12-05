import csv
import os
from django.core.management.base import BaseCommand
from app.utils.lambert_to_gps import lamber93_to_gps
from app.utils.reverse_geographic_search import GeographicSearch
from app.models import MobileSite, Operator
from logger_settings.logger import get_logger

log = get_logger("save_csv_in_db")

MNC_TO_NAME = {"20801": "Orange", "20810": "SFR", "20815": "Free", "20820": "Bouygue"}


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = os.path.join(
            "data", "2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv"
        )

        with open(path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            count = 0
            skipped = 0

            for row in reader:
                try:
                    x = float(row["x"])
                    y = float(row["y"])

                    coords = lamber93_to_gps(x, y)

                    if not coords:
                        skipped += 1
                        continue

                    lon, lat = coords
                    var = GeographicSearch(lon, lat)
                    city = GeographicSearch.geographic_search(
                        var.longitude, var.latitude
                    )

                    if not city:
                        skipped += 1
                        log.info(f"[SKIPPED] City not found lon={lon}, lat={lat}")
                        continue

                    operator_code = row["Operateur"]
                    operator_name = MNC_TO_NAME.get(
                        operator_code, f"Unknown {operator_code}"
                    )
                    operator, _ = Operator.objects.get_or_create(
                        code=operator_code, defaults={"name": operator_name}
                    )

                    MobileSite.objects.create(
                        operator=operator,
                        x=row["x"],
                        y=row["y"],
                        has_2g=row["2G"],
                        has_3g=row["3G"],
                        has_4g=row["4G"],
                    )

                    count += 1
                    if count % 100 == 0:
                        log.info(f"{count} rows imported...")

                except Exception as e:
                    log.info(f"Error in row: {row}\n→ {str(e)}")

        log.info(f"Import. Success: {count}, skipped: {skipped}")
