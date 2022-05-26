import click
import geopandas as gpd
import pandas as pd
from pyrosm import OSM
import warnings

warnings.filterwarnings("ignore")


@click.command()
@click.argument("input_paths", type=click.Path(exists=True), nargs=2)
@click.argument("output_path", type=click.Path())
def get_pois(input_paths: list[str], output_path: str):
    """Function gets points of interest from the downloaded OSM maps
    :param input_paths: Paths to read filtered GeoDataFrame and OSM dump
    :param output_path: Path to save pois GeoDataFrame
    :return:
    """
    gdf = gpd.read_file(input_paths[0])

    gdf = gdf.to_crs("epsg:3395")
    gdf["poi_buffer"] = gdf.buffer(200)
    gdf = gdf.set_geometry("poi_buffer")
    gdf = gdf.to_crs("epsg:4326")

    def pyrosm_query(fp, bbox_geom, columns_filter):
        osm = OSM(fp, bounding_box=bbox_geom)
        pois = osm.get_data_by_custom_criteria(custom_filter=custom_filter)
        pois = pois.filter(items=columns_filter)
        return pois

    aero = ["terminal"]
    amenities = [
        "bar",
        "cafe",
        "fast_food",
        "pub",
        "restaurant",
        "college",
        "university",
        "bus_station",
        "parking",
        "fuel",
        "atm",
        "bank",
        "bureau_de_change",
        "clinic",
        "hospital",
        "pharmacy",
        "veterinary",
        "theatre",
        "post_office",
        "townhall",
        "marketplace",
    ]
    buildings = ["office", "train_station"]
    highways = ["bus_stop"]
    tourist = ["hotel"]
    custom_filter = {
        "aeroway": aero,
        "amenity": amenities,
        "building": buildings,
        "highway": highways,
        "shop": True,
        "tourism": tourist,
    }
    columns_filter = list(custom_filter.keys()) + ["geometry"]

    fp = input_paths[1]
    gdfs = []
    for geom in enumerate(gdf["poi_buffer"].values, start=1):
        try:
            print(f"Ищем точки интерса вокруг объекта {geom[0]} / {len(gdf['poi_buffer'].values)}")
            gdfs.append(pyrosm_query(fp, geom[1], columns_filter))
        except KeyError:
            print(f"Точка {geom[0]} не заслуживает внимания")
        except AttributeError:
            print(f"Вокруг точки {geom[0]} ничего интересного нет")
    data_poi = pd.concat(gdfs)

    data_poi.to_file(output_path, driver="GeoJSON")


if __name__ == "__main__":
    get_pois()
