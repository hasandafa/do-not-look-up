# 📖 Data Dictionary

**Don't Look Up: NASA Asteroid Dataset**  
*Created by Abdullah Hasan Dafa (@hasandafa)*

---

## 🎯 Overview

This document provides detailed information about each column in the asteroid dataset, including data types, value ranges, and interpretation guidelines.

---

## 📊 Column Specifications

### 1. `asteroid_designation`

**Type**: String  
**Example**: `"2023 XY1"`, `"Apophis"`, `"(99942)"`

**Description**:  
Official designation assigned by the Minor Planet Center (MPC). This is the asteroid's unique identifier in astronomical databases.

**Format Patterns**:
- **Provisional**: `YYYY ABC` (e.g., "2023 XY1") - Recently discovered
- **Numbered**: `(12345)` - Well-established orbit
- **Named**: May include common name (e.g., "Apophis", "Bennu")

**Notes**:
- Not all asteroids have official names
- Designation format indicates discovery era
- Can be used as unique key for joining datasets

---

### 2. `close_approach_date`

**Type**: DateTime  
**Format**: `YYYY-MM-DD HH:MM:SS`  
**Example**: `2029-04-13 21:46:00`

**Description**:  
The exact date and time (UTC) when the asteroid reaches its closest point to Earth during this particular approach.

**Value Range**: 2020-01-01 to 2100-12-31

**Time Zone**: Coordinated Universal Time (UTC)

**Notes**:
- Calculated using NASA's orbital models
- Precision: ±minutes for near-term, ±hours for distant future
- Can be used for temporal analysis and time series modeling

**Use Cases**:
- Filter approaches by date range
- Analyze seasonal patterns
- Build time series forecasts

---

### 3. `year`

**Type**: Integer  
**Range**: 2020 - 2100  
**Example**: `2029`

**Description**:  
Extracted year from `close_approach_date` for easy filtering and grouping.

**Distribution**: Roughly uniform across the range, with slight variations due to orbital mechanics.

**Use Cases**:
- Aggregate approaches by year
- Identify peak years for approaches
- Temporal trend analysis

---

### 4. `month`

**Type**: Integer  
**Range**: 1 - 12  
**Example**: `4` (April)

**Description**:  
Extracted month from `close_approach_date`.

**Month Mapping**:
- 1 = January, 2 = February, ..., 12 = December

**Use Cases**:
- Detect seasonal patterns
- Monthly distribution analysis
- Identify if certain months have more approaches

---

### 5. `distance_au`

**Type**: Float  
**Unit**: Astronomical Units (AU)  
**Range**: 0.0001 - 0.2000  
**Example**: `0.0234`

**Description**:  
Minimum distance between the asteroid and Earth during the close approach, measured in Astronomical Units.

**Unit Conversion**:
- 1 AU = 149,597,871 km
- 1 AU = 92,955,807 miles
- To convert to km: `distance_au * 149597870.7`

**Distance Context**:
- < 0.002 AU (~300,000 km): Closer than Moon's orbit
- < 0.05 AU (~7.5M km): Notably close
- 0.05 - 0.1 AU: Moderate distance
- > 0.1 AU: Relatively far

**Statistical Summary**:
- Mean: ~0.08 AU
- Median: ~0.07 AU
- Min: ~0.0001 AU (very rare!)
- Max: 0.2 AU (filter cutoff)

**Notes**:
- Lower values = closer approach = higher concern
- Used heavily in risk score calculation
- Most approaches are > 0.05 AU (safe distance)

---

### 6. `velocity_km_s`

**Type**: Float  
**Unit**: Kilometers per second (km/s)  
**Range**: 5 - 70  
**Example**: `28.5`

**Description**:  
Relative velocity of the asteroid with respect to Earth at the time of closest approach.

**Velocity Context**:
- < 15 km/s: Relatively slow
- 15 - 30 km/s: Typical asteroid velocity
- 30 - 50 km/s: Fast-moving
- > 50 km/s: Extremely fast (comets or hyperbolic orbits)

**Reference Points**:
- Earth's orbital velocity: ~30 km/s
- Escape velocity from Earth: 11.2 km/s
- Typical meteorite impact: 11-72 km/s

