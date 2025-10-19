"""
============================================================================
🌠 DON'T LOOK UP: ASTEROID IMPACT TRACKER
Main Gradio Application
============================================================================
Author: Abdullah Hasan Dafa (@hasandafa)
GitHub: https://github.com/hasandafa/do-not-look-up
Dataset: https://www.kaggle.com/datasets/hasandafa1201/nasa-asteroid-impact-dataset

"Looking up is optional. The data isn't." ☄️
============================================================================
"""

import gradio as gr
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import joblib
from datetime import datetime, timedelta
import json

# ============================================================================
# CONFIGURATION & DATA LOADING
# ============================================================================

# Determine correct path based on where script is run from
import os
import sys

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# If running from app/ folder, go up one level
if os.path.basename(script_dir) == 'app':
    base_path = os.path.dirname(script_dir)
else:
    base_path = script_dir

# Construct paths
data_path = os.path.join(base_path, 'data', 'processed', 'asteroid_dataset_engineered.csv')
models_path = os.path.join(base_path, 'data', 'models')
viz_path = os.path.join(base_path, 'data', 'visualizations')

print(f"🔍 Loading data from: {data_path}")
print(f"🔍 Models path: {models_path}")
print(f"🔍 Visualizations path: {viz_path}")

# Load data
try:
    df = pd.read_csv(data_path)
    df['close_approach_date'] = pd.to_datetime(df['close_approach_date'])
    print(f"✅ Loaded {len(df):,} asteroid records")
except FileNotFoundError:
    print("❌ ERROR: Dataset not found!")
    print(f"   Looking for: {data_path}")
    print(f"   Please run notebooks 01-03 first to generate the dataset.")
    sys.exit(1)

# Load ML models
try:
    panic_model = joblib.load(os.path.join(models_path, 'panic_classifier.pkl'))
    panic_scaler = joblib.load(os.path.join(models_path, 'panic_scaler.pkl'))
    panic_features = joblib.load(os.path.join(models_path, 'panic_features.pkl'))
    
    impact_model = joblib.load(os.path.join(models_path, 'impact_regressor.pkl'))
    impact_scaler = joblib.load(os.path.join(models_path, 'impact_scaler.pkl'))
    impact_features = joblib.load(os.path.join(models_path, 'impact_features.pkl'))
    
    # Don't load worry_calculator from pickle (causes issues)
    # We'll define it in this file instead
    worry_calculator = None
    
    print("✅ ML models loaded successfully")
except Exception as e:
    print(f"⚠️  Warning: Could not load models - {e}")
    print(f"   Some features may not work. Please run notebook 04 to train models.")
    panic_model = None

# Color schemes
THREAT_COLORS = {
    'SAFE': '#4ade80',
    'MONITOR': '#fbbf24',
    'CONCERN': '#fb923c',
    'OH_NO': '#ef4444'
}

# ============================================================================
# TAB 1: THE PANIC METER™
# ============================================================================

