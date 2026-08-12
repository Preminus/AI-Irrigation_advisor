"""
irrigation.py

Irrigation requirement calculations.

Author: Preminus Karani
Project: AI Irrigation Advisor
"""


"""
Irrigation calculations for the tomato irrigation advisor.

The module combines:
    - Reference evapotranspiration (ET0)
    - Tomato crop coefficient (Kc)
    - Crop evapotranspiration (ETc)
"""
from .crop_calendar import get_growth_stage, get_kc

from .soil.soils import get_muguga_water_parameters

def calculate_etc(et0, kc):
    """
    Calculate crop evapotranspiration (ETc).

    Parameters
    ----------
    et0 : float
        Reference evapotranspiration (mm/day).

    kc : float
        Crop coefficient.

    Returns
    -------
    float
        Crop evapotranspiration (mm/day).
    """

    if et0 < 0:
        raise ValueError("ET0 cannot be negative.")

    if kc < 0:
        raise ValueError("Kc cannot be negative.")

    etc = et0 * kc

    return etc

# calculate root zone available water.
def calculate_available_water(
    field_capacity,
    wilting_point,
    root_depth
):
    """
    Calculate total available water in the crop root zone.

    Parameters
    ----------
    field_capacity : float
        Soil water content at field capacity (cm3/cm3).

    wilting_point : float
        Soil water content at permanent wilting point (cm3/cm3).

    root_depth : float
        Effective crop root depth (m).

    Returns
    -------
    float
        Available water in the root zone (mm).
    """

    if field_capacity < 0 or wilting_point < 0:
        raise ValueError(
            "Soil water contents cannot be negative."
        )

    if field_capacity <= wilting_point:
        raise ValueError(
            "Field capacity must be greater than "
            "wilting point."
        )

    if root_depth <= 0:
        raise ValueError(
            "Root depth must be greater than zero."
        )

    available_water_fraction = (
        field_capacity - wilting_point
    )

    available_water_mm = (
        available_water_fraction
        * root_depth
        * 1000
    )

    return available_water_mm

# step 3, Daily soil water balance.

def update_soil_water(
    previous_soil_water,
    rainfall,
    irrigation,
    etc,
    available_water
):
    """
    Update the amount of water stored in the crop root zone.

    Parameters
    ----------
    previous_soil_water : float
        Soil water stored at the beginning of the day (mm).

    rainfall : float
        Effective rainfall entering the root zone (mm/day).

    irrigation : float
        Irrigation water applied (mm/day).

    etc : float
        Crop evapotranspiration (mm/day).

    available_water : float
        Maximum available water that can be stored in
        the root zone (mm).

    Returns
    -------
    float
        Updated soil water storage (mm).
    """

    if available_water <= 0:
        raise ValueError(
            "Available water must be greater than zero."
        )

    if rainfall < 0 or irrigation < 0:
        raise ValueError(
            "Rainfall and irrigation cannot be negative."
        )

    if etc < 0:
        raise ValueError(
            "ETc cannot be negative."
        )

    # Water balance
    soil_water = (
        previous_soil_water
        + rainfall
        + irrigation
        - etc
    )

    # Soil cannot store more than its available capacity
    soil_water = min(
        soil_water,
        available_water
    )

    # Soil water cannot fall below zero
    soil_water = max(
        soil_water,
        0
    )

    return soil_water



#  step 4, irrigation decision.


def should_irrigate(
    soil_water,
    available_water,
    refill_fraction=0.50
):
    """
    Determine whether irrigation is required.

    Parameters
    ----------
    soil_water : float
        Current available soil water in the root zone (mm).

    available_water : float
        Total available water in the root zone (mm).

    refill_fraction : float
        Fraction of available water at which irrigation
        should be triggered.

    Returns
    -------
    bool
        True if irrigation is required, otherwise False.
    """

    if available_water <= 0:
        raise ValueError(
            "Available water must be greater than zero."
        )

    if soil_water < 0:
        raise ValueError(
            "Soil water cannot be negative."
        )

    if not 0 < refill_fraction < 1:
        raise ValueError(
            "Refill fraction must be between 0 and 1."
        )

    irrigation_threshold = (
        available_water * refill_fraction
    )

    return soil_water <= irrigation_threshold

