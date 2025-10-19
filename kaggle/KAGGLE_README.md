# 🌠 Don't Look Up: NASA Asteroid Dataset (2020-2100)

> *"We really did have everything, didn't we?"* - Now with NASA data to prove it.

[![Data Source](https://img.shields.io/badge/data-NASA%20JPL-red.svg)](https://cneos.jpl.nasa.gov/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

**Created by Abdullah Hasan Dafa ([@hasandafa](https://github.com/hasandafa))**

---

## 📋 Dataset Overview

This dataset contains **comprehensive asteroid close approach data** from NASA's Center for Near-Earth Object Studies (CNEOS), covering the period from 2020 to 2100. It includes orbital parameters, physical properties, and custom risk assessments for thousands of asteroids that will (or did) pass close to Earth.

### What Makes This Dataset Unique?

- ✅ **Real NASA Data** - Direct from JPL CNEOS APIs (no synthetic data)
- ✅ **Risk Scores Included** - Custom panic levels (0-10) for each approach
- ✅ **Threat Categories** - Asteroids classified: SAFE → MONITOR → CONCERN → OH_NO
- ✅ **Time Context** - Includes both historical and future approaches
- ✅ **Clean & Ready** - Pre-processed, no missing critical values
- ✅ **ML-Ready** - Features calculated, labels assigned, ready for modeling

### Perfect For:

- 🤖 **Machine Learning** - Classification, regression, time series prediction
- 📊 **Data Visualization** - Interactive dashboards, 3D orbital plots
- 📈 **Time Series Analysis** - Temporal patterns, seasonal trends
- 🔬 **Scientific Research** - Asteroid trajectory analysis, risk assessment
- 🎓 **Educational Projects** - Learn astronomy, data science, and existential dread

---

## 📊 Dataset Statistics

| Metric | Value |
|--------|-------|
| **Total Records** | ~10,000+ asteroid approaches |
| **Date Range** | 2020-01-01 to 2100-12-31 |
| **Data Sources** | 3 NASA APIs (CAD, Sentry, NeoWs) |
| **Features** | 14 columns |
| **File Size** | ~2-5 MB (CSV) |
| **Missing Values** | 0% in critical columns |

### Threat Distribution

- 🟢 **SAFE**: ~85% - "You're fine. Go touch grass."
- 🟡 **MONITOR**: ~12% - "Worth a tweet, not worth a bunker."
- 🟠 **CONCERN**: ~2.5% - "Time to learn survival skills?"
- 🔴 **OH_NO**: ~0.5% - "Did you backup your data?"

---

## 📁 Column Descriptions

| Column Name | Type | Description | Example |
|-------------|------|-------------|---------|
| `asteroid_designation` | string | Official asteroid identifier | "2023 XY1" |
| `close_approach_date` | datetime | Date & time of closest approach | "2029-04-13 21:45:00" |
| `year` | int | Year of approach | 2029 |
| `month` | int | Month of approach | 4 |
| `distance_au` | float | Minimum distance in AU* | 0.0234 |
| `velocity_km_s` | float | Relative velocity in km/s | 28.5 |
| `absolute_magnitude` | float | H magnitude (brightness) | 19.7 |
| `days_until_approach` | int | Days from today (negative = past) | 1547 |
| `is_past_event` | bool | Has this approach already happened? | False |
| `is_future_event` | bool | Is this approach upcoming? | True |
| `risk_score` | float | Custom risk score (0-1) | 0.23 |
| `panic_level` | int | Panic level on scale 0-10 | 2 |
| `threat_category` | string | Risk category | "MONITOR" |
| `panic_verdict` | string | Human-readable verdict | "Worth a tweet..." |

**\*AU = Astronomical Unit** (1 AU = 149,597,871 km = distance from Earth to Sun)

---

## 🎯 Use Cases & Ideas

### Beginner Projects

1. **Visualization Dashboard** - Plot approach timeline, distance distribution
2. **Basic EDA** - Explore patterns, find the closest/fastest asteroids
3. **Risk Analysis** - Analyze which factors contribute most to risk scores

### Intermediate Projects

4. **Classification Model** - Predict threat category from physical features
5. **Time Series Forecasting** - Predict approach frequency over time
6. **Interactive 3D Visualization** - Plot asteroid orbits in solar system

### Advanced Projects

7. **Deep Learning** - LSTM/Transformer for trajectory prediction
8. **Ensemble Models** - Combine multiple approaches for risk assessment
9. **Real-time Tracker** - Build web app that updates with latest NASA data
10. **Impact Probability Calculator** - Estimate collision probabilities

---

## 🔬 Data Sources

This dataset is compiled from **3 official NASA APIs**:

### 1. Close Approach Data (CAD)
- **URL**: https://cneos.jpl.nasa.gov/ca/
- **Purpose**: Timeline of all asteroid close approaches
- **Data**: Dates, distances, velocities, orbital uncertainties

### 2. Sentry Risk Table
- **URL**: https://ssd-api.jpl.nasa.gov/sentry.api
- **Purpose**: Impact risk monitoring for concerning asteroids
- **Data**: Impact probabilities, Palermo Scale, Virtual Impactors

### 3. NeoWs (Near Earth Object Web Service)
- **URL**: https://api.nasa.gov/neo/rest/v1/
- **Purpose**: Detailed asteroid properties
- **Data**: Size, mass, orbital elements, classification

---

## 🤖 Risk Score Methodology

The custom `risk_score` is calculated using a weighted algorithm:

```python
risk_score = (
    distance_risk * 0.40 +    # Closer = higher risk
    velocity_risk * 0.30 +    # Faster = more energy
    time_risk * 0.30          # Sooner = more urgent
)
```

### Threat Categories

| Category | Panic Level | Risk Score | What It Means |
|----------|-------------|------------|---------------|
| **SAFE** | 0-2 | 0.0-0.2 | No cause for concern |
| **MONITOR** | 3-4 | 0.21-0.4 | Worth tracking |
| **CONCERN** | 5-7 | 0.41-0.7 | Elevated attention needed |
| **OH_NO** | 8-10 | 0.71-1.0 | Highest priority monitoring |

**Note**: Even "OH_NO" asteroids typically have very low impact probabilities (<0.01%). The categories are relative risk assessments, not absolute predictions.

---

## 📚 Example Queries

### SQL Examples

```sql
-- Find the closest approach in the dataset
SELECT asteroid_designation, close_approach_date, distance_au
FROM asteroids
ORDER BY distance_au
LIMIT 1;

-- Count approaches per threat category
SELECT threat_category, COUNT(*) as count
FROM asteroids
GROUP BY threat_category
ORDER BY count DESC;

-- Get upcoming high-risk approaches
SELECT *
FROM asteroids
WHERE is_future_event = true 
  AND threat_category IN ('CONCERN', 'OH_NO')
ORDER BY close_approach_date;
```

### Python Examples

```python
import pandas as pd

# Load dataset
df = pd.read_csv('asteroid_dataset.csv')

# Find fastest asteroids
fastest = df.nlargest(10, 'velocity_km_s')

# Upcoming approaches in next year
upcoming = df[
    (df['is_future_event']) & 
    (df['days_until_approach'] <= 365)
]

# Risk distribution visualization
import plotly.express as px
fig = px.pie(df, names='threat_category', 
             title='Asteroid Threat Distribution')
fig.show()
```

---

## 🌟 Featured Asteroids

### Apophis (99942 Apophis)
- **Close Approach**: April 13, 2029
- **Distance**: 0.000255 AU (~38,000 km)
- **Threat**: MONITOR
- **Fun Fact**: Will pass closer than some satellites!

### Bennu (101955 Bennu)
- **OSIRIS-REx Mission Target**
- **Threat**: SAFE
- **Fun Fact**: We literally grabbed a sample from it

### Didymos
- **DART Mission Target** (2022)
- **First Successful Planetary Defense Test**
- **Threat**: SAFE

---

## ⚠️ Important Disclaimers

### Should You Actually Panic?

**No.** Here's why:

1. **Scale Matters**: Even "close" approaches are typically > 18 million km away
2. **We're Watching**: NASA tracks these 24/7 with much better models
3. **Time to Act**: We'd have years/decades of warning for any real threat
4. **Defense Options**: Technologies like DART mission prove we can deflect asteroids

### Data Limitations

- ⚠️ Risk scores are **educational calculations**, not official NASA assessments
- ⚠️ Real impact probabilities require complex orbital mechanics beyond this dataset
- ⚠️ New discoveries may add asteroids not in this dataset
- ⚠️ For real planetary defense info, visit [NASA CNEOS](https://cneos.jpl.nasa.gov/)

---

## 🛠️ Getting Started

### Quick Load (Python)

```python
import pandas as pd

# Load the dataset
df = pd.read_csv('asteroid_dataset.csv', parse_dates=['close_approach_date'])

# Basic info
print(f"Total asteroids: {len(df):,}")
print(f"Date range: {df['close_approach_date'].min()} to {df['close_approach_date'].max()}")
print(f"\nThreat distribution:\n{df['threat_category'].value_counts()}")
```

### Quick Analysis

```python
# Find next close approach
next_approach = df[df['is_future_event']].nsmallest(1, 'days_until_approach')
print(f"Next: {next_approach['asteroid_designation'].values[0]}")
print(f"Date: {next_approach['close_approach_date'].values[0]}")
print(f"Days until: {next_approach['days_until_approach'].values[0]}")
```

---

## 📖 Additional Resources

- **Source Code**: [github.com/hasandafa/do-not-look-up](https://github.com/hasandafa/do-not-look-up)
- **NASA CNEOS**: [cneos.jpl.nasa.gov](https://cneos.jpl.nasa.gov/)
- **API Documentation**: [api.nasa.gov](https://api.nasa.gov/)
- **Film Reference**: [Don't Look Up (2021)](https://www.netflix.com/title/81252357)

---

## 🙏 Acknowledgments

- **NASA JPL** - For tracking space rocks so we don't have to
- **CNEOS Team** - For maintaining amazing APIs
- **Coffee** - For keeping me awake during data processing
- **Existential Dread** - For motivating this project

---

## 📄 License

This dataset is released under the **MIT License**. NASA data is public domain.

Feel free to use, modify, and share this dataset. Just give credit where credit is due!

---

## 📧 Contact & Feedback

**Created by**: Abdullah Hasan Dafa  
**GitHub**: [@hasandafa](https://github.com/hasandafa)  
**Project**: [do-not-look-up](https://github.com/hasandafa/do-not-look-up)

Found this useful? Give it a ⭐ on GitHub!  
Found an issue? Open an issue or submit a PR!

---

<div align="center">

### Current Threat Level: **CHILL** ✅

*Next Notable Approach: Apophis on April 13, 2029*

**Remember: Looking up is optional. The data isn't.**

---

Made with 💀 and Python | Data by NASA | Vibes by Existential Dread

*Last Updated: October 2025*

</div>