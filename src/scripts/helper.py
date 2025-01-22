import geopandas as gpd
import pandas as pd


def points_in_boundaries(
    df: pd.DataFrame, city_boundaries: gpd.GeoDataFrame, ts_col: str = "ts"
) -> pd.DataFrame:

    df = df.drop_duplicates().reset_index(drop=True)
    df = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["longitude"], df["latitude"], crs=4326),
        crs=4326,
    )  # type: ignore

    df_left = (
        pd.DataFrame(
            data=df.sindex.query(city_boundaries.geometry, predicate="intersects").T,
            columns=["district_id", "point_id"],
        )
        .reset_index(drop=True)
        .set_index("district_id")
        .join(city_boundaries)
    )

    df_right = (
        df.iloc[df_left["point_id"]][ts_col]
        .reset_index()
        .rename(
            columns={
                "index": "point_id",
                ts_col: "timestamp",
            }
        )
    )

    return pd.merge(df_left, df_right, on="point_id").rename(
        columns={
            "City": "city",
            "name": "district_id",
        }
    )


def build_timeseries(data):
    ts = (
        data.groupby(by=["district_id", "city", "timestamp"])
        .agg({"point_id": "count"})
        .rename({"point_id": "crowd"}, axis=1)
        .sort_values(by="timestamp")
        .reset_index()
    )

    return ts[["district_id", "timestamp", "crowd", "city"]]