**Energy Implications**:
Higher velocity = more kinetic energy = greater potential impact damage  
**Formula**: KE = ½ × mass × velocity²

**Statistical Summary**:
- Mean: ~20 km/s
- Median: ~18 km/s
- Standard deviation: ~8 km/s

**Use Cases**:
- Energy calculations
- Orbit type classification
- Risk assessment component

---

### 7. `absolute_magnitude`

**Type**: Float  
**Symbol**: H  
**Range**: 10 - 30  
**Example**: `19.7`

**Description**:  
The asteroid's brightness at a standard distance of 1 AU from both the Sun and Earth, with a phase angle of 0°. This is an intrinsic property related to size.

**Magnitude Scale**:
- **Lower H = Brighter = Larger asteroid**
- H < 18: Very large (> 1 km diameter)
- H 18-22: Large (140m - 1km)
- H 22-25: Medium (40-140m)
- H > 25: Small (< 40m)

**Approximate Size Conversion** (for typical albedo ~0.14):
```
Diameter (km) ≈ 1329 / √(albedo) × 10^(-H/5)
```

**Example Conversions**:
- H = 15 → ~5 km diameter (planet killer)
- H = 20 → ~500m diameter (regional devastation)
- H = 25 → ~50m diameter (Chelyabinsk meteor size)

**Notes**:
- Assumes average reflectivity (albedo = 0.14)
- Actual size can vary based on composition
- Darker asteroids appear smaller at same H

**Use Cases**:
- Estimate asteroid size
- Filter by potential impact severity
- Size distribution analysis

---

### 8. `days_until_approach`

**Type**: Integer  
**Range**: -18,000 to +27,000 (approximately)  
**Example**: `1547`

**Description**:  
Number of days between the current date (dataset generation date) and the close approach date.

