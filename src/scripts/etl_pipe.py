import time

import geopandas as gpd
import pandas as pd
from api_call import fetch_data
from config import MISC_DIR, REFRESH_INTERVAL
from database import make_connection
from helper import build_timeseries, points_in_boundaries
from logger import configure_logger
from requests.exceptions import RequestException


def main():
    TABLE_NAME = "crowdedness"

    geojson_files = {
        file.name.split("_")[0].title(): gpd.read_file(file) for file in MISC_DIR.iterdir()
    }

    boundaries = gpd.GeoDataFrame(
        pd.concat(geojson_files.values(), keys=geojson_files.keys())
        .reset_index()
        .drop(columns=["level_1", "cartodb_id", "created_at", "updated_at"])
        .rename(columns={"level_0": "City"})
    )

    engine = make_connection()

    logger.info("Starting ETL Pipeline")

    with engine.connect() as conn:
        while True:
            try:
                start = time.time()
                if (data := fetch_data()) is not None:
                    data = data.pipe(points_in_boundaries, boundaries).pipe(build_timeseries)
                    data.to_sql(
                        TABLE_NAME,
                        conn,
                        if_exists="append",
                        index=False,
                        method="multi",
                    )
                    logger.info(f"Pushed {len(data)} new rows to table")
                else:
                    logger.warning("No new data has been pulled | Waiting")
                end = time.time()
                logger.info(f"Pushed in {end - start:.2f} seconds\n")
                if end - start < REFRESH_INTERVAL:
                    time.sleep(REFRESH_INTERVAL - (end - start))

            except RequestException as e:
                logger.error(f"An error occurred while handling your request. | {e}")
            except ValueError as e:
                logger.error(f"Error parsing response | {e}")
                break
            except Exception as e:
                logger.critical(f"Unexpected error | {e}")
                break


if __name__ == "__main__":
    logger = configure_logger(log_file="etl-pipeline")
    main()
