import time
import requests
import json
import pandas as pd
from pathlib import Path

from .config import (
    SOILGRIDS_URL,
    SOIL_PROPERTIES,
    CACHE
)

class SoilDownloader:

    def __init__(
        self,
        retries=5,
        sleep=0.5,
        timeout=30
    ):

        self.session = requests.Session()

        self.retries = retries
        self.sleep = sleep
        self.timeout = timeout

    def query(
        self,
        latitude,
        longitude
    ):

        cache_file = CACHE / f"{latitude}_{longitude}.json"

        if cache_file.exists():
         with open(cache_file, "r") as f:
          return json.load(f)

        params = {

            "lon": longitude,
            "lat": latitude,
            "property": SOIL_PROPERTIES,
            "depth": "0-5cm",
            "value": "mean"
        }

        for _ in range(self.retries):

            try:

                r = self.session.get(
                    SOILGRIDS_URL,
                    params=params,
                    timeout=self.timeout
                )

                r.raise_for_status()

                data = r.json()

                values = {}

                for layer in data["properties"]["layers"]:

                    values[layer["name"]] = \
                        layer["depths"][0]["values"]["mean"]

                values["location"] = "Muguga"

                with open(cache_file, "w") as f:
                  json.dump(values, f, indent=4)

                return values

            except Exception:

                time.sleep(self.sleep)

        return None

    def add_soil_features(self, df):
        """
        Compute derived soil properties.
        """

        # Placeholder for now.
        # We will calculate these using SoilGrids variables later.

        return df

    def build_dataset(self, points):

        rows = []

        total = len(points)

        for i, point in enumerate(points.itertuples()):

            print(f"{i+1}/{total}")

            row = self.query(
                point.latitude,
                point.longitude
            )

            if row is not None:

                rows.append(row)

        df = pd.DataFrame(rows)

        df = self.add_soil_features(df)

        return df


def load_muguga_soil():
    """
    Load the representative Muguga soil profile.

    Note:
    These are provisional/assumed values for the prototype,
    not laboratory measurements from the farm.
    """

    soil_file = (
        Path(__file__).resolve().parent
        / "dummy_muguga_soil.csv"
    )

    if not soil_file.exists():
        raise FileNotFoundError(
            f"Muguga soil file not found: {soil_file}"
        )

    soil_df = pd.read_csv(soil_file)

    return soil_df

## soil-water function
def calculate_available_water(
    field_capacity,
    wilting_point,
    root_depth
):
    """
    Calculate total available water (TAW)
    in the tomato root zone.

    TAW = 1000 × (FC - WP) × root depth

    Parameters
    ----------
    field_capacity : float
        Volumetric water content at field capacity.

    wilting_point : float
        Volumetric water content at wilting point.

    root_depth : float
        Effective tomato root depth in metres.

    Returns
    -------
    float
        Total available water in mm.
    """

    if field_capacity <= wilting_point:
        raise ValueError(
            "Field capacity must be greater than wilting point."
        )

    if root_depth <= 0:
        raise ValueError(
            "Root depth must be greater than zero."
        )

    taw = (
        1000
        * (field_capacity - wilting_point)
        * root_depth
    )

    return taw


## create a soil-water function

def get_muguga_water_parameters(root_depth=0.60):
    """
    Load Muguga soil data and calculate
    TAW and RAW for the tomato root zone.

    Parameters
    ----------
    root_depth : float
        Effective root depth in metres.

    Returns
    -------
    dict
        Soil water parameters.
    """

    soil_df = load_muguga_soil()

    field_capacity = soil_df.loc[0, "field_capacity"]
    wilting_point = soil_df.loc[0, "wilting_point"]

    taw = calculate_available_water(
        field_capacity=field_capacity,
        wilting_point=wilting_point,
        root_depth=root_depth
    )

    raw = taw * 0.40

    return {
        "field_capacity": field_capacity,
        "wilting_point": wilting_point,
        "root_depth": root_depth,
        "TAW": taw,
        "RAW": raw
    }