def calculate_panic(asteroid_name):
    """Calculate panic level for selected asteroid"""
    try:
        # Find asteroid
        asteroid_data = df[df['asteroid_designation'] == asteroid_name]
        
        if len(asteroid_data) == 0:
            return None, "Asteroid not found!", None
        
        data = asteroid_data.iloc[0]
        
        # Get panic verdict - handle if column doesn't exist
        if 'panic_verdict' in data and pd.notna(data['panic_verdict']):
            verdict_text = data['panic_verdict']
        else:
            # Generate verdict based on panic level
            panic = data['panic_level']
            if panic <= 2:
                verdict_text = "You're fine. Go touch grass."
            elif panic <= 4:
                verdict_text = "Worth a tweet, not worth a bunker."
            elif panic <= 6:
                verdict_text = "Time to learn survival skills?"
            else:
                verdict_text = "Did you backup your data?"
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=data['panic_level'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Panic Level", 'font': {'size': 24}},
            number={'font': {'size': 48}},
            gauge={
                'axis': {'range': [0, 10], 'tickwidth': 2, 'tickcolor': "white"},
                'bar': {'color': "darkred", 'thickness': 0.75},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "white",
                'steps': [
                    {'range': [0, 3], 'color': THREAT_COLORS['SAFE']},
                    {'range': [3, 6], 'color': THREAT_COLORS['MONITOR']},
                    {'range': [6, 8], 'color': THREAT_COLORS['CONCERN']},
                    {'range': [8, 10], 'color': THREAT_COLORS['OH_NO']}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': data['panic_level']
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': "white", 'family': "Arial"},
            height=400
        )
        
        # Verdict text
        sentry_text = ""
        if data['on_sentry_list'] and 'sentry_impact_prob' in data and pd.notna(data['sentry_impact_prob']):
            sentry_text = f"\n\n⚠️ **ON NASA SENTRY LIST** - Impact probability: {data['sentry_impact_prob']:.2e}"
        
        verdict = f"""
## {data['threat_category']} 🎯

**Panic Level:** {data['panic_level']}/10

**{verdict_text}**

---

### Details:
- **Distance:** {data['distance_au']:.6f} AU ({data['distance_au'] * 149597870.7:.0f} km)
- **Velocity:** {data['velocity_km_s']:.2f} km/s
- **Approach Date:** {data['close_approach_date']}
- **Risk Score:** {data['risk_score']:.4f}
- **Orbit Type:** {data.get('orbit_type', 'Unknown')}
{sentry_text}
        """
        
        # Stats DataFrame
        stats_df = pd.DataFrame({
            'Metric': [
                'Distance (AU)',
                'Distance (km)', 
                'Velocity (km/s)',
                'Approach Date',
                'Days from today',
                'Risk Score',
                'Absolute Magnitude',
                'Orbit Type',
                'Sentry Listed'
            ],
            'Value': [
                f"{data['distance_au']:.6f}",
                f"{data['distance_au'] * 149597870.7:,.0f}",
                f"{data['velocity_km_s']:.2f}",
                str(data['close_approach_date'])[:10],
                f"{data.get('days_from_today', 'N/A')}",
                f"{data['risk_score']:.4f}",
                f"{data.get('absolute_magnitude', 'N/A')}",
                data.get('orbit_type', 'Unknown'),
                '✅ Yes' if data['on_sentry_list'] else '❌ No'
            ]
        })
        
        return fig, verdict, stats_df
        
    except Exception as e:
        return None, f"Error: {str(e)}", None

# ============================================================================
# TAB 2: APOCALYPSE CALENDAR
# ============================================================================

def generate_calendar(year, threat_levels):
    """Generate calendar heatmap for selected year"""
    try:
        # Filter data
        year_data = df[
            (df['year'] == year) & 
            (df['threat_category'].isin(threat_levels))
        ].copy()
        
        if len(year_data) == 0:
            # Empty heatmap
            fig = go.Figure()
            fig.add_annotation(
                text=f"No asteroids in {year} matching selected threat levels",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color="white")
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=600
            )
            return fig, pd.DataFrame()
        
        # Aggregate by month
        monthly_data = year_data.groupby('month').agg({
            'asteroid_designation': 'count',
            'risk_score': 'max',
            'panic_level': 'max'
        }).reset_index()
        monthly_data.columns = ['month', 'count', 'max_risk', 'max_panic']
        
        # Create heatmap data
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        z_data = []
        hover_data = []
        
        for month in range(1, 13):
            month_info = monthly_data[monthly_data['month'] == month]
            if len(month_info) > 0:
                z_data.append(month_info.iloc[0]['max_risk'])
                hover_data.append(
                    f"Month: {month_names[month-1]}<br>" +
                    f"Approaches: {month_info.iloc[0]['count']}<br>" +
                    f"Max Risk: {month_info.iloc[0]['max_risk']:.4f}<br>" +
                    f"Max Panic: {month_info.iloc[0]['max_panic']}/10"
                )
            else:
                z_data.append(0)
                hover_data.append(f"Month: {month_names[month-1]}<br>No approaches")
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=[z_data],
            x=month_names,
            y=[year],
            colorscale='YlOrRd',
            text=[hover_data],
            hovertemplate='%{text}<extra></extra>',
            colorbar=dict(title="Max Risk<br>Score")
        ))
        
        fig.update_layout(
            title=f"📅 Asteroid Approaches in {year}",
            xaxis_title="Month",
            yaxis_title="Year",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400
        )
        
        # Event list
        events_df = year_data.sort_values('risk_score', ascending=False).head(20)[[
            'asteroid_designation', 'close_approach_date', 'distance_au',
            'velocity_km_s', 'panic_level', 'threat_category'
        ]].copy()
        
        events_df['close_approach_date'] = events_df['close_approach_date'].dt.strftime('%Y-%m-%d')
        events_df.columns = ['Asteroid', 'Date', 'Distance (AU)', 
                             'Velocity (km/s)', 'Panic', 'Category']
        
        return fig, events_df
        
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=f"Error: {str(e)}", x=0.5, y=0.5, showarrow=False)
        return fig, pd.DataFrame()

