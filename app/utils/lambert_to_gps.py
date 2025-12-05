from pyproj import Transformer

transformer = Transformer.from_crs("EPSG:2154", "EPSG:4326", always_xy=True)


def lamber93_to_gps(x, y):
    try:
        lon, lat = transformer.transform(x, y)
        return lon, lat
    except Exception as e:
        print(f"[lamber93_to_gps ERROR] x={x}, y={y} | {e}")
        return None
