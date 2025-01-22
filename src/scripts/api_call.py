import time
from typing import Dict, List

import pandas as pd
import requests
from config import API_URL
from loguru import logger


def _parse_json_data(
    json_data: List[Dict[str, str | float]],
    timestamp: float,
) -> pd.DataFrame:
    try:
        logger.info("Parsing JSON data")
        df = pd.DataFrame(json_data)

        # Add timestamp column
        df["ts"] = timestamp

        location_df = pd.json_normalize(df.pop("location"))
        df = pd.concat([df, location_df], axis=1)

        logger.info("Added lat/lon columns and dropped location column")
        return df
    except KeyError as e:
        logger.error(f"Missing expected keys in JSON data: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during JSON parsing: {e}")
        raise


def fetch_data() -> pd.DataFrame | None:
    """
    Fetch data from the API and process it into a DataFrame.

    Returns:
        pd.DataFrame | None: DataFrame containing processed data or None if the request fails.
    """
    try:
        logger.info("Fetching data from API")
        response = requests.get(API_URL, timeout=10)

        # Check HTTP status code
        if response.status_code == 200:
            ts = time.time()
            logger.success(f"Request successful | Status Code: {response.status_code}")

            # Parse JSON once
            try:
                if data := response.json().get("vehicles_in_public_space", []):
                    df = _parse_json_data(data, ts)
                    logger.info(f"{len(df)} rows processed")
                    return df
                else:
                    logger.warning("No data available in the API response")
                    return None
            except ValueError as e:
                logger.error(f"Error decoding JSON response: {e}")
                raise
        else:
            logger.error(f"Request failed | Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        logger.error(f"Request exception occurred: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error while fetching data: {e}")
        return None


if __name__ == "__main__":
    if (df := fetch_data()) is not None:
        print(df.head())
