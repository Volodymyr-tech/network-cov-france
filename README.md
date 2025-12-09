# 📡 Network Coverage France

A Django-based API that provides mobile network coverage data (2G, 3G, 4G) by city in France. Data is imported from a CSV file with Lambert-93 coordinates, which are converted to GPS and matched to cities via reverse geolocation.

## Features

✅ Import and save mobile site data from CSV

✅ Lambert-93 to GPS conversion

✅ Reverse geolocation lookup for city name

✅ Operator mapping based on MNC code

✅ API endpoint to get coverage by city

✅ Includes logs for skipped/invalid rows

## 📦 Installation
- git clone https://github.com/yourusername/network-cov-france.git

- cd network-cov-france

- docker-compose up --build

## ⚙️ CSV Import Command

#### Once the app is running in Docker:

- docker-compose exec web python manage.py save_csv_in_db.py


#### This command imports data from:

- data/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv


- Logs will show imported and skipped rows.

## 🔍 API Endpoint

#### Query mobile coverage by city name (case-insensitive):

- GET /api/coverage/?q=Paris

####  ✅ Example Response:
```json
{
  "orange": { "2G": true, "3G": true, "4G": false },
  "SFR": { "2G": true, "3G": true, "4G": true }
}
```

## 🧪 Running Tests
- docker-compose exec web python manage.py test


#### To measure code coverage:

- docker-compose exec web coverage run --source='.' manage.py test
- docker-compose exec web coverage report


## 🔗 Operators Mapping
#### MNC Code - Operator

20801	Orange

20810	SFR

20815	Free

20820	Bouygue

## 🧑‍💻 Maintainer

Valdemar – LinkedIn
 | GitHub