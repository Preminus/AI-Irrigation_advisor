## imports 

"""
dataset.py

Creates a machine learning dataset
for the AI Irrigation Advisor.

Author: Preminus Karani
"""

import pandas as pd

from datetime import datetime
# from soil.soils import SoilDownloader

import fao56 as fao
import crop_calendar as calendar


## constants

latitude_deg = -1.246
longitude_deg = 36.662
elevation = 1800

IRRIGATION_EFFICIENCY = 0.85

## Load weather data

def load_weather_dataset(path):
    """
    Load historical weather data.
    """

    df = pd.read_csv(path)

    df["Date"] = pd.to_datetime(df["Date"])

    return df

## Calendar features

def add_calendar_features(df):
    """
    Add date-related features.
    """

    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df["DayOfYear"] = df["Date"].dt.dayofyear

    return df


## weather features

def add_weather_features(df):

    df["Temp_Range"] = (
        df["Max_Temperature"]
        - df["Min_Temperature"]
    )

    df["Rain_3Day"] = (
        df["Rainfall"]
        .rolling(3)
        .sum()
    )

    df["Rain_7Day"] = (
        df["Rainfall"]
        .rolling(7)
        .sum()
    )

    return df

## crop calendar features

def add_crop_features(df, planting_date):

    df["GrowthStage"] = df["Date"].apply(
        lambda d: calendar.get_growth_stage(
            d,
            planting_date
        )
    )

    df["Kc"] = df["Date"].apply(
        lambda d: calendar.get_kc(
            d,
            planting_date
        )
    )

    return df

## ETo calculate reference evapotranspiration (ETo) using the FAO-56 Penman-Monteith method

def calculate_et0(row):

    return fao.calculate_daily_et0_from_radiation(

        Tmax=row["Max_Temperature"],
        Tmin=row["Min_Temperature"],
        RH=row["Relative_Humidity"],
        wind_speed=row["Wind_Speed"],
        wind_height=WIND_HEIGHT,
        elevation=elevation,
        latitude_deg=latitude_deg,
        day_of_year=row["DayOfYear"],
        solar_radiation=row["Solar_Radiation"],
    )

def add_et0(df):

    df["ET0"] = df.apply(
        calculate_et0,
        axis=1
    )

    return df

## ETc calculation of crop evapotranspiration (ETc) using the FAO-56 method

def add_etc(df):

    df["ETc"] = (
        df["ET0"]
        * df["Kc"]
    )

    return df

## Irrigation requirement calculation
def add_irrigation(df):

    df["NIR"] = (
        df["ETc"]
        - df["Rainfall"]
    ).clip(lower=0)

    df["GIR"] = (
        df["NIR"]
        / IRRIGATION_EFFICIENCY
    )

    return df

## pipeline to create the dataset

def build_dataset(path, planting_date):

    df = load_weather_dataset(path)

    df = add_calendar_features(df)

    df = add_weather_features(df)

    df = add_crop_features(
        df,
        planting_date
    )

    df = add_et0(df)

    df = add_etc(df)

    df = add_irrigation(df)

    return df