# step 5, Calculate irrigation amount.


def calculate_irrigation_amount(
    soil_water,
    available_water,
    target_fraction=0.90
):
    """
    Calculate the amount of irrigation water required
    to refill the root zone to a target level.

    Parameters
    ----------
    soil_water : float
        Current available soil water in the root zone (mm).

    available_water : float
        Total available water in the root zone (mm).

    target_fraction : float
        Desired fraction of available water after irrigation.

    Returns
    -------
    float
        Required irrigation amount (mm).
    """

    if available_water <= 0:
        raise ValueError(
            "Available water must be greater than zero."
        )

    if soil_water < 0:
        raise ValueError(
            "Soil water cannot be negative."
        )

    if soil_water > available_water:
        raise ValueError(
            "Soil water cannot exceed available water."
        )

    if not 0 < target_fraction <= 1:
        raise ValueError(
            "Target fraction must be between 0 and 1."
        )

    target_soil_water = (
        available_water * target_fraction
    )

    irrigation_amount = (
        target_soil_water - soil_water
    )

    # If enough water is already present,
    # no irrigation is required.
    irrigation_amount = max(
        irrigation_amount,
        0
    )

    return irrigation_amount


# step 6,

def calculate_taw(
    field_capacity,
    wilting_point,
    root_depth
):
    """
    Calculate Total Available Water (TAW)
    in the crop root zone.

    FAO-56:
        TAW = 1000 * (FC - WP) * Zr

    Parameters
    ----------
    field_capacity : float
        Volumetric water content at field capacity
        (cm3/cm3).

    wilting_point : float
        Volumetric water content at wilting point
        (cm3/cm3).

    root_depth : float
        Effective root depth (m).

    Returns
    -------
    float
        Total available water (mm).
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

# step 7, calculate readily available water (RAW).
def calculate_raw(taw, depletion_fraction):
    """
    Calculate Readily Available Water (RAW).

    FAO-56:
        RAW = p × TAW

    Parameters
    ----------
    taw : float
        Total available water (mm).

    depletion_fraction : float
        Fraction of TAW that can be depleted
        before crop stress occurs.

    Returns
    -------
    float
        Readily available water (mm).
    """

    if taw <= 0:
        raise ValueError(
            "TAW must be greater than zero."
        )

    if not 0 < depletion_fraction < 1:
        raise ValueError(
            "Depletion fraction must be between 0 and 1."
        )

    raw = taw * depletion_fraction

    return raw


# calculate root zone depletion (Dr).

def calculate_root_zone_depletion(
    taw,
    soil_water
):
    """
    Calculate root-zone water depletion.

    Parameters
    ----------
    taw : float
        Total available water in the root zone (mm).

    soil_water : float
        Current available soil water in the root zone (mm).

    Returns
    -------
    float
        Root-zone depletion (mm).

    Formula
    -------
    Dr = TAW - available soil water
    """

    if taw <= 0:
        raise ValueError(
            "TAW must be greater than zero."
        )

    if soil_water < 0:
        raise ValueError(
            "Soil water cannot be negative."
        )

    if soil_water > taw:
        raise ValueError(
            "Soil water cannot exceed TAW."
        )

    depletion = taw - soil_water

    return depletion

# step 7, Determine whether irrigation is required based on root zone depletion (Dr) and readily available water (RAW).

def calculate_root_zone_depletion(
    taw,
    soil_water
):
    """
    Calculate root-zone water depletion.

    Parameters
    ----------
    taw : float
        Total available water in the root zone (mm).

    soil_water : float
        Current available soil water in the root zone (mm).

    Returns
    -------
    float
        Root-zone depletion (mm).

    Formula
    -------
    Dr = TAW - available soil water
    """

    if taw <= 0:
        raise ValueError(
            "TAW must be greater than zero."
        )

    if soil_water < 0:
        raise ValueError(
            "Soil water cannot be negative."
        )

    if soil_water > taw:
        raise ValueError(
            "Soil water cannot exceed TAW."
        )

    depletion = taw - soil_water

    return depletion

# step 8, calculate the FAO-based net irrigation requirement.

def calculate_net_irrigation(
    root_zone_depletion,
    taw
):
    """
    Calculate net irrigation required to refill
    the root zone to field capacity.

    Parameters
    ----------
    root_zone_depletion : float
        Current root-zone depletion (mm).

    taw : float
        Total available water (mm).

    Returns
    -------
    float
        Net irrigation requirement (mm).
    """

    if root_zone_depletion < 0:
        raise ValueError(
            "Root-zone depletion cannot be negative."
        )

    if taw <= 0:
        raise ValueError(
            "TAW must be greater than zero."
        )

    if root_zone_depletion > taw:
        raise ValueError(
            "Depletion cannot exceed TAW."
        )

    return root_zone_depletion


# step 9, account for irrigation efficiency to calculate gross irrigation requirement.

def calculate_gross_irrigation(
    net_irrigation,
    irrigation_efficiency
):
    """
    Calculate gross irrigation depth.

    Formula:
        Gross irrigation = Net irrigation / efficiency

    Parameters
    ----------
    net_irrigation : float
        Net irrigation requirement (mm).

    irrigation_efficiency : float
        Application efficiency as a decimal.

    Returns
    -------
    float
        Gross irrigation depth (mm).
    """

    if net_irrigation < 0:
        raise ValueError(
            "Net irrigation cannot be negative."
        )

    if not 0 < irrigation_efficiency <= 1:
        raise ValueError(
            "Irrigation efficiency must be between 0 and 1."
        )

    gross_irrigation = (
        net_irrigation / irrigation_efficiency
    )

    return gross_irrigation


# step 10, effective rainfall calculation.
# made with the assumption that 80% of rainfall is effective.
def calculate_effective_rainfall(rainfall):
    """
    Calculate effective rainfall.

    Parameters
    ----------
    rainfall : float
        Total rainfall (mm).

    Returns
    -------
    float
        Effective rainfall (mm).
    """
    if rainfall < 0:
        raise ValueError(
            "Rainfall cannot be negative."
        )

    effective_rainfall = rainfall * 0.8

    return effective_rainfall

# Step 11, update root-zone depletion after rainfall and irrigation.

def update_root_zone_depletion(
    previous_depletion,
    etc,
    effective_rainfall,
    irrigation,
    taw
):
    """
    Update root-zone depletion using a daily water balance.

    Formula:

        Dr_new = Dr_previous + ETc
                 - P_eff - I

    Parameters
    ----------
    previous_depletion : float
        Root-zone depletion at the beginning of the day (mm).

    etc : float
        Crop evapotranspiration (mm/day).

    effective_rainfall : float
        Effective rainfall (mm/day).

    irrigation : float
        Net irrigation entering the root zone (mm/day).

    taw : float
        Total available water (mm).

    Returns
    -------
    float
        Updated root-zone depletion (mm).
    """

    if taw <= 0:
        raise ValueError(
            "TAW must be greater than zero."
        )

    if previous_depletion < 0:
        raise ValueError(
            "Previous depletion cannot be negative."
        )

    if previous_depletion > taw:
        raise ValueError(
            "Previous depletion cannot exceed TAW."
        )

    if etc < 0:
        raise ValueError(
            "ETc cannot be negative."
        )

    if effective_rainfall < 0:
        raise ValueError(
            "Rainfall cannot be negative."
        )

    if irrigation < 0:
        raise ValueError(
            "Irrigation cannot be negative."
        )

    depletion = (
        previous_depletion
        + etc
        - effective_rainfall
        - irrigation
    )

    # Depletion cannot be negative.
    depletion = max(depletion, 0)

    # Depletion cannot exceed TAW.
    depletion = min(depletion, taw)

    return depletion

## Should irrigate based on FAO-56 RAW threshold.
def fao_should_irrigate(
    root_zone_depletion,
    raw
):
    """
    Determine whether irrigation is required
    using the FAO-56 RAW threshold.

    Irrigation is required when:

        Dr >= RAW

    Parameters
    ----------
    root_zone_depletion : float
        Current root-zone depletion (mm).

    raw : float
        Readily available water (mm).

    Returns
    -------
    bool
        True if irrigation is required.
    """

    if root_zone_depletion < 0:
        raise ValueError(
            "Root-zone depletion cannot be negative."
        )

    if raw <= 0:
        raise ValueError(
            "RAW must be greater than zero."
        )

    return root_zone_depletion >= raw

## calculate daily irrigation requirement based on ET0, Kc, rainfall, previous depletion, TAW, RAW, and irrigation efficiency.

def calculate_daily_irrigation(
    et0,
    kc,
    rainfall,
    previous_depletion,
    taw,
    raw,
    irrigation_efficiency=0.80
):
    """
    Calculate daily crop water use and irrigation requirement.

    Returns
    -------
    dict
        Daily irrigation results.
    """

    # 1. Crop evapotranspiration
    etc = calculate_etc(
        et0,
        kc
    )

    # 2. Effective rainfall
    effective_rainfall = calculate_effective_rainfall(
        rainfall
    )

    # 3. Depletion before irrigation
    depletion_before_irrigation = (
        update_root_zone_depletion(
            previous_depletion=previous_depletion,
            etc=etc,
            effective_rainfall=effective_rainfall,
            irrigation=0,
            taw=taw
        )
    )

    # 4. Irrigation decision
    irrigate = fao_should_irrigate(
        root_zone_depletion=depletion_before_irrigation,
        raw=raw
    )

    # 5. Calculate irrigation requirement
    if irrigate:

        net_irrigation = calculate_net_irrigation(
            root_zone_depletion=
                depletion_before_irrigation,
            taw=taw
        )

        gross_irrigation = calculate_gross_irrigation(
            net_irrigation=net_irrigation,
            irrigation_efficiency=
                irrigation_efficiency
        )

    else:

        net_irrigation = 0
        gross_irrigation = 0

    # 6. Final depletion after irrigation
    final_depletion = update_root_zone_depletion(
        previous_depletion=previous_depletion,
        etc=etc,
        effective_rainfall=effective_rainfall,
        irrigation=net_irrigation,
        taw=taw
    )

    return {
        "ET0": et0,
        "Kc": kc,
        "ETc": etc,
        "rainfall": rainfall,
        "effective_rainfall": effective_rainfall,
        "TAW": taw,
        "RAW": raw,
        "depletion_before_irrigation":
            depletion_before_irrigation,
        "irrigate": irrigate,
        "net_irrigation":
            net_irrigation,
        "gross_irrigation":
            gross_irrigation,
        "final_depletion":
            final_depletion
    }

##
def calculate_daily_irrigation_for_crop(
    et0,
    rainfall,
    previous_depletion,
    planting_date,
    current_date,
    root_depth=0.60,
    irrigation_efficiency=0.80
):
    """
    Calculate daily irrigation requirement for a tomato crop.

    Kc is obtained from the crop calendar.
    TAW and RAW are obtained from the Muguga soil profile.
    """

    # 1. Determine crop growth stage
    growth_stage = get_growth_stage(
        current_date,
        planting_date
    )

    # 2. Determine Kc
    kc = get_kc(
        current_date,
        planting_date
    )

    # Crop is outside the active growing period
    if growth_stage is None or kc is None:

        return {
            "growth_stage": None,
            "Kc": None,
            "ET0": et0,
            "ETc": 0,
            "irrigate": False,
            "net_irrigation": 0,
            "gross_irrigation": 0
        }

    # 3. Load Muguga soil-water parameters
    soil_water = get_muguga_water_parameters(
        root_depth=root_depth
    )

    taw = soil_water["TAW"]
    raw = soil_water["RAW"]

    # 4. Run irrigation engine
    result = calculate_daily_irrigation(
        et0=et0,
        kc=kc,
        rainfall=rainfall,
        previous_depletion=previous_depletion,
        taw=taw,
        raw=raw,
        irrigation_efficiency=irrigation_efficiency
    )

    # 5. Add crop and soil information
    result["growth_stage"] = growth_stage
    result["root_depth"] = root_depth
    result["field_capacity"] = soil_water["field_capacity"]
    result["wilting_point"] = soil_water["wilting_point"]

    return result
