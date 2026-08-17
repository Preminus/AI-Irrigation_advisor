# 🌱 AI Irrigation Advisor for Tomato Production

An AI-based irrigation decision-support system that combines **FAO-56 evapotranspiration modelling, soil-water balance, crop growth information, and machine learning** to predict when tomato crops require irrigation and estimate the amount of water required.

> **Project status:** Prototype / Research Project

---

## 📌 Project Overview

Efficient irrigation is essential for tomato production. Too little water can cause crop stress and reduced yields, while excessive irrigation can waste water, increase production costs, and contribute to nutrient leaching.

Many irrigation decisions are still based on fixed schedules, experience, or visual observation. However, crop water requirements change continuously with weather conditions, crop growth stage, rainfall, evapotranspiration, and soil-water availability.

This project develops a hybrid **AI Irrigation Advisor** that combines established agricultural water-balance methods with machine learning.

The system answers two main questions:

1. **Should the tomato crop be irrigated today?**
2. **If irrigation is required, how much water should be applied?**

---

# 🎯 Problem Statement

Tomato growers often make irrigation decisions using fixed schedules or personal judgement, which can result in over-irrigation, under-irrigation, and inefficient water use.

This project aims to predict whether tomato crops require irrigation and estimate the amount of water required using **weather, crop-growth, evapotranspiration, rainfall, and soil-water features**.

The classification model is primarily evaluated using **recall for irrigation events**, while the regression model is evaluated using **MAE, RMSE, and R²**.

---

# 🎯 Objectives

## Main Objective

To develop an AI-based irrigation advisor for tomato production using weather, crop, and soil-water information.

## Specific Objectives

- Calculate reference evapotranspiration (ET₀) using the FAO-56 Penman-Monteith equation method.
- Estimate crop evapotranspiration (ETc).
- Develop a tomato crop growth calendar and crop coefficients.
- Model root-zone soil-water depletion.
- Determine irrigation events using readily available water (RAW).
- Develop a classification model for irrigation decisions.
- Develop a regression model for irrigation quantity.
- Compare machine-learning models.
- Develop a foundation for a farmer-facing irrigation decision-support system.

---

# 🧠 System Architecture

The project follows a hybrid **agronomic + machine-learning** architecture:

```text
                WEATHER DATA
                     │
                     ▼
          ┌────────────────────┐
          │      FAO-56        │
          │   Penman-Monteith  │
          └─────────┬──────────┘
                    │
                   ET₀
                    │
                    ▼
          ┌────────────────────┐
          │  Tomato Crop       │
          │  Calendar + Kc     │
          └─────────┬──────────┘
                    │
                   ETc
                    │
                    ▼
          ┌────────────────────┐
          │   Soil-Water       │
          │     Balance        │
          └─────────┬──────────┘
                    │
             Soil Depletion
                    │
                    ▼
          ┌────────────────────┐
          │ Feature Engineering│
          └─────────┬──────────┘
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
   CLASSIFICATION        REGRESSION
   "Irrigate?"           "How much?"
          │                   │
          └─────────┬─────────┘
                    ▼
          IRRIGATION ADVISORY
````

---

# 🌦️ Data

The project uses **10 years of daily weather data (2016–2025)**.

The original dataset contains **3,653 daily observations**.

### Weather variables

* Temperature
* Maximum temperature
* Minimum temperature
* Relative humidity
* Rainfall
* Wind speed
* Solar radiation

### Derived agricultural variables

* Mean temperature (`Tmean`)
* Reference evapotranspiration (`ET0`)
* Crop age
* Growth stage
* Crop coefficient (`Kc`)
* Crop evapotranspiration (`ETc`)
* Effective rainfall
* Soil-water depletion
* Total Available Water (`TAW`)
* Readily Available Water (`RAW`)

---

# 💧 FAO-56 Reference Evapotranspiration

Reference evapotranspiration is calculated using the **FAO-56 Penman-Monteith method**.

ET₀ represents atmospheric evaporative demand and provides the foundation for calculating crop water requirements.

### ET₀ diagnostics

| Metric         |        Value |
| -------------- | -----------: |
| Minimum ET₀    | 1.568 mm/day |
| Maximum ET₀    | 7.197 mm/day |
| Mean ET₀       | 4.301 mm/day |
| Missing values |            0 |

The FAO-56 implementation is contained in:

```text
src/fao56.py
```

---

# 🍅 Tomato Crop Calendar

The model uses a **120-day annual tomato production cycle**.

| Growth Stage | Days After Planting |   Kc |
| ------------ | ------------------: | ---: |
| Initial      |                0–29 | 0.60 |
| Development  |               30–59 | 0.90 |
| Mid-season   |               60–89 | 1.15 |
| Late-season  |              90–119 | 0.80 |
| No crop      |                ≥120 | 0.00 |

Crop evapotranspiration is calculated conceptually as:

```text
ETc = ET₀ × Kc
```

The crop calendar is implemented in:

```text
src/crop_calendar.py
```

---

# 🌱 Soil-Water Balance

The irrigation model uses soil-water properties to estimate the amount of water available to the crop.

Current model configuration:

| Parameter                     |  Value |
| ----------------------------- | -----: |
| Field capacity                |   0.30 |
| Wilting point                 |   0.15 |
| Root depth                    | 0.60 m |
| Total Available Water (TAW)   |  90 mm |
| Readily Available Water (RAW) |  36 mm |

The soil-water balance updates root-zone depletion based on:

* crop evapotranspiration,
* effective rainfall,
* and irrigation.

Irrigation is triggered when depletion reaches the RAW threshold.

---

# 🚿 Irrigation Simulation Results

Using the ten-year weather dataset and the agronomic water-balance model, the system generated:

| Metric                 |          Result |
| ---------------------- | --------------: |
| Irrigation events      |          **87** |
| Total net irrigation   | **3,367.47 mm** |
| Irrigation efficiency  |         **80%** |
| Total gross irrigation | **4,209.33 mm** |

Gross irrigation accounts for application losses using the assumed irrigation efficiency.

---

# 🤖 Machine Learning

The project uses two machine-learning tasks.

## 1. Classification — Should We Irrigate?

Target:

```text
irrigate
```

where:

```text
False → No irrigation
True  → Irrigation required
```

### Class imbalance

The original dataset contained:

```text
No irrigation: 3566
Irrigation:      87
```

Therefore, irrigation events represented only about **2.4%** of all observations.

To address this imbalance, **SMOTE (Synthetic Minority Over-sampling Technique)** was applied to the training set only.

### Classification results

| Class         | Precision |   Recall | F1-score |
| ------------- | --------: | -------: | -------: |
| No irrigation |      1.00 |     0.91 |     0.95 |
| Irrigation    |      0.16 | **0.93** |     0.28 |

Confusion matrix:

```text
[[650, 66],
 [  1, 13]]
