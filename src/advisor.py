"""
advisor.py

AI Irrigation Advisory Module

Author: Preminus Karani
Project: AI Irrigation Advisor
"""


def irrigation_advice(gir, rainfall=0):
    """
    Generate a simple irrigation recommendation.

    Parameters
    ----------
    gir : float
        Gross irrigation requirement (mm/day)

    rainfall : float
        Forecast or observed rainfall (mm)

    Returns
    -------
    dict
        Irrigation recommendation
    """

    if rainfall >= gir:
        return {
            "irrigate": False,
            "amount": 0,
            "message": (
                "No irrigation is required today. "
                "Expected rainfall is sufficient."
            ),
        }

    amount = round(gir - rainfall, 2)

    return {
        "irrigate": True,
        "amount": amount,
        "message": (
            f"Apply approximately {amount:.2f} mm of irrigation today."
        ),
    }