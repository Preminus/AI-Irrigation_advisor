"""
crops.py

Crop coefficients (Kc) and crop-related functions.

Author: Preminus Karani
Project: AI Irrigation Advisor
"""

# FAO-56 Tomato Crop Coefficients

TOMATO_KC = {
    "initial": 0.60,
    "development": 0.90,
    "mid": 1.15,
    "late": 0.80,
}


def get_crop_coefficient(crop, stage):
    """
    Returns the crop coefficient (Kc) for a given crop and growth stage.

    Parameters
    ----------
    crop : str
        Crop name

    stage : str
        Growth stage

    Returns
    -------
    float
        Crop coefficient
    """

    crop = crop.lower()
    stage = stage.lower()

    if crop == "tomato":
        if stage not in TOMATO_KC:
            raise ValueError(f"Unknown tomato growth stage: {stage}")

        return TOMATO_KC[stage]

    raise ValueError(f"Crop '{crop}' is not yet supported.")