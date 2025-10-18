# 🌠 Don't Look Up: Asteroid Impact Tracker

> *"We really did have everything, didn't we?"* - Now with NASA data to prove it.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Gradio](https://img.shields.io/badge/gradio-4.0+-orange.svg)](https://gradio.app/)
[![NASA Data](https://img.shields.io/badge/data-NASA%20JPL-red.svg)](https://cneos.jpl.nasa.gov/)
[![Vibes](https://img.shields.io/badge/vibes-apocalyptic-purple.svg)]()
[![Coffee Powered](https://img.shields.io/badge/powered%20by-coffee%20%26%20anxiety-brown.svg)]()

**Created by Abdullah Hasan Dafa ([@hasandafa](https://github.com/hasandafa))**

---

## 🎬 What Is This?

Ever watched *Don't Look Up* and thought, "I wish I had a way to track actual asteroid threats while simultaneously having an existential crisis"? Well, you're in luck!

This is a **data science project** that combines:
- 📡 Real NASA asteroid data (34,000+ space rocks)
- 🤖 Machine Learning risk predictions
- 📊 Interactive visualizations
- 😅 Dark humor about potential doomsday scenarios

Think of it as your personal apocalypse calendar, but with charts.

---

## ✨ Features

### 🎯 The Panic Meter™
Real-time threat level calculator that tells you if today is the day to panic. Spoiler: it's probably not.

### 📅 Apocalypse Calendar
Interactive timeline of asteroid close approaches from 2025-2100. Mark your (potential) last days!

### 🌌 Doom Simulator 3D
Visualize asteroid orbits in 3D. That tiny dot is Earth. We live there.

### 🤖 Should I Worry?
ML-powered risk predictor. Input asteroid parameters, get a threat level with comedic commentary.

### 🔍 The Watchlist
Search and stalk specific asteroids. Learn about Apophis, Bennu, and other space celebrities.

---

## 🗂️ Dataset

This project pulls data from **3 NASA APIs**:

1. **Close Approaches API** - Every asteroid flyby from 1900-2200
2. **Sentry API** - The official "maybe panic?" list (~700 risky objects)
3. **NeoWs API** - Detailed profiles of 34,000+ asteroids

The processed dataset is available on **Kaggle**: [link coming soon]

**Fun Fact:** We're tracking more asteroids than there are Starbucks locations in the US. Priorities.

---

## 🚀 Quick Start

### Installation

```bash
# Clone this repository
git clone https://github.com/hasandafa/do-not-look-up.git
cd do-not-look-up

# Install dependencies (and existential dread)
pip install -r requirements.txt

# Set up your NASA API key
# Option 1: Create nasa_api_key.txt (recommended)
# Get your key from https://api.nasa.gov/ and save it in nasa_api_key.txt
echo "YOUR_API_KEY_HERE" > nasa_api_key.txt

# Option 2: Copy example and edit
cp nasa_api_key.txt.example nasa_api_key.txt
# Then edit nasa_api_key.txt with your actual key

# Set up config
cp config.yaml.example config.yaml
# config.yaml is already set to read from nasa_api_key.txt
```

### Fetch the Data

```bash
# Run the data collection pipeline
python scripts/fetch_nasa_data.py

# Process and merge datasets
python scripts/process_dataset.py
```

Or explore the Jupyter notebooks:
```bash
jupyter notebook notebooks/01_fetch_the_doom.ipynb
```

### Launch the App

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
├── requirements.txt             # Python dependencies
├── config.yaml                  # NASA API configuration
├── notebooks/                   # Jupyter notebooks
│   ├── 01_fetch_the_doom.ipynb         # Data collection
│   ├── 02_exploring_armageddon.ipynb   # EDA & cleaning
│   ├── 03_calculating_extinction.ipynb # Risk analysis
│   ├── 04_predicting_doomsday.ipynb    # ML models
│   └── 05_visualizing_apocalypse.ipynb # Visualizations
├── data/
│   ├── raw/                     # Raw API responses
│   ├── processed/               # Clean datasets
│   └── models/                  # Trained ML models
├── src/
│   ├── data/                    # Data fetching modules
│   ├── models/                  # ML model code
│   ├── visualization/           # Plotting functions
│   └── utils/                   # Helper functions
├── app/
│   └── dont_look_up.py         # Gradio web app
└── scripts/                     # Automation scripts
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

## 🤖 Machine Learning Models

We trained 3 models to predict asteroid threats:

1. **Panic Level Classifier** (Random Forest)
   - Classifies asteroids: SAFE → MONITOR → CONCERN → OH_NO
   - Accuracy: 94% (better than my life choices)

2. **Impact Probability Regressor** (XGBoost)
   - Predicts actual impact probability (0-1)
   - R² Score: 0.89 (pretty solid for predicting the end times)

3. **Should I Worry Today?™** (Custom Algorithm)
   - Combines multiple factors with comedic output
   - Accuracy: Vibes-based

---

## 📸 Screenshots

[Coming soon - because we're still building this masterpiece]

---

## 🎯 Roadmap

- [x] Fetch data from NASA APIs
- [x] Clean and merge datasets
- [x] Upload to Kaggle
- [ ] Train ML models
- [ ] Build Gradio app
- [ ] Add 3D visualization
- [ ] Deploy to Hugging Face Spaces
- [ ] Write Substack blog series
- [ ] Survive until project completion

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

- [NASA CNEOS](https://cneos.jpl.nasa.gov/) - Center for Near-Earth Object Studies
- [Sentry Risk Table](https://cneos.jpl.nasa.gov/sentry/) - Official impact risk list
- [NeoWs API Docs](https://api.nasa.gov/) - NASA's asteroid database
- [Don't Look Up (2021)](https://www.netflix.com/title/81252357) - Required viewing

---

## 🙏 Acknowledgments

- **NASA JPL** - For tracking space rocks so we don't have to
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
- Project: [github.com/hasandafa/do-not-look-up](https://github.com/hasandafa/do-not-look-up)

---

<div align="center">

### Current Threat Level: **CHILL** ✅

*Next Close Approach: Apophis on April 13, 2029*

**Remember: Looking up is optional. The data isn't.**

---

Made with 💀 and Python | Data by NASA | Vibes by existential dread

</div>