```

The model detected **13 of the 14 irrigation events** in the test set.

Because irrigation is a rare event, recall for the irrigation class is more informative than overall accuracy alone.

---

# 📊 Feature Importance

The most important classification features were:

| Feature  | Importance |
| -------- | ---------: |
| ETc_3day |     17.21% |
| ETc_7day |     16.07% |
| crop_age |     14.67% |
| Kc       |     10.85% |
| ET0_7day |      7.73% |
| ET0      |      5.99% |
| ET0_lag1 |      4.96% |

The results indicate that **recent crop water demand and crop development stage** are particularly important in determining irrigation requirements.

---

# 📈 Regression — How Much Water?

Once irrigation is predicted to be necessary, the regression model estimates the required irrigation amount in millimetres.

Three models were compared:

* Random Forest
* Gradient Boosting
* Extra Trees

### Model comparison

| Model             | MAE (mm) | RMSE (mm) |        R² |
| ----------------- | -------: | --------: | --------: |
| **Extra Trees**   | **1.32** |  **1.51** | **0.305** |
| Random Forest     |     1.32 |      1.54 |     0.276 |
| Gradient Boosting |     1.46 |      1.76 |     0.057 |

### Selected model

**Extra Trees Regressor**

The model achieved:

* **MAE:** 1.32 mm
* **RMSE:** 1.51 mm
* **R²:** 0.305

The regression model was trained on irrigation events only.

---

# 🧪 Handling Multicollinearity

Several features naturally contain related information, for example:

* ET₀ and ET₀ rolling features
* ETc and ETc rolling features
* temperature-derived variables

The project managed this through:

* feature selection,
* feature importance analysis,
* model-performance comparison,
* and the use of tree-based models.

The final models are based on **Random Forest and Extra Trees**, which are less sensitive to multicollinearity than coefficient-based linear models.

A future improvement would be to explicitly evaluate feature correlation and **Variance Inflation Factor (VIF)** before final feature selection.



# ⚠️ Limitations

This project is currently a **prototype/research decision-support system**.

The current machine-learning targets are primarily derived from the FAO-56 soil-water-balance framework rather than a large dataset of directly observed farmer irrigation decisions.

Other limitations include:

* Only 87 irrigation events were generated.
* The regression test set was relatively small.
* The current soil scenario uses fixed soil parameters.
* Effective rainfall is represented using a simplified assumption.
* The classification model has relatively low irrigation precision.
* The regression model has moderate predictive performance.

Therefore, the current system should **not yet be treated as a field-ready autonomous irrigation controller**.

---

# 🔭 Future Work

Future development will focus on:

* Collecting real farmer irrigation records.
* Integrating soil-moisture sensors.
* Validating soil-water depletion against field measurements.
* Incorporating real-time weather forecasts.
* Improving rainfall effectiveness estimation.
* Using farm-specific planting dates.
* Expanding the dataset across farms and soil types.
* Optimizing classification thresholds.
* Testing additional machine-learning algorithms.
* Developing a web/mobile farmer-facing interface.
* Integrating the advisor with automated irrigation systems.

---

# 👨🏽‍💻 Author

**Preminus Karani**

BSc Agricultural and Biosystems Engineering
Jomo Kenyatta University of Agriculture and Technology (JKUAT)

**George Mutuma**

### Areas of interest

* Precision Agriculture
* Artificial Intelligence
* Data Science
* Smart Irrigation
* Agricultural Engineering

---

# 📌 Project Status

**Prototype / Research Project**

The current system demonstrates the feasibility of combining **FAO-56 crop-water modelling with machine learning** for irrigation decision support.

The next major step is **field validation using actual soil-moisture measurements and irrigation records**.

---

## 📜 Disclaimer

This project is intended for research and decision-support purposes. Irrigation recommendations should be validated against local soil conditions, weather conditions, crop requirements and agronomic expertise before operational use.

