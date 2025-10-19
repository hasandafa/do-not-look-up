# 🚀 Quick Start Guide

**Don't Look Up: Asteroid Impact Tracker**  
*Created by Abdullah Hasan Dafa (@hasandafa)*

---

## ⚡ 5-Minute Setup

### Step 1: Get NASA API Key (30 seconds)

1. Go to: **https://api.nasa.gov/**
2. Fill in your name and email
3. Click "Signup"
4. Check your email for the API key
5. Copy your API key

**Example key**: `abcdef123456789YOURKEY`

---

### Step 2: Save Your API Key (15 seconds)

Create a file named `nasa_api_key.txt` in project root:

```bash
# Create the file
touch nasa_api_key.txt

# Or copy from example
cp nasa_api_key.txt.example nasa_api_key.txt
```

Open `nasa_api_key.txt` and paste your API key:

```
abcdef123456789YOURKEY
```

**Important**: 
- ✅ Just the key, nothing else
- ✅ No quotes
- ✅ No spaces before/after
- ❌ Don't commit this file to git (.gitignore handles it)

---

### Step 3: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

Wait for packages to install... ☕

---

### Step 4: Setup Config (15 seconds)

```bash
cp config.yaml.example config.yaml
```

That's it! `config.yaml` is already set to read from `nasa_api_key.txt`

---

### Step 5: Run! (3-5 minutes)

#### Option A: Using Scripts

```bash
# Fetch data from NASA APIs
python scripts/fetch_nasa_data.py

# Process and create final dataset
python scripts/process_dataset.py
```

#### Option B: Using Jupyter Notebooks

```bash
# Launch Jupyter
jupyter notebook

# Then open:
# - notebooks/01_fetch_the_doom.ipynb
# - notebooks/02_exploring_armageddon.ipynb
```

---

## ✅ Success Checklist

After running, you should have:

```
do-not-look-up/
├── nasa_api_key.txt ✅ (your secret key)
├── config.yaml ✅ (your config)
│
├── data/
│   ├── raw/ ✅
│   │   ├── close_approaches_raw.json
│   │   ├── sentry_objects_raw.json
│   │   └── neows_data_raw.json
│   │
│   └── processed/ ✅
│       ├── asteroid_dataset_YYYYMMDD.csv
│       ├── asteroid_dataset_YYYYMMDD.parquet
│       └── dataset_summary_YYYYMMDD.json
```

---

## 🎯 Quick Test

Run this to verify everything works:

```python
import pandas as pd

# Load the dataset
df = pd.read_csv('data/processed/asteroid_dataset_*.csv')

print(f"✅ Dataset loaded: {len(df):,} asteroids")
print(f"📅 Date range: {df['close_approach_date'].min()} to {df['close_approach_date'].max()}")
print(f"\n🎯 Threat distribution:")
print(df['threat_category'].value_counts())
```

Expected output:
```
✅ Dataset loaded: 10,000+ asteroids
📅 Date range: 2020-01-01 to 2100-12-31

🎯 Threat distribution:
SAFE        8500
MONITOR     1200
CONCERN      250
OH_NO         50
```

---

## 🐛 Troubleshooting

### Error: "nasa_api_key.txt not found"

**Solution**:
```bash
# Create the file
echo "YOUR_API_KEY_HERE" > nasa_api_key.txt

# Or copy example
cp nasa_api_key.txt.example nasa_api_key.txt
# Then edit with your actual key
```

---

### Error: "API key is empty"

**Solution**: Make sure `nasa_api_key.txt` contains ONLY your API key:

```
# ✅ CORRECT
abcdef123456789YOURKEY

# ❌ WRONG
"abcdef123456789YOURKEY"
api_key = abcdef123456789YOURKEY
NASA_API_KEY=abcdef123456789YOURKEY
```

---

### Error: "Invalid API key"