# ============================================================================
# TAB 3: DOOM SIMULATOR 3D
# ============================================================================

def load_3d_viz():
    """Load pre-generated 3D visualization"""
    try:
        viz_file = os.path.join(viz_path, '3d_solar_system.html')
        
        # Check if file exists
        if not os.path.exists(viz_file):
            return f"""
            <div style='color:white; padding:20px; text-align:center;'>
                <h3>⚠️ 3D visualization not found</h3>
                <p>File should be at: {viz_file}</p>
                <p>Please run Notebook 05 Part 3 to generate it.</p>
            </div>
            """
        
        # Read file
        with open(viz_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check if content is valid
        if len(html_content) < 100:
            return f"""
            <div style='color:white; padding:20px; text-align:center;'>
                <h3>⚠️ 3D visualization file is empty or corrupted</h3>
                <p>File size: {len(html_content)} bytes</p>
                <p>Please re-run Notebook 05 Part 3.</p>
            </div>
            """
        
        print(f"✅ Loaded 3D viz: {len(html_content)} bytes")
        return html_content
        
    except Exception as e:
        return f"""
        <div style='color:white; padding:20px; text-align:center;'>
            <h3>❌ Error loading 3D visualization</h3>
            <p><strong>Error:</strong> {str(e)}</p>
            <p><strong>File path:</strong> {viz_file if 'viz_file' in locals() else 'N/A'}</p>
            <p>Please check the file and try again.</p>
        </div>
        """

# ============================================================================
# TAB 4: SHOULD I WORRY?
# ============================================================================

def should_i_worry_today(df, today=None, horizon_days=30):
    """
    Calculate worry score based on upcoming asteroid approaches.
    Re-implemented here to avoid pickle issues.
    """
    if today is None:
        today = pd.Timestamp.now()
    
    # Convert date column
    df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df['close_approach_date']):
        df['close_approach_date'] = pd.to_datetime(df['close_approach_date'])
    
    # Filter upcoming approaches
    end_date = today + pd.Timedelta(days=horizon_days)
    upcoming = df[(df['close_approach_date'] >= today) & 
                  (df['close_approach_date'] <= end_date)]
    
    if len(upcoming) == 0:
        return {
            'worry_score': 0,
            'verdict': "Nah, you're good",
            'reason': f"No asteroids approaching in the next {horizon_days} days",
            'recommendation': "Go touch grass 🌱",
            'next_event': None,
            'statistics': {
                'total_upcoming': 0,
                'sentry_threats': 0,
                'max_panic_level': 0,
                'avg_risk_score': 0,
                'closest_distance_au': 0,
                'concern_level_count': 0,
                'oh_no_level_count': 0
            }
        }
    
    # Calculate aggregate metrics
    max_panic = upcoming['panic_level'].max()
    avg_risk = upcoming['risk_score'].mean()
    sentry_count = upcoming['on_sentry_list'].sum()
    closest_distance = upcoming['distance_au'].min()
    
    # Count by threat category
    threat_counts = upcoming['threat_category'].value_counts()
    concern_count = threat_counts.get('CONCERN', 0)
    oh_no_count = threat_counts.get('OH_NO', 0)
    
    # Weighted worry score calculation
    worry_score = (
        (max_panic / 10) * 0.35 +
        avg_risk * 0.25 +
        (sentry_count / max(len(upcoming), 1)) * 0.20 +
        (1 - min(closest_distance, 1)) * 0.15 +
        (concern_count + oh_no_count * 2) / max(len(upcoming), 1) * 0.05
    ) * 100
    
    worry_score = min(worry_score, 100)
    
    # Determine verdict
    if worry_score < 10:
        verdict = "Nah, you're good"
        recommendation = "Go touch grass 🌱"
    elif worry_score < 25:
        verdict = "Maybe check Twitter"
        recommendation = "Worth a casual glance at the news"
    elif worry_score < 45:
        verdict = "Worth mentioning at dinner"
        recommendation = "Interesting conversation starter material"
    elif worry_score < 65:
        verdict = "Time to pay attention"
        recommendation = "Maybe bookmark some NASA pages"
    elif worry_score < 80:
        verdict = "Call your mom"
        recommendation = "Check in with loved ones, just in case"
    else:
        verdict = "Did you backup your data?"
        recommendation = "Seriously, backup everything. NOW."
    
    # Find next closest approach
    next_approach = upcoming.nsmallest(1, 'distance_au').iloc[0]
    
    return {
        'worry_score': int(worry_score),
        'verdict': verdict,
        'reason': f"Based on {len(upcoming)} approaching asteroids in next {horizon_days} days",
        'recommendation': recommendation,
        'next_event': {
            'asteroid': next_approach['asteroid_designation'],
            'date': str(next_approach['close_approach_date']),
            'distance_au': float(next_approach['distance_au']),
            'velocity_km_s': float(next_approach['velocity_km_s']),
            'panic_level': int(next_approach['panic_level']),
            'threat_category': next_approach['threat_category']
        },
        'statistics': {
            'total_upcoming': int(len(upcoming)),
            'sentry_threats': int(sentry_count),
            'max_panic_level': int(max_panic),
            'avg_risk_score': float(avg_risk),
            'closest_distance_au': float(closest_distance),
            'concern_level_count': int(concern_count),
            'oh_no_level_count': int(oh_no_count)
        }
    }

