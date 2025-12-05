from pyproj import Transformer

def gps_to_lambert93(lon, lat):
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2154", always_xy=True)  # WGS84 -> Lambert-93
    x, y = transformer.transform(lon, lat)
    return round(x), round(y)