**Solution**:
1. Double-check your key from https://api.nasa.gov/
2. Make sure there are no extra spaces in nasa_api_key.txt
3. Try getting a new API key (they're free!)

---

### Error: "Rate limit exceeded"

**Solution**: NASA limits requests. Wait 1 hour or adjust in `config.yaml`:

```yaml
nasa_api:
  rate_limit:
    delay_between_requests: 1.0  # Increase from 0.5 to 1.0
```

---

### Error: "Module not found"

**Solution**: Install dependencies again:
```bash
pip install -r requirements.txt
```

---

## 📊 Next Steps

### 1. Explore Your Data

```python
import pandas as pd
import plotly.express as px

df = pd.read_csv('data/processed/asteroid_dataset_*.csv')

# Timeline of approaches
fig = px.scatter(df, x='close_approach_date', y='distance_au', 
                 color='threat_category', size='velocity_km_s',
                 title='Asteroid Approaches Over Time')
fig.show()
```

### 2. Upload to Kaggle

1. Go to [kaggle.com/datasets/new](https://www.kaggle.com/datasets/new)
2. Upload your CSV file
3. Use `kaggle/KAGGLE_README.md` as description
4. Add tags: astronomy, nasa, asteroids, space, machine-learning
5. Publish!

### 3. Build Something Cool

Ideas:
- 🤖 Train ML model to predict threat levels
- 📊 Create interactive dashboard
- 📈 Time series analysis
- 🌌 3D orbital visualization
- 🔔 Build alert system for upcoming approaches

---

## 🎓 Learning Resources

### Understanding the Data

- **NASA CNEOS**: https://cneos.jpl.nasa.gov/
- **Asteroid Basics**: https://solarsystem.nasa.gov/asteroids-comets-and-meteors/
- **Orbital Mechanics**: https://en.wikipedia.org/wiki/Orbital_elements

### Data Science Tutorials

- **Pandas Guide**: https://pandas.pydata.org/docs/
- **Plotly Docs**: https://plotly.com/python/
- **ML with Scikit-learn**: https://scikit-learn.org/stable/tutorial/

---

## 💡 Pro Tips

### Tip 1: Faster Data Loading
```python
# Use parquet instead of CSV (much faster!)
df = pd.read_parquet('data/processed/asteroid_dataset_*.parquet')
```

### Tip 2: Filter by Date
```python
# Get only future approaches
future = df[df['is_future_event'] == True]

# Get approaches in next 10 years
next_decade = df[df['days_until_approach'].between(0, 3650)]
```

### Tip 3: Find Interesting Asteroids
```python
# Top 10 closest approaches
closest = df.nsmallest(10, 'distance_au')

# High-risk asteroids
high_risk = df[df['threat_category'].isin(['CONCERN', 'OH_NO'])]

# Next approach
next_up = df[df['is_future_event']].nsmallest(1, 'days_until_approach')
```

### Tip 4: Update Data Periodically
```python
# NASA discovers new asteroids regularly
# Re-run scripts monthly to get latest data
python scripts/fetch_nasa_data.py
python scripts/process_dataset.py
```

---

## 🤝 Contributing

Want to improve this project?

1. Fork the repo
2. Create a branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Submit a Pull Request

Ideas for contributions:
- Add more NASA APIs (Sentry impact probabilities)
- Improve risk scoring algorithm
- Add more visualizations
- Write better documentation
- Fix bugs

---

## 📞 Need Help?

### Check These First:
1. **README.md** - Main documentation
2. **FASE_1_COMPLETE.md** - Detailed guide
3. **kaggle/data-dictionary.md** - Column explanations

### Still Stuck?
- **GitHub Issues**: [github.com/hasandafa/do-not-look-up/issues](https://github.com/hasandafa/do-not-look-up/issues)
- **Kaggle Comments**: Comment on the dataset
- **Email**: (if you added it to config.yaml)

---

## 🎯 Quick Reference

### File Structure
```
nasa_api_key.txt      → Your API key (DON'T commit!)
config.yaml           → Configuration file
requirements.txt      → Python dependencies
scripts/              → Data fetching & processing
notebooks/            → Jupyter notebooks for exploration
data/raw/            → Raw NASA data (auto-generated)
data/processed/      → Final dataset (auto-generated)
```

### Important Commands
```bash
# Setup
pip install -r requirements.txt
cp config.yaml.example config.yaml
echo "YOUR_KEY" > nasa_api_key.txt

# Run
python scripts/fetch_nasa_data.py
python scripts/process_dataset.py

# Explore
jupyter notebook notebooks/01_fetch_the_doom.ipynb
```

### Key Files After Running
```
data/processed/asteroid_dataset_YYYYMMDD.csv  → Main dataset
data/processed/asteroid_dataset_YYYYMMDD.parquet  → Faster format
data/processed/dataset_summary_YYYYMMDD.json  → Metadata
```

---

## ✅ Checklist: Am I Ready?

Before uploading to Kaggle, verify:

- [x] Dataset generated successfully (CSV file exists)
- [x] No errors in console output
- [x] File size reasonable (~2-5 MB)
- [x] Opened CSV and spot-checked data
- [x] Read KAGGLE_README.md
- [x] Understand what the columns mean
- [x] Have Kaggle account ready
- [x] Excited to share! 🎉

---

## 🌟 What Makes This Special?

### Real NASA Data ✅
Not simulated, not made up. Straight from JPL.

### Custom Risk Scoring ✅
Unique panic level calculations with humor.

### ML-Ready ✅
Features calculated, labels assigned, ready to train.

### Well-Documented ✅
Every column explained, examples provided.

### Fun & Educational ✅
Learn about asteroids without falling asleep.

---

## 🎬 Final Notes

### Should You Panic?
**No.** Even "OH_NO" asteroids are safe. NASA's watching.

### Should You Learn?
**Yes!** This is real science made accessible.

### Should You Share?
**Absolutely!** Upload to Kaggle, share on social media, teach others.

---

<div align="center">

## 🚀 Ready to Launch!

Your dataset is prepared.  
Your knowledge is expanded.  
The cosmos awaits your analysis.

**Go forth and track some asteroids!** 🌠

---

*Remember: Looking up is optional. The data isn't.*

Made with 💀, ☕, and Python  
Created by Abdullah Hasan Dafa (@hasandafa)

</div>