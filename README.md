# AI-Based Irrigation Advisor for Tomato Production

An AI-based irrigation decision-support system that combines FAO-56 evapotranspiration modelling, soil-water balance and machine learning to predict irrigation requirements for tomato production.

---

## 1. Project Overview

Efficient irrigation is critical for tomato production because both water stress and excessive irrigation can reduce crop productivity and increase water use.

This project develops an AI-based irrigation advisor that uses weather conditions, crop growth stage, evapotranspiration and soil-water characteristics to determine when irrigation is required and estimate the required irrigation amount.

The system combines an agronomic water-balance model with machine learning.

---

## 2. Problem Statement

Tomato growers often rely on fixed irrigation schedules or visual judgement when deciding when and how much to irrigate. These approaches may lead to over-irrigation, under-irrigation and inefficient water use.

This project addresses the problem by predicting:

1. Whether irrigation is required.
2. The estimated irrigation quantity required.

The model uses weather, crop, evapotranspiration and soil-water features.

---

## 3. Objectives

### Main Objective

To develop an AI-based irrigation advisor for tomato production.

### Specific Objectives

- Calculate reference evapotranspiration (ET₀) using the FAO-56 Penman-Monteith method.
- Estimate crop evapotranspiration (ETc).
- Model soil-water depletion using a daily water balance.
- Determine irrigation events using the soil-water balance.
- Develop a classification model for irrigation decisions.
- Develop a regression model for irrigation quantity.
- Evaluate and compare machine learning models.
- Develop a prototype suitable for future field validation.

---

## 4. System Architecture

The system follows the pipeline:

Weather Data
      ↓
Data Preprocessing
      ↓
FAO-56 ET₀
      ↓
Tomato Crop Calendar
      ↓
Crop Coefficient (Kc)
      ↓
Crop Evapotranspiration (ETc)
      ↓
Soil-Water Balance
      ↓
Irrigation Decision
      ↓
Feature Engineering
      ↓
Machine Learning
      ↓
Irrigation Recommendation

---

## 5. Data

The project uses daily weather data containing variables such as:

- Temperature
- Maximum temperature
- Minimum temperature
- Relative humidity
- Rainfall
- Wind speed
- Solar radiation

The integrated modelling dataset contains 3,653 daily observations.

---

## 6. FAO-56 Model

Reference evapotranspiration is calculated using the FAO-56 Penman-Monteith methodology.

The resulting ET₀ values are combined with the tomato crop coefficient:

ETc = ET₀ × Kc

The tomato crop calendar is divided into:

| Growth Stage | Days After Planting | Kc |
|---|---:|---:|
| Initial | 0–29 | 0.60 |
| Development | 30–59 | 0.90 |
| Mid-season | 60–89 | 1.15 |
| Late-season | 90–119 | 0.80 |

---

## 7. Soil-Water Balance

The irrigation model uses:

- Field capacity
- Wilting point
- Root depth
- Total Available Water (TAW)
- Readily Available Water (RAW)
- Effective rainfall
- Crop evapotranspiration
- Soil-water depletion

For the selected soil scenario:

- Field capacity = 0.30
- Wilting point = 0.15
- Root depth = 0.60 m
- TAW = 90 mm
- RAW = 36 mm

Irrigation is triggered when soil-water depletion reaches the RAW threshold.

---

## 8. Feature Engineering

Additional temporal features were created to capture recent water-demand patterns.

Examples include:

- ET₀ lag 1 day
- 3-day ET₀
- 7-day ET₀
- 3-day ETc
- 7-day ETc
- 3-day rainfall
- 7-day rainfall

These features allow the models to account for recent weather and crop-water conditions rather than relying only on a single day's observation.

---

## 9. Classification Model

The classification target is:

```text
irrigate
