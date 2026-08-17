"""
crop_calendar.py

Tomato crop calendar and growth stage functions.

Author: Preminus Karani
Project: AI Irrigation Advisor
"""

from datetime import datetime

# Tomato growth stages (days after planting)
TOMATO_INITIAL_KC = 0.60
TOMATO_DEVELOPMENT_KC = 0.90
TOMATO_MID_KC = 1.15
TOMATO_LATE_KC = 0.80

"""
Tomato growth stages based on FAO-56.
Duration is in days after planting (DAP).
"""

TOMATO_STAGES = [

    {
        "stage": "Initial",
        "start": 0,
        "end": 30,
        "kc": 0.60
    },

    {
        "stage": "Development",
        "start": 31,
        "end": 60,
        "kc": 0.90
    },

    {
        "stage": "Mid",
        "start": 61,
        "end": 90,
        "kc": 1.15
    },

    {
        "stage": "Late",
        "start": 91,
        "end": 120,
        "kc": 0.80
    }

]

TOMATO_GROWTH_DURATION = 120

## Step 2: Determine crop age
from datetime import datetime


def crop_age(current_date, planting_date):
    """
    Returns crop age in days.

    Parameters
    ----------
    current_date : datetime

    planting_date : datetime

    Returns
    -------
    int
    """

    return (current_date - planting_date).days

## Step 3: Determine growth stage

def get_growth_stage(current_date, planting_date):
    """
    Returns the current tomato growth stage.
    """

    age = crop_age(current_date, planting_date)

    if age < 0:
        return None

    for stage in TOMATO_STAGES:

        if stage["start"] <= age <= stage["end"]:

            return stage["stage"]

    return "Harvested"

## Step 4: Determine crop coefficient (Kc)

def get_kc(current_date, planting_date):
    """
    Returns crop coefficient (Kc).
    """

    age = crop_age(current_date, planting_date)

    if age < 0:
        return None

    for stage in TOMATO_STAGES:

        if stage["start"] <= age <= stage["end"]:

            return stage["kc"]

    return 0.0

# step 5: check if the crop is active
def is_crop_active(current_date, planting_date):
    """
    Returns True if the crop is active, False otherwise.
    """
    age = crop_age(current_date, planting_date)
    return 0 <= age <= TOMATO_GROWTH_DURATION
    return age > TOMATO_GROWTH_DURATION


## Step 6: Check if the crop is in which stage
def is_stage(current_date, planting_date, stage_name):
    """
    Returns True if crop is in the specified stage.
    """

    return (
        get_growth_stage(
            current_date,
            planting_date
        ) == stage_name
    )
# Update is_crop_active()

def is_crop_active(current_date, planting_date):
    """
    Returns True while tomatoes are still growing.
    """

    age = crop_age(current_date, planting_date)

    return 0 <= age <= 120