def check_worry(days_ahead, location):
    """Calculate worry score using ML model"""
    try:
        # Use the function defined in this file (not pickle)
        result = should_i_worry_today(df, today=datetime.now(), horizon_days=int(days_ahead))
        
        # Create gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=result['worry_score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Worry Score", 'font': {'size': 24}},
            number={'font': {'size': 48}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 2},
                'bar': {'color': "darkred"},
                'steps': [
                    {'range': [0, 25], 'color': THREAT_COLORS['SAFE']},
                    {'range': [25, 50], 'color': THREAT_COLORS['MONITOR']},
                    {'range': [50, 75], 'color': THREAT_COLORS['CONCERN']},
                    {'range': [75, 100], 'color': THREAT_COLORS['OH_NO']}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': result['worry_score']
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': "white"},
            height=400
        )
        
        # Verdict text with safe access
        next_event_info = ""
        if result.get('next_event'):
            ne = result['next_event']
            next_event_info = f"""
### 🎯 Next Close Approach:
- **Asteroid:** {ne.get('asteroid', 'Unknown')}
- **Date:** {ne.get('date', 'Unknown')[:10]}
- **Distance:** {ne.get('distance_au', 0):.6f} AU
- **Velocity:** {ne.get('velocity_km_s', 0):.2f} km/s
- **Panic Level:** {ne.get('panic_level', 0)}/10
- **Category:** {ne.get('threat_category', 'Unknown')}
"""
        
        verdict = f"""
## {result['verdict']} 🤖

**Worry Score:** {result['worry_score']}/100

**Recommendation:** {result['recommendation']}

---

### Analysis Summary:
- **Time Horizon:** Next {days_ahead} days
- **Total Approaching:** {result['statistics']['total_upcoming']} asteroids
- **Sentry Threats:** {result['statistics']['sentry_threats']}
- **Max Panic Level:** {result['statistics']['max_panic_level']}/10
- **Avg Risk Score:** {result['statistics']['avg_risk_score']:.4f}
- **Closest Distance:** {result['statistics']['closest_distance_au']:.6f} AU

{f"### ⚠️ High Concern Events: {result['statistics']['concern_level_count'] + result['statistics']['oh_no_level_count']}" if result['statistics']['concern_level_count'] + result['statistics']['oh_no_level_count'] > 0 else ""}

{next_event_info}
        """
        
        # Next event table
        if result.get('next_event'):
            next_df = pd.DataFrame({
                'Metric': ['Asteroid', 'Date', 'Distance (AU)', 'Velocity (km/s)', 'Panic Level', 'Category'],
                'Value': [
                    result['next_event']['asteroid'],
                    result['next_event']['date'][:10],
                    f"{result['next_event']['distance_au']:.6f}",
                    f"{result['next_event']['velocity_km_s']:.2f}",
                    f"{result['next_event']['panic_level']}/10",
                    result['next_event']['threat_category']
                ]
            })
        else:
            next_df = pd.DataFrame({'Message': ['No upcoming threats']})
        
        return fig, verdict, next_df
        
    except Exception as e:
        import traceback
        error_msg = f"Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        return None, error_msg, pd.DataFrame()

# ============================================================================
# TAB 5: THE WATCHLIST
# ============================================================================

