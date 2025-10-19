# 🌠 Don't Look Up: Asteroid Impact Tracker

> *"We really did have everything, didn't we?"* - Now with NASA data to prove it.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Gradio](https://img.shields.io/badge/gradio-4.0+-orange.svg)](https://gradio.app/)
[![NASA Data](https://img.shields.io/badge/data-NASA%20JPL-red.svg)](https://cneos.jpl.nasa.gov/)
[![Kaggle Dataset](https://img.shields.io/badge/dataset-Kaggle-20BEFF.svg)](https://www.kaggle.com/datasets/hasandafa1201/nasa-asteroid-impact-dataset)
[![Vibes](https://img.shields.io/badge/vibes-apocalyptic-purple.svg)]()
[![Coffee Powered](https://img.shields.io/badge/powered%20by-coffee%20%26%20anxiety-brown.svg)]()

**Created by Abdullah Hasan Dafa ([@hasandafa](https://github.com/hasandafa))**

---

## 🎬 What Is This?

Ever watched *Don't Look Up* and thought, "I wish I had a way to track actual asteroid threats while simultaneously having an existential crisis"? Well, you're in luck!

This is a **data science project** that combines:
- 📡 Real NASA asteroid data (89,000+ close approaches)
- 🤖 Machine Learning risk predictions
- 📊 Interactive visualizations
- 😅 Dark humor about potential doomsday scenarios

Think of it as your personal apocalypse calendar, but with charts.

---

## ✨ Features

### 🎯 The Panic Meter™
Real-time threat level calculator that tells you if today is the day to panic. Spoiler: it's probably not.

### 📅 Apocalypse Calendar
Interactive timeline of asteroid close approaches from 2020-2100. Mark your (potential) last days!

### 🌌 Doom Simulator 3D
Visualize asteroid orbits in 3D. That tiny dot is Earth. We live there.

### 🤖 Should I Worry?
ML-powered risk predictor. Input asteroid parameters, get a threat level with comedic commentary.

### 🔍 The Watchlist
Search and stalk specific asteroids. Learn about Apophis, Bennu, and other space celebrities.

---

## 🗂️ Dataset

### 📊 Download from Kaggle
**[NASA Asteroid Impact Dataset (2020-2100)](https://www.kaggle.com/datasets/hasandafa1201/nasa-asteroid-impact-dataset)** 

**89,227 asteroid close approaches** with custom risk scoring and official NASA data.

#### Dataset Highlights:
- ✅ **89K+ records** from NASA Close Approach Database
- ✅ **~2K enriched** with Sentry risk assessments
- ✅ **14 features** including distance, velocity, risk scores
- ✅ **Custom metrics** like Panic Level (0-10) and Threat Categories
- ✅ **Time range**: 2020-2100 (if we make it that far)
- ✅ **100% real data** - No synthetic nonsense

#### Quick Stats:
- 📅 **Temporal Coverage**: 80+ years of asteroid approaches
- 🌍 **Distance Range**: 0.000047 AU (really close) to 74.99 AU (chill)
- ⚡ **Velocity Range**: 0.11 km/s to 72.44 km/s
- 🎯 **Risk Categories**: SAFE (93.5%) | MONITOR (5.8%) | CONCERN (0.6%) | OH_NO (0.1%)

---

### 🔧 Or Build It Yourself

This project pulls data from **3 NASA APIs**:

1. **Close Approaches API** - Every asteroid flyby from 1900-2200
2. **Sentry API** - The official "maybe panic?" list (~2,000 risky objects)
3. **NeoWs API** - Detailed profiles of 245,000+ asteroids

**Fun Fact:** We're tracking more asteroids than there are Starbucks locations in the US. Priorities.

---

## 🚀 Quick Start

### Option 1: Use Kaggle Dataset (Recommended)

```bash
# Clone this repository
git clone https://github.com/hasandafa/do-not-look-up.git
cd do-not-look-up

# Install dependencies
pip install -r requirements.txt

# Download dataset from Kaggle
# Visit: https://www.kaggle.com/datasets/hasandafa1201/nasa-asteroid-impact-dataset
# Place the CSV in: data/processed/

# Skip to the analysis notebooks!
jupyter notebook notebooks/03_calculating_extinction.ipynb
```

### Option 2: Fetch Fresh Data from NASA

```bash
# Clone this repository
git clone https://github.com/hasandafa/do-not-look-up.git
cd do-not-look-up

# Install dependencies
pip install -r requirements.txt

# Set up your NASA API key
# Get your key from https://api.nasa.gov/
echo "YOUR_API_KEY_HERE" > nasa_api_key.txt

# Or copy and edit the example
cp nasa_api_key.txt.example nasa_api_key.txt

# Set up config
cp config.yaml.example config.yaml

# Verify setup (optional but recommended)
python scripts/verify_setup.py

# Fetch the data (this takes ~15-20 minutes)
python scripts/fetch_nasa_data.py

# Process and merge datasets
python scripts/process_dataset.py
```

### Explore the Notebooks

```bash
jupyter notebook notebooks/
```

**Notebook Sequence:**
1. `01_fetch_the_doom.ipynb` - Data collection walkthrough
2. `02_exploring_armageddon.ipynb` - EDA & risk scoring
3. `03_calculating_extinction.ipynb` - Advanced analysis (coming soon)
4. `04_predicting_doomsday.ipynb` - ML models (coming soon)
5. `05_visualizing_apocalypse.ipynb` - Visualizations (coming soon)

### Launch the App (Coming Soon)

```bash
cd app
python dont_look_up.py
```

Then open your browser to `http://localhost:7860` and start tracking the apocalypse!

---

## 📊 Project Structure

```
do-not-look-up/
├── README.md                    # You are here
├── QUICK_START.md              # 5-minute setup guide
├── requirements.txt             # Python dependencies
├── config.yaml.example          # NASA API configuration template
├── nasa_api_key.txt.example    # API key template
├── .gitignore                  # Keep secrets secret
│
├── notebooks/                   # Jupyter notebooks
│   ├── 01_fetch_the_doom.ipynb         # Data collection ✅
│   ├── 02_exploring_armageddon.ipynb   # EDA & cleaning ✅
│   ├── 03_calculating_extinction.ipynb # Risk analysis 🚧
│   ├── 04_predicting_doomsday.ipynb    # ML models 🚧
│   └── 05_visualizing_apocalypse.ipynb # Visualizations 🚧
│
├── data/                        # Data files (gitignored)
│   ├── raw/                     # Raw API responses
│   ├── processed/               # Clean datasets
│   └── models/                  # Trained ML models
│
├── scripts/                     # Automation scripts
│   ├── fetch_nasa_data.py      # Data collection pipeline
│   ├── process_dataset.py      # Data processing
│   └── verify_setup.py         # Setup validation
│
├── kaggle/                      # Kaggle dataset docs
│   ├── KAGGLE_README.md        # Dataset description
│   └── data-dictionary.md      # Column specifications
│
└── app/                         # Gradio web app (coming soon)
    └── dont_look_up.py         # Main application
```

---

## 🎓 When to ACTUALLY Panic

We use the **Torino Scale** (NASA's official "how scared should I be?" scale):

| Level | Color | What It Means | Your Reaction |
|-------|-------|---------------|---------------|
| 0 | ⚪ White | Zero chance of impact | Touch grass |
| 1 | 🟢 Green | Normal | Keep scrolling |
| 2-4 | 🟡 Yellow | Worth monitoring | Interesting tweet material |
| 5-7 | 🟠 Orange | Threatening | Cancel plans, maybe |
| 8-10 | 🔴 Red | Certain collision | It's been real, folks |

**Current Status:** Level 0 (We're vibing)

---

## 📈 Custom Risk Metrics

Our dataset includes custom-calculated metrics for easier analysis:

### Risk Score (0-1 scale)
```
risk_score = (distance_factor × 0.4) + (velocity_factor × 0.3) + (time_factor × 0.3)
```

### Panic Level (0-10 integer)
Scaled version of risk score for human-friendly interpretation.

### Threat Categories
- 🟢 **SAFE** - "You're fine. Go touch grass."
- 🟡 **MONITOR** - "Worth a tweet, not worth a bunker."
- 🟠 **CONCERN** - "Time to learn survival skills?"
- 🔴 **OH_NO** - "Did you backup your data?"

### Panic Verdicts
Algorithmically-generated comedic commentary on each asteroid's threat level.

---

## 🤖 Machine Learning Models (Coming Soon)

We're training 3 models to predict asteroid threats:

1. **Panic Level Classifier** (Random Forest)
   - Classifies asteroids: SAFE → MONITOR → CONCERN → OH_NO
   - Target accuracy: >90%

2. **Impact Probability Regressor** (XGBoost)
   - Predicts actual impact probability (0-1)
   - For Sentry-listed asteroids

3. **Should I Worry Today?™** (Custom Algorithm)
   - Combines multiple factors with comedic output
   - Accuracy: Vibes-based

---

## 📸 Screenshots

### Dataset Preview
Check out the [Kaggle dataset page](https://www.kaggle.com/datasets/hasandafa1201/nasa-asteroid-impact-dataset) for interactive data exploration!

### Notebooks
[Coming soon - because we're still building this masterpiece]

---

## 🎯 Roadmap

**Phase 1: Data Pipeline** ✅
- [x] Fetch data from NASA APIs
- [x] Clean and merge datasets
- [x] Create custom risk scoring
- [x] Upload to Kaggle
- [x] Write documentation

**Phase 2: Analysis & ML** 🚧
- [ ] Advanced statistical analysis
- [ ] Feature engineering
- [ ] Train ML models
- [ ] Model evaluation & comparison

**Phase 3: Visualization** 🚧
- [ ] Interactive Plotly dashboards
- [ ] 3D solar system visualization
- [ ] Temporal heatmaps
- [ ] Risk distribution charts

**Phase 4: Application** 📅
- [ ] Build Gradio web app (5 tabs)
- [ ] Deploy to Hugging Face Spaces
- [ ] Add real-time data updates
- [ ] Mobile-responsive design

**Phase 5: Content** 📝
- [ ] Write Substack blog series
- [ ] Create demo videos
- [ ] Social media content
- [ ] Community engagement

---

## 🤝 Contributing

Found a bug? Want to add more doom-related features? PRs are welcome!

Just remember:
- Keep the humor respectful
- Data accuracy is non-negotiable
- Code quality > clever one-liners
- Test your changes (we have enough uncertainty with asteroids)

---

## 📚 Resources & References

### Data Sources
- [NASA CNEOS](https://cneos.jpl.nasa.gov/) - Center for Near-Earth Object Studies
- [Sentry Risk Table](https://cneos.jpl.nasa.gov/sentry/) - Official impact risk list
- [NeoWs API Docs](https://api.nasa.gov/) - NASA's asteroid database
- [Close Approach Data API](https://ssd-api.jpl.nasa.gov/doc/cad.html) - Historical approaches

### Dataset
- [Kaggle Dataset](https://www.kaggle.com/datasets/hasandafa1201/nasa-asteroid-impact-dataset) - Download processed data here

### Inspiration
- [Don't Look Up (2021)](https://www.netflix.com/title/81252357) - Required viewing

---

## 🙏 Acknowledgments

- **NASA JPL** - For tracking space rocks so we don't have to
- **Kaggle Community** - For hosting our apocalypse data
- **Coffee** - For keeping me awake during late-night coding
- **Anxiety** - For motivating this entire project
- **Adam McKay** - For the film that inspired this chaos

---

## 📄 License

MIT License - Feel free to use this code. If an asteroid wipes us out, all bets are off.

---

## 📧 Contact

**Abdullah Hasan Dafa**
- GitHub: [@hasandafa](https://github.com/hasandafa)
- Kaggle: [@hasandafa1201](https://www.kaggle.com/hasandafa1201)
- Project Repo: [github.com/hasandafa/do-not-look-up](https://github.com/hasandafa/do-not-look-up)
- Dataset: [Kaggle Dataset](https://www.kaggle.com/datasets/hasandafa1201/nasa-asteroid-impact-dataset)

---

<div align="center">

### Current Threat Level: **CHILL** ✅

*Next Close Approach: Apophis on April 13, 2029*

**Remember: Looking up is optional. The data isn't.**

---

Made with 💀 and Python | Data by NASA | Available on Kaggle

**[⬇️ Download Dataset](https://www.kaggle.com/datasets/hasandafa1201/nasa-asteroid-impact-dataset) | [📓 Explore Notebooks](./notebooks/) | [⭐ Star This Repo](https://github.com/hasandafa/do-not-look-up)**

</div>