**Value Interpretation**:
- **Positive**: Future approach (hasn't happened yet)
- **Negative**: Past approach (already occurred)
- **Zero**: Happening today (very rare in dataset)

**Use Cases**:
- Filter for upcoming vs historical approaches
- Priority ranking (lower positive = more urgent)
- Time-based risk weighting
- Create countdowns

**Example Filtering**:
```python
# Next 30 days
urgent = df[df['days_until_approach'].between(0, 30)]

# Next year
upcoming_year = df[df['days_until_approach'].between(0, 365)]

# Historical
past = df[df['days_until_approach'] < 0]
```

---

### 9. `is_past_event`

**Type**: Boolean  
**Values**: `True` or `False`  
**Example**: `False`

**Description**:  
Flag indicating whether this close approach has already occurred (True) or is still in the future (False).

**Distribution**:
- True: ~40-50% (historical data)
- False: ~50-60% (future predictions)

**Use Cases**:
- Quickly filter historical vs predictive data
- Training/testing split for ML models
- Validation of past predictions

**Relationship**: `is_past_event = (days_until_approach < 0)`

---

### 10. `is_future_event`

**Type**: Boolean  
**Values**: `True` or `False`  
**Example**: `True`

**Description**:  
Flag indicating whether this close approach is still upcoming (True) or has already happened (False).

**Relationship**: `is_future_event = (days_until_approach >= 0)`

**Note**: `is_future_event` and `is_past_event` are mutually exclusive (one is always the inverse of the other).

**Use Cases**:
- Focus on upcoming threats
- Real-time monitoring systems
- Alert systems

---

### 11. `risk_score`

**Type**: Float  
**Range**: 0.0 - 1.0  
**Example**: `0.234`

**Description**:  
Custom calculated risk metric combining distance, velocity, and temporal urgency. Higher score = higher perceived risk.

**Calculation Formula**:
```python
risk_score = (
    distance_risk * 0.40 +   # Normalized inverse distance
    velocity_risk * 0.30 +   # Normalized velocity
    time_risk * 0.30         # Normalized urgency (for future events)
)
```

**Component Weights**:
- Distance: 40% (most important factor)
- Velocity: 30% (kinetic energy consideration)
- Time: 30% (urgency for future events only)

**Score Interpretation**:
- 0.0 - 0.2: Low risk (SAFE)
- 0.2 - 0.4: Moderate monitoring (MONITOR)
- 0.4 - 0.7: Elevated concern (CONCERN)
- 0.7 - 1.0: High priority (OH_NO)

**Important Notes**:
- This is an **educational metric**, not official NASA risk assessment
- Does not include orbital uncertainties
- Real impact probability requires complex orbital mechanics
- For actual risk assessment, see NASA's Sentry system

**Use Cases**:
- Relative comparison between asteroids
- Prioritization for monitoring
- Feature for ML models
- Educational demonstrations

---

### 12. `panic_level`

**Type**: Integer  
**Range**: 0 - 10  
**Example**: `2`

**Description**:  
Discrete risk level on a 0-10 scale, derived from `risk_score` for easier interpretation.

**Calculation**: `panic_level = round(risk_score * 10)`

**Level Guide**:
- **0-2**: Chill. You're fine.
- **3-4**: Mildly interesting. Worth a tweet.
- **5-7**: Getting spicy. Maybe read up on it.
- **8-10**: This is what NASA gets paid for.

**Distribution**:
- 0-2: ~85% of dataset
- 3-4: ~12% of dataset  
- 5-7: ~2.5% of dataset
- 8-10: ~0.5% of dataset (rare!)

**Use Cases**:
- Quick visual assessments
- Dashboard color coding
- Alert thresholds
- Public communication

---

### 13. `threat_category`

**Type**: String (Categorical)  
**Values**: `SAFE`, `MONITOR`, `CONCERN`, `OH_NO`  
**Example**: `"MONITOR"`

**Description**:  
Human-readable threat classification based on `panic_level`.

**Category Mapping**:

| Category | Panic Level | % of Dataset | Color Code |
|----------|-------------|--------------|------------|
| **SAFE** | 0-2 | ~85% | 🟢 Green |
| **MONITOR** | 3-4 | ~12% | 🟡 Yellow |
| **CONCERN** | 5-7 | ~2.5% | 🟠 Orange |
| **OH_NO** | 8-10 | ~0.5% | 🔴 Red |

**Category Meanings**:
- **SAFE**: No cause for concern. Business as usual.
- **MONITOR**: Worth keeping an eye on, but not urgent.
- **CONCERN**: Elevated attention recommended.
- **OH_NO**: Top priority for tracking and analysis.

**Use Cases**:
- Quick filtering by risk level
- Dashboard categorization
- Alert routing
- Public reporting

**Note**: Even "OH_NO" asteroids typically have very low absolute impact probabilities. Categories represent relative risk within this dataset.

---

### 14. `panic_verdict`

**Type**: String  
**Example**: `"Worth a tweet, not worth a bunker."`

**Description**:  
Humorous but informative human-readable verdict about the threat level. Maps directly to `threat_category`.

**Verdict Mapping**:

| Category | Verdict |
|----------|---------|
| SAFE | "You're fine. Go touch grass." |
| MONITOR | "Worth a tweet, not worth a bunker." |
| CONCERN | "Time to learn survival skills?" |
| OH_NO | "Did you backup your data?" |

**Purpose**:
- Make data more engaging and accessible
- Reduce anxiety while maintaining accuracy
- Educational communication
- Social media content

**Tone**: Casual, slightly sarcastic, but grounded in real data

**Use Cases**:
- User-facing dashboards
- Social media posts
- Educational materials
- Gamification elements

---

## 📈 Statistical Summary

### Numerical Columns

```
distance_au:
  Mean: 0.082 AU
  Median: 0.074 AU
  Std Dev: 0.045 AU
  Min: 0.0001 AU
  Max: 0.2 AU

velocity_km_s:
  Mean: 20.3 km/s
  Median: 18.7 km/s
  Std Dev: 8.2 km/s
  Min: 5.1 km/s
  Max: 72.5 km/s

absolute_magnitude:
  Mean: 23.5
  Median: 24.1
  Std Dev: 2.8
  Min: 10.2
  Max: 30.5

risk_score:
  Mean: 0.18
  Median: 0.15
  Std Dev: 0.14
  Min: 0.001
  Max: 0.98

panic_level:
  Mean: 1.8
  Median: 1.5
  Std Dev: 1.4
  Min: 0
  Max: 10
```

---

## 🔗 Relationships Between Columns

### Key Dependencies

1. **Date Fields**:
   - `year` and `month` are derived from `close_approach_date`
   - `days_until_approach` calculated from `close_approach_date`

2. **Boolean Flags**:
   - `is_past_event = (days_until_approach < 0)`
   - `is_future_event = (days_until_approach >= 0)`
   - These are mutually exclusive

3. **Risk Metrics**:
   - `risk_score` → derived from distance, velocity, and time
   - `panic_level` = `round(risk_score * 10)`
   - `threat_category` → binned from `panic_level`
   - `panic_verdict` → mapped from `threat_category`

### Correlation Matrix (Key Variables)

```
                   distance_au  velocity_km_s  risk_score
distance_au            1.00        -0.12        -0.82
velocity_km_s         -0.12         1.00         0.34
risk_score            -0.82         0.34         1.00
```

**Insights**:
- Strong negative correlation between distance and risk (-0.82)
- Moderate positive correlation between velocity and risk (0.34)
- Weak negative correlation between distance and velocity (-0.12)

---

## 🎯 Data Quality Notes

### Completeness

| Column | Missing Values | Notes |
|--------|----------------|-------|
| `asteroid_designation` | 0% | Required field |
| `close_approach_date` | 0% | Required field |
| `distance_au` | 0% | Required field |
| `velocity_km_s` | <0.1% | Occasionally missing for very distant future |
| `absolute_magnitude` | ~2% | Not available for all asteroids |
| All other columns | 0% | Calculated or derived |

### Data Cleaning Applied

✅ **Removed**: Records with missing critical values (distance, date)  
✅ **Converted**: All numeric strings to proper float/int types  
✅ **Standardized**: Date formats to ISO 8601  
✅ **Validated**: Distance values within 0-0.2 AU range  
✅ **Calculated**: All derived columns with consistent methodology  

---

## 💡 Usage Tips & Best Practices

### For Machine Learning

**Classification Tasks**:
```python
# Target variable
y = df['threat_category']

# Feature selection (avoid data leakage!)
features = [
    'distance_au', 
    'velocity_km_s', 
    'absolute_magnitude',
    'days_until_approach'  # Use with caution
]
X = df[features]

# Don't use: risk_score, panic_level (these are derived from target)
```

**Regression Tasks**:
```python
# Predicting distance
X = df[['velocity_km_s', 'absolute_magnitude', 'year', 'month']]
y = df['distance_au']

# Predicting velocity
X = df[['distance_au', 'absolute_magnitude', 'year']]
y = df['velocity_km_s']
```

### For Time Series Analysis

```python
# Set datetime index
df['close_approach_date'] = pd.to_datetime(df['close_approach_date'])
df_ts = df.set_index('close_approach_date').sort_index()

# Resample by month
monthly = df_ts.resample('M').size()

# Analyze trends
from statsmodels.tsa.seasonal import seasonal_decompose
decomposition = seasonal_decompose(monthly, model='additive')
```

### For Visualization

```python
# Color mapping by threat category
color_map = {
    'SAFE': '#00ff00',
    'MONITOR': '#ffff00', 
    'CONCERN': '#ff9900',
    'OH_NO': '#ff0000'
}

# Size by absolute magnitude (inverse - smaller H = bigger asteroid)
df['size'] = 30 - df['absolute_magnitude']

# Plot
import plotly.express as px
fig = px.scatter(
    df, 
    x='close_approach_date', 
    y='distance_au',
    color='threat_category',
    size='size',
    color_discrete_map=color_map,
    hover_data=['asteroid_designation', 'velocity_km_s']
)
```

---

## 🔍 Common Queries & Filters

### Find Specific Events

```python
# Closest approach ever
closest = df.nsmallest(1, 'distance_au')

# Fastest asteroid
fastest = df.nlargest(1, 'velocity_km_s')

# Next approach
next_up = df[df['is_future_event']].nsmallest(1, 'days_until_approach')

# Largest asteroid (smallest H magnitude)
largest = df.nsmallest(1, 'absolute_magnitude')
```

### Filter by Risk

```python
# All high-risk asteroids
high_risk = df[df['threat_category'].isin(['CONCERN', 'OH_NO'])]

# Future threats only
future_threats = df[
    (df['is_future_event']) & 
    (df['panic_level'] >= 5)
]

# Very close approaches
very_close = df[df['distance_au'] < 0.01]  # Within 1.5M km
```

### Time-Based Filters

```python
# This decade
this_decade = df[df['year'].between(2020, 2030)]

# Next 5 years
next_5y = df[
    (df['is_future_event']) & 
    (df['days_until_approach'] <= 365*5)
]

# Specific year
year_2029 = df[df['year'] == 2029]

# Summer months (Northern Hemisphere)
summer = df[df['month'].isin([6, 7, 8])]
```

---

## 📚 References & Further Reading

### Understanding Asteroid Data

- **Absolute Magnitude**: [Minor Planet Center - Magnitude System](https://www.minorplanetcenter.net/iau/info/MagScale.html)
- **Orbital Mechanics**: [NASA - Orbital Elements](https://ssd.jpl.nasa.gov/planets/approx_pos.html)
- **Close Approaches**: [CNEOS - Close Approach Tables](https://cneos.jpl.nasa.gov/ca/)

### Risk Assessment

- **Torino Scale**: [NASA - Impact Hazard Scale](https://cneos.jpl.nasa.gov/sentry/torino_scale.html)
- **Palermo Scale**: [Technical Description](https://cneos.jpl.nasa.gov/sentry/palermo_scale.html)
- **Sentry System**: [NASA's Impact Monitoring](https://cneos.jpl.nasa.gov/sentry/)

### Astronomical Units

- **Distance Conversions**: 
  - 1 AU = 149,597,870.7 km
  - 1 AU = 92,955,807.3 miles
  - Moon's orbit: ~0.00257 AU (~384,400 km)
  
---

## ⚠️ Important Caveats

### What This Dataset IS

✅ Real NASA data from official APIs  
✅ Accurate close approach dates and distances  
✅ Educational tool for learning about asteroids  
✅ Good foundation for data science projects  
✅ Demonstrates relative risk assessment methodology  

### What This Dataset IS NOT

❌ Official NASA impact risk assessment  
❌ Comprehensive orbital uncertainty analysis  
❌ Real-time updated (static snapshot)  
❌ Substitute for professional planetary defense systems  
❌ Cause for actual panic  

### Disclaimer

The `risk_score`, `panic_level`, and `threat_category` fields are **educational calculations** designed to demonstrate risk assessment methodology. They are not official NASA risk ratings.

For authoritative impact risk information, always refer to:
- [NASA CNEOS](https://cneos.jpl.nasa.gov/)
- [ESA NEO Coordination Centre](https://neo.esa.int/)
- [IAU Minor Planet Center](https://www.minorplanetcenter.net/)

---

## 🤝 Contributing & Feedback

### Found an Issue?

If you discover:
- Data inconsistencies
- Calculation errors
- Documentation gaps
- Suggestions for improvement

Please open an issue on GitHub: [hasandafa/do-not-look-up](https://github.com/hasandafa/do-not-look-up)

### Want to Extend This?

Ideas for derivatives:
- Add Sentry impact probabilities
- Include orbital elements (eccentricity, inclination)
- Merge with asteroid composition data
- Add historical impact events
- Include asteroid discovery dates

---

## 📊 Quick Reference Card

| Want to... | Use Column(s) |
|------------|---------------|
| Filter by date | `close_approach_date`, `year`, `month` |
| Find closest approaches | `distance_au` (ascending) |
| Find fastest asteroids | `velocity_km_s` (descending) |
| Estimate size | `absolute_magnitude` (lower = larger) |
| Filter by risk | `threat_category` or `panic_level` |
| Get upcoming events | `is_future_event = True` |
| Calculate urgency | `days_until_approach` |
| Identify specific asteroid | `asteroid_designation` |

---

## 📝 Version History

- **v1.0** (October 2025): Initial release
  - 14 columns
  - ~10,000+ records
  - Date range: 2020-2100
  - Custom risk scoring implemented

---

## 📧 Contact

**Dataset Creator**: Abdullah Hasan Dafa  
**GitHub**: [@hasandafa](https://github.com/hasandafa)  
**Project**: [do-not-look-up](https://github.com/hasandafa/do-not-look-up)

---

<div align="center">

**Remember: Looking up is optional. Understanding the data isn't.**

*Made with 💀 and Python | Data by NASA JPL*

</div>