def search_asteroids(query, min_risk, max_risk, threat_levels, limit):
    """Search and filter asteroids"""
    try:
        # Start with all data
        filtered = df.copy()
        
        # Apply filters
        if query and query.strip():
            filtered = filtered[
                filtered['asteroid_designation'].str.contains(query.strip(), case=False, na=False)
            ]
        
        filtered = filtered[
            (filtered['risk_score'] >= float(min_risk)) &
            (filtered['risk_score'] <= float(max_risk)) &
            (filtered['threat_category'].isin(threat_levels))
        ]
        
        # Sort by risk
        filtered = filtered.sort_values('risk_score', ascending=False)
        
        # Limit results
        filtered = filtered.head(int(limit))
        
        # Select columns
        result_df = filtered[[
            'asteroid_designation', 'close_approach_date', 'distance_au',
            'velocity_km_s', 'risk_score', 'panic_level', 'threat_category',
            'orbit_type', 'on_sentry_list'
        ]].copy()
        
        result_df['close_approach_date'] = result_df['close_approach_date'].dt.strftime('%Y-%m-%d')
        result_df.columns = [
            'Asteroid', 'Date', 'Distance (AU)', 'Velocity (km/s)',
            'Risk Score', 'Panic', 'Category', 'Orbit Type', 'Sentry'
        ]
        
        result_df['Sentry'] = result_df['Sentry'].map({True: '✅', False: '❌'})
        
        # Format numeric columns
        result_df['Distance (AU)'] = result_df['Distance (AU)'].apply(lambda x: f"{float(x):.6f}")
        result_df['Velocity (km/s)'] = result_df['Velocity (km/s)'].apply(lambda x: f"{float(x):.2f}")
        result_df['Risk Score'] = result_df['Risk Score'].apply(lambda x: f"{float(x):.4f}")
        
        # Calculate summary stats
        avg_risk = float(filtered['risk_score'].mean()) if len(filtered) > 0 else 0.0
        max_panic = int(filtered['panic_level'].max()) if len(filtered) > 0 else 0
        sentry_sum = int(filtered['on_sentry_list'].sum()) if len(filtered) > 0 else 0
        
        summary = f"""
### Search Results
- **Total Matches:** {len(filtered)} asteroids
- **Avg Risk Score:** {avg_risk:.4f}
- **Max Panic Level:** {max_panic}/10
- **Sentry Listed:** {sentry_sum}
        """
        
        return result_df, summary
        
    except Exception as e:
        return pd.DataFrame(), f"Error: {str(e)}"

def export_results(dataframe):
    """Export search results to CSV"""
    if dataframe is None or len(dataframe) == 0:
        return None
    
    output_path = '/tmp/asteroid_search_results.csv'
    dataframe.to_csv(output_path, index=False)
    return output_path

# ============================================================================
# BUILD GRADIO INTERFACE
# ============================================================================

# Custom CSS
custom_css = """
.gradio-container {
    font-family: 'Inter', sans-serif;
}
.gr-button-primary {
    background: linear-gradient(90deg, #ef4444, #dc2626) !important;
    border: none !important;
}
.gr-button-secondary {
    background: linear-gradient(90deg, #3b82f6, #2563eb) !important;
    border: none !important;
}
h1, h2, h3 {
    color: #ffffff !important;
}
"""

