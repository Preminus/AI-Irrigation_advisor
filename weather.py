"""
weather.py

Provides weather data for the irrigation advisor.

Author: Preminus Karani
"""

from datetime import datetime


def sample_weather():
    """
    Returns a sample weather observation for
    Muguga, Kikuyu, Kiambu County.
    """

    return {

        # Temperature (°C)
        "Tmax": 28.0,
        "Tmin": 18.0,

        # Relative humidity (%)
        "RH": 70,

        # Wind
        "wind_speed": 2.0,
        "wind_height": 2.0,

        # Rainfall (mm/day)
        "rainfall": 2.4,

        # Sunshine duration (hours/day)
        "sunshine_hours": 8.5,

        # Site information
        "latitude_deg": -1.246,
        "longitude_deg": 36.662,
        "elevation": 1800,

        # Julian day
        "day_of_year": 100

    }
from datetime import datetime


def weather_today():
    """
    Returns today's weather.
    Updates only the day of year.
    """

    weather = sample_weather()

    weather["day_of_year"] = (
        datetime.now().timetuple().tm_yday
    )

    return weather