# Create Gradio Blocks
with gr.Blocks(theme=gr.themes.Base(primary_hue="red", secondary_hue="blue"), css=custom_css) as app:
    
    # Header
    gr.Markdown("""
    # 🌠 Don't Look Up: Asteroid Impact Tracker
    
    > *"Looking up is optional. The data isn't."*
    
    **Track 89,000+ asteroid close approaches with real NASA data and machine learning predictions.**
    
    Created by [@hasandafa](https://github.com/hasandafa) | 
    [GitHub](https://github.com/hasandafa/do-not-look-up) | 
    [Kaggle Dataset](https://www.kaggle.com/datasets/hasandafa1201/nasa-asteroid-impact-dataset)
    
    ---
    """)
    
    # Tabs
    with gr.Tabs():
        
        # ====================================================================
        # TAB 1: PANIC METER
        # ====================================================================
        with gr.Tab("🎯 The Panic Meter™"):
            gr.Markdown("""
            ## Should You Panic About This Asteroid?
            Select an asteroid and get an instant threat assessment with dark humor.
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    # Get top 100 highest risk asteroids for dropdown
                    top_asteroids = df.nlargest(100, 'risk_score')['asteroid_designation'].tolist()
                    
                    asteroid_input = gr.Dropdown(
                        choices=top_asteroids,
                        value=top_asteroids[0],
                        label="🔍 Choose Your Doom",
                        info="Select an asteroid from the top 100 highest risk"
                    )
                    
                    calculate_btn = gr.Button("Calculate Panic Level", variant="primary", size="lg")
                    
                    gr.Markdown("""
                    ---
                    ### 💡 Quick Facts
                    - **89,227** total close approaches tracked
                    - **2,000+** on NASA's Sentry risk list
                    - **2020-2100** date range
                    - **Real NASA data** (no fiction here)
                    """)
                
                with gr.Column(scale=2):
                    panic_gauge = gr.Plot(label="Panic Meter")
                    verdict_text = gr.Markdown()
            
            with gr.Row():
                stats_table = gr.Dataframe(label="📊 Detailed Statistics", interactive=False)
            
            # Connect button
            calculate_btn.click(
                fn=calculate_panic,
                inputs=[asteroid_input],
                outputs=[panic_gauge, verdict_text, stats_table]
            )
        
        # ====================================================================
        # TAB 2: APOCALYPSE CALENDAR
        # ====================================================================
        with gr.Tab("📅 Apocalypse Calendar"):
            gr.Markdown("""
            ## When Will The Sky Fall?
            Explore asteroid approaches by year and month. Filter by threat level.
            """)
            
            with gr.Row():
                year_slider = gr.Slider(
                    minimum=2020,
                    maximum=2100,
                    value=2025,
                    step=1,
                    label="📅 Select Year"
                )
                
                threat_filter = gr.CheckboxGroup(
                    choices=['SAFE', 'MONITOR', 'CONCERN', 'OH_NO'],
                    value=['MONITOR', 'CONCERN', 'OH_NO'],
                    label="⚠️ Show Threat Levels"
                )
            
            calendar_plot = gr.Plot(label="Monthly Threat Heatmap")
            
            event_table = gr.Dataframe(
                label="📋 Top Events This Year",
                interactive=False,
                wrap=True
            )
            
            # Auto-update on change
            year_slider.change(
                fn=generate_calendar,
                inputs=[year_slider, threat_filter],
                outputs=[calendar_plot, event_table]
            )
            
            threat_filter.change(
                fn=generate_calendar,
                inputs=[year_slider, threat_filter],
                outputs=[calendar_plot, event_table]
            )
            
            # Load initial
            app.load(
                fn=generate_calendar,
                inputs=[year_slider, threat_filter],
                outputs=[calendar_plot, event_table]
            )
        
        # ====================================================================
        # TAB 3: 3D SIMULATOR
        # ====================================================================
        with gr.Tab("🌌 Doom Simulator 3D"):
            gr.Markdown("""
            ## Visualize Asteroid Orbits
            Interactive 3D view of asteroid positions. That tiny blue dot is Earth. We live there.
            
            **Controls:**
            - 🖱️ **Drag** to rotate
            - 🔍 **Scroll** to zoom
            - 🎯 **Click** asteroids for details
            """)
            
            # Generate 3D plot on-the-fly instead of loading HTML
            def generate_3d_plot():
                try:
                    # Sample data for performance
                    high_risk = df[df['panic_level'] >= 5]
                    low_risk_sample = df[df['panic_level'] < 5].sample(n=min(2000, len(df[df['panic_level'] < 5])), random_state=42)
                    viz_df = pd.concat([high_risk, low_risk_sample]).copy()
                    
                    # Create coordinates
                    np.random.seed(42)
                    theta = np.random.uniform(0, 2*np.pi, len(viz_df))
                    phi = np.random.uniform(-np.pi/6, np.pi/6, len(viz_df))
                    
                    viz_df['x'] = viz_df['distance_au'] * np.cos(theta) * np.cos(phi)
                    viz_df['y'] = viz_df['distance_au'] * np.sin(theta) * np.cos(phi)
                    viz_df['z'] = viz_df['distance_au'] * np.sin(phi)
                    
                    # Create sizes (handle NaN)
                    sizes = (25 - viz_df['absolute_magnitude'].fillna(viz_df['absolute_magnitude'].median())) / 5
                    sizes = sizes.clip(0.5, 4).fillna(2)
                    
                    # Create plot
                    fig = go.Figure()
                    
                    # Earth
                    fig.add_trace(go.Scatter3d(
                        x=[0], y=[0], z=[0],
                        mode='markers+text',
                        name='Earth',
                        marker=dict(size=25, color='#3b82f6', line=dict(color='white', width=3)),
                        text=['🌍'],
                        textposition='top center',
                        textfont=dict(size=14, color='white'),
                        hovertext='🌍 Earth - Our home',
                        hoverinfo='text'
                    ))
                    
                    # Asteroids
                    hover_text = [
                        f"<b>{row['asteroid_designation']}</b><br>" +
                        f"Distance: {row['distance_au']:.6f} AU<br>" +
                        f"Velocity: {row['velocity_km_s']:.2f} km/s<br>" +
                        f"Panic: {row['panic_level']}/10<br>" +
                        f"Category: {row['threat_category']}"
                        for idx, row in viz_df.iterrows()
                    ]
                    
                    fig.add_trace(go.Scatter3d(
                        x=viz_df['x'],
                        y=viz_df['y'],
                        z=viz_df['z'],
                        mode='markers',
                        name='Asteroids',
                        marker=dict(
                            size=sizes,
                            color=viz_df['panic_level'],
                            colorscale='YlOrRd',
                            showscale=True,
                            colorbar=dict(title="Panic<br>Level", thickness=15, len=0.7),
                            line=dict(color='rgba(255,255,255,0.3)', width=0.5),
                            opacity=0.8
                        ),
                        text=hover_text,
                        hoverinfo='text'
                    ))
                    
                    # Layout
                    fig.update_layout(
                        title="🌌 Solar System Asteroid Distribution",
                        scene=dict(
                            xaxis=dict(title='X (AU)', backgroundcolor='black', gridcolor='#1e293b', 
                                      showbackground=True, range=[-2, 2]),
                            yaxis=dict(title='Y (AU)', backgroundcolor='black', gridcolor='#1e293b',
                                      showbackground=True, range=[-2, 2]),
                            zaxis=dict(title='Z (AU)', backgroundcolor='black', gridcolor='#1e293b',
                                      showbackground=True, range=[-0.5, 0.5]),
                            bgcolor='black',
                            camera=dict(eye=dict(x=1.2, y=1.2, z=0.8), center=dict(x=0, y=0, z=0)),
                            aspectmode='cube'
                        ),
                        paper_bgcolor='#0a0a0a',
                        font=dict(color='white'),
                        height=700,
                        showlegend=True,
                        legend=dict(x=0.85, y=0.95, bgcolor='rgba(0,0,0,0.7)', 
                                   bordercolor='white', borderwidth=1)
                    )
                    
                    return fig
                    
                except Exception as e:
                    # Return empty figure with error
                    fig = go.Figure()
                    fig.add_annotation(
                        text=f"Error loading 3D visualization: {str(e)}",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5, showarrow=False,
                        font=dict(size=16, color="white")
                    )
                    fig.update_layout(
                        paper_bgcolor='#0a0a0a',
                        plot_bgcolor='#0a0a0a',
                        height=700
                    )
                    return fig
            
            # Use Gradio Plot component for direct embedding
            plot_3d = gr.Plot(value=generate_3d_plot, label="3D Solar System")
            
            gr.Markdown("""
            ---
            ### ℹ️ About This Visualization
            
            This is a **simplified representation** of asteroid orbits. 
            
            - **Colors** represent panic level (yellow → red)
            - **Size** represents absolute magnitude (brightness)
            - **Position** is approximate based on distance and orbital parameters
            - **Earth** is the big blue sphere at the center with 🌍
            
            Real orbital mechanics require full ephemeris data from NASA JPL.
            """)
        
        # ====================================================================
        # TAB 4: SHOULD I WORRY?
        # ====================================================================
        with gr.Tab("🤖 Should I Worry?"):
            gr.Markdown("""
            ## ML-Powered Threat Assessment
            Get a worry score based on upcoming asteroid approaches. Uses machine learning and custom algorithms.
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    days_input = gr.Slider(
                        minimum=1,
                        maximum=365,
                        value=30,
                        step=1,
                        label="🗓️ Check Next N Days"
                    )
                    
                    location_input = gr.Radio(
                        choices=['Global', 'Northern Hemisphere', 'Southern Hemisphere'],
                        value='Global',
                        label="🌍 Your Location"
                    )
                    
                    worry_btn = gr.Button("Should I Worry?", variant="primary", size="lg")
                    
                    gr.Markdown("""
                    ---
                    ### How It Works
                    
                    The worry score combines:
                    - **Max panic level** (35%)
                    - **Average risk** (25%)
                    - **Sentry ratio** (20%)
                    - **Closest distance** (15%)
                    - **Threat distribution** (5%)
                    """)
                
                with gr.Column(scale=2):
                    worry_gauge = gr.Plot(label="Worry Score")
                    worry_verdict = gr.Markdown()
            
            with gr.Row():
                next_event_table = gr.Dataframe(
                    label="🎯 Next Close Approach",
                    interactive=False
                )
            
            # Connect button
            worry_btn.click(
                fn=check_worry,
                inputs=[days_input, location_input],
                outputs=[worry_gauge, worry_verdict, next_event_table]
            )
        
        # ====================================================================
        # TAB 5: THE WATCHLIST
        # ====================================================================
        with gr.Tab("🔍 The Watchlist"):
            gr.Markdown("""
            ## Search & Filter Asteroids
            Find specific asteroids or browse by threat level. Export results as CSV.
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    # Get all unique asteroids sorted by risk
                    all_asteroids = df.nlargest(500, 'risk_score')['asteroid_designation'].tolist()
                    
                    search_dropdown = gr.Dropdown(
                        choices=['All Asteroids'] + all_asteroids,
                        value='All Asteroids',
                        label="🔍 Select Asteroid",
                        info="Choose from top 500 highest risk asteroids"
                    )
                    
                    risk_min = gr.Slider(0, 1, 0, label="📊 Min Risk Score")
                    risk_max = gr.Slider(0, 1, 1, label="📊 Max Risk Score")
                    
                    threat_select = gr.CheckboxGroup(
                        choices=['SAFE', 'MONITOR', 'CONCERN', 'OH_NO'],
                        value=['MONITOR', 'CONCERN', 'OH_NO'],
                        label="⚠️ Threat Categories"
                    )
                    
                    limit_input = gr.Slider(
                        minimum=10,
                        maximum=500,
                        value=50,
                        step=10,
                        label="📄 Results Limit"
                    )
                    
                    search_btn = gr.Button("🔍 Search", variant="primary")
                    export_btn = gr.Button("📥 Export to CSV", variant="secondary")
                
                with gr.Column(scale=2):
                    summary_text = gr.Markdown()
                    results_table = gr.Dataframe(
                        label="Search Results",
                        interactive=False,
                        wrap=True
                    )
                    
                    download_file = gr.File(label="Download CSV", visible=False)
            
            # Connect search with dropdown support
            def search_with_dropdown(asteroid_choice, min_r, max_r, threats, lim):
                # If specific asteroid selected, use it as query
                if asteroid_choice and asteroid_choice != 'All Asteroids':
                    return search_asteroids(asteroid_choice, min_r, max_r, threats, lim)
                else:
                    return search_asteroids('', min_r, max_r, threats, lim)
            
            search_btn.click(
                fn=search_with_dropdown,
                inputs=[search_dropdown, risk_min, risk_max, threat_select, limit_input],
                outputs=[results_table, summary_text]
            )
            
            # Connect export
            def export_wrapper(df):
                file = export_results(df)
                return file, gr.File(visible=True)
            
            export_btn.click(
                fn=export_wrapper,
                inputs=[results_table],
                outputs=[download_file, download_file]
            )
    
    # Footer
    gr.Markdown("""
    ---
    
    ## 📚 Resources
    
    - **GitHub Repository:** [hasandafa/do-not-look-up](https://github.com/hasandafa/do-not-look-up)
    - **Kaggle Dataset:** [NASA Asteroid Impact Dataset](https://www.kaggle.com/datasets/hasandafa1201/nasa-asteroid-impact-dataset)
    - **Data Sources:** [NASA CNEOS](https://cneos.jpl.nasa.gov/) | [Sentry](https://cneos.jpl.nasa.gov/sentry/) | [NeoWs](https://api.nasa.gov/)
    
    ## 🙏 Acknowledgments
    
    - **NASA JPL** for tracking space rocks
    - **Kaggle** for hosting the dataset
    - **Coffee & Anxiety** for making this possible
    
    ---
    
    <div style="text-align: center; color: #888;">
    Made with 💀 and Python | Current Threat Level: <span style="color: #4ade80;">CHILL ✅</span>
    </div>
    
    <div style="text-align: center; margin-top: 10px;">
    <strong>Remember: Looking up is optional. The data isn't.</strong>
    </div>
    """)

# ============================================================================
# LAUNCH APPLICATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("🌠 DON'T LOOK UP: ASTEROID IMPACT TRACKER")
    print("=" * 80)
    print("\n🚀 Launching Gradio application...")
    print("📊 Dataset loaded: {:,} asteroids".format(len(df)))
    print("🤖 ML models: {}".format("✅ Loaded" if panic_model else "❌ Not loaded"))
    print("\n🌐 Opening in browser...")
    print("=" * 80)
    
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True
    )