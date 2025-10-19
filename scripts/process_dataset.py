"""
Don't Look Up: Dataset Processor
Created by Abdullah Hasan Dafa (@hasandafa)

This script takes the raw NASA data and turns it into a beautiful,
clean dataset ready for Kaggle (and your impending existential crisis).

What it does:
1. Loads raw data from all 3 sources
2. Cleans & standardizes everything
3. Merges them into one unified dataset
4. Calculates risk scores & panic levels
5. Exports to multiple formats (CSV, Parquet, JSON)
"""

import pandas as pd
import numpy as np
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple
import warnings
warnings.filterwarnings('ignore')


class AsteroidDataProcessor:
    """
    Process and merge asteroid data from multiple sources.
    
    Turns chaos into order. Turns terror into tables.
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the processor with config.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.raw_path = Path(self.config['paths']['data']['raw'])
        self.processed_path = Path(self.config['paths']['data']['processed'])
        self.processed_path.mkdir(parents=True, exist_ok=True)
        
        print("🔧 Asteroid Data Processor initialized!")
        print("📂 Ready to turn chaos into clean data...")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def load_raw_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load all raw data files.
        
        Returns:
            Dictionary with DataFrames from all sources
        """
        print("\n📂 Loading raw data files...")
        
        data = {}
        
        # Load Close Approaches
        try:
            with open(self.raw_path / 'close_approaches_raw.json', 'r') as f:
                ca_data = json.load(f)
                data['close_approaches'] = pd.DataFrame(
                    ca_data['data'], 
                    columns=ca_data['fields']
                )
            print(f"  ✅ Close Approaches: {len(data['close_approaches']):,} records")
        except FileNotFoundError:
            print("  ⚠️  Close Approaches data not found (run fetch script first)")
            data['close_approaches'] = pd.DataFrame()
        
        # Load Sentry Objects
        try:
            with open(self.raw_path / 'sentry_objects_raw.json', 'r') as f:
                sentry_data = json.load(f)
                
                # Handle both old and new Sentry API formats
                if 'data' in sentry_data and isinstance(sentry_data['data'], list):
                    # New format: direct array
                    data['sentry'] = pd.DataFrame(sentry_data['data'])
                elif 'sentry' in sentry_data:
                    # Old format: dictionary of objects
                    sentry_list = []
                    for des, obj in sentry_data['sentry'].items():
                        obj['designation'] = des
                        sentry_list.append(obj)
                    data['sentry'] = pd.DataFrame(sentry_list)
                else:
                    data['sentry'] = pd.DataFrame()
                    
            print(f"  ✅ Sentry Objects: {len(data['sentry']):,} records")
        except FileNotFoundError:
            print("  ⚠️  Sentry data not found (run fetch script first)")
            data['sentry'] = pd.DataFrame()
        
        # Load NeoWs Data
        try:
            with open(self.raw_path / 'neows_data_raw.json', 'r') as f:
                neows_data = json.load(f)
                data['neows'] = pd.DataFrame(neows_data['asteroids'])
            print(f"  ✅ NeoWs Data: {len(data['neows']):,} records")
        except FileNotFoundError:
            print("  ⚠️  NeoWs data not found (run fetch script first)")
            data['neows'] = pd.DataFrame()
        
        return data
    
    def clean_close_approaches(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize close approach data.
        
        Args:
            df: Raw close approaches DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        if df.empty:
            return df
        
        print("\n🧹 Cleaning Close Approaches data...")
        
        # Rename columns for clarity
        column_mapping = {
            'des': 'designation',
            'orbit_id': 'orbit_id',
            'jd': 'julian_date',
            'cd': 'close_approach_date',
            'dist': 'distance_au',
            'dist_min': 'distance_min_au',
            'dist_max': 'distance_max_au',
            'v_rel': 'velocity_km_s',
            'v_inf': 'velocity_infinity_km_s',
            'h': 'absolute_magnitude',
            'fullname': 'full_name'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Convert data types
        numeric_cols = [
            'distance_au', 'distance_min_au', 'distance_max_au',
            'velocity_km_s', 'velocity_infinity_km_s', 'absolute_magnitude'
        ]
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Parse dates
        if 'close_approach_date' in df.columns:
            df['close_approach_datetime'] = pd.to_datetime(
                df['close_approach_date'], 
                errors='coerce'
            )
            df['year'] = df['close_approach_datetime'].dt.year
            df['month'] = df['close_approach_datetime'].dt.month
            df['day'] = df['close_approach_datetime'].dt.day
        
        # Calculate days until approach
        today = pd.Timestamp.now()
        df['days_until_approach'] = (
            df['close_approach_datetime'] - today
        ).dt.days
        
        # Categorize approaches
        df['is_past'] = df['days_until_approach'] < 0
        df['is_upcoming'] = df['days_until_approach'] >= 0
        
        print(f"  ✅ Cleaned {len(df):,} close approach records")
        print(f"     • Past approaches: {df['is_past'].sum():,}")
        print(f"     • Upcoming approaches: {df['is_upcoming'].sum():,}")
        
        return df
    
    def clean_sentry_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize Sentry risk data.
        
        Args:
            df: Raw Sentry DataFrame
            
        Returns:
            Cleaned DataFrame with risk metrics
        """
        if df.empty:
            return df
        
        print("\n🧹 Cleaning Sentry (risk) data...")
        
        # Extract nested data if present
        if 'ip' in df.columns:
            df['impact_probability'] = pd.to_numeric(df['ip'], errors='coerce')
        
        if 'ps_max' in df.columns:
            df['palermo_scale_max'] = pd.to_numeric(df['ps_max'], errors='coerce')
        
        if 'ts_max' in df.columns:
            df['torino_scale_max'] = pd.to_numeric(df['ts_max'], errors='coerce')
        
        # Add risk flags
        df['is_high_risk'] = True  # All Sentry objects are considered risky
        df['on_sentry_list'] = True
        
        print(f"  ✅ Cleaned {len(df):,} high-risk asteroids")
        
        return df
    
    def clean_neows_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize NeoWs detailed data.
        
        Args:
            df: Raw NeoWs DataFrame
            
        Returns:
            Cleaned DataFrame with physical properties
        """
        if df.empty:
            return df
        
        print("\n🧹 Cleaning NeoWs (detailed) data...")
        
        # Extract nested fields
        if 'estimated_diameter' in df.columns:
            df['diameter_km_min'] = df['estimated_diameter'].apply(
                lambda x: x.get('kilometers', {}).get('estimated_diameter_min', np.nan)
                if isinstance(x, dict) else np.nan
            )
            df['diameter_km_max'] = df['estimated_diameter'].apply(
                lambda x: x.get('kilometers', {}).get('estimated_diameter_max', np.nan)
                if isinstance(x, dict) else np.nan
            )
            df['diameter_km_avg'] = (df['diameter_km_min'] + df['diameter_km_max']) / 2
        
        # Extract orbital data
        if 'orbital_data' in df.columns:
            df['orbital_period_days'] = df['orbital_data'].apply(
                lambda x: float(x.get('orbital_period', np.nan))
                if isinstance(x, dict) else np.nan
            )
            df['eccentricity'] = df['orbital_data'].apply(
                lambda x: float(x.get('eccentricity', np.nan))
                if isinstance(x, dict) else np.nan
            )
        
        # Extract hazard status
        if 'is_potentially_hazardous_asteroid' in df.columns:
            df['is_hazardous'] = df['is_potentially_hazardous_asteroid']
        
        # Extract absolute magnitude
        if 'absolute_magnitude_h' in df.columns:
            df['absolute_magnitude'] = pd.to_numeric(
                df['absolute_magnitude_h'], 
                errors='coerce'
            )
        
        print(f"  ✅ Cleaned {len(df):,} asteroid profiles")
        if 'is_hazardous' in df.columns:
            hazardous_count = df['is_hazardous'].sum()
            print(f"     • Potentially Hazardous: {hazardous_count:,} (yikes)")
        
        return df
    
    def calculate_risk_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate custom risk scores and panic levels.
        
        This is where the magic (and anxiety) happens.
        
        Args:
            df: Merged DataFrame
            
        Returns:
            DataFrame with risk scores
        """
        print("\n🎯 Calculating risk scores & panic levels...")
        
        # Initialize risk score
        df['risk_score'] = 0.0
        df['panic_level'] = 0
        
        # Factor 1: Distance (closer = scarier)
        if 'distance_au' in df.columns:
            # Normalize distance (inverse relationship)
            max_dist = df['distance_au'].max()
            df['distance_risk'] = 1 - (df['distance_au'] / max_dist)
            df['risk_score'] += df['distance_risk'] * 0.3  # 30% weight
        
        # Factor 2: Size (bigger = worse)
        if 'diameter_km_avg' in df.columns:
            # Normalize size
            max_size = df['diameter_km_avg'].max()
            df['size_risk'] = df['diameter_km_avg'] / max_size
            df['risk_score'] += df['size_risk'] * 0.25  # 25% weight
        
        # Factor 3: Velocity (faster = more energetic impact)
        if 'velocity_km_s' in df.columns:
            max_vel = df['velocity_km_s'].max()
            df['velocity_risk'] = df['velocity_km_s'] / max_vel
            df['risk_score'] += df['velocity_risk'] * 0.20  # 20% weight
        
        # Factor 4: Time until approach (sooner = more immediate concern)
        if 'days_until_approach' in df.columns:
            # Only for upcoming approaches
            upcoming = df['days_until_approach'] > 0
            if upcoming.any():
                max_days = df.loc[upcoming, 'days_until_approach'].max()
                df.loc[upcoming, 'time_risk'] = 1 - (
                    df.loc[upcoming, 'days_until_approach'] / max_days
                )
                df['risk_score'] += df['time_risk'].fillna(0) * 0.15  # 15% weight
        
        # Factor 5: Sentry list bonus
        if 'on_sentry_list' in df.columns:
            df.loc[df['on_sentry_list'] == True, 'risk_score'] += 0.10
        
        # Normalize to 0-1 range
        df['risk_score'] = df['risk_score'].clip(0, 1)
        
        # Calculate panic levels (0-10 scale)
        df['panic_level'] = (df['risk_score'] * 10).round().astype(int)
        
        # Categorize threat levels
        df['threat_category'] = pd.cut(
            df['panic_level'],
            bins=[-1, 2, 4, 7, 10],
            labels=['SAFE', 'MONITOR', 'CONCERN', 'OH_NO']
        )
        
        # Add fun descriptions
        threat_descriptions = {
            'SAFE': "You're fine. Go touch grass.",
            'MONITOR': "Worth a tweet, not worth a bunker.",
            'CONCERN': "Time to learn survival skills?",
            'OH_NO': "Did you backup your data?"
        }
        df['should_you_panic'] = df['threat_category'].map(threat_descriptions)
        
        print(f"  ✅ Risk scores calculated!")
        print(f"\n  📊 Threat Distribution:")
        threat_counts = df['threat_category'].value_counts().sort_index()
        for category, count in threat_counts.items():
            print(f"     • {category}: {count:,} asteroids")
        
        return df
    
    def merge_datasets(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Merge all datasets into one unified DataFrame.
        
        Args:
            data: Dictionary with cleaned DataFrames
            
        Returns:
            Unified DataFrame
        """
        print("\n🔀 Merging datasets...")
        
        # Start with close approaches as base
        merged = data['close_approaches'].copy()
        
        # Merge with Sentry data
        if not data['sentry'].empty:
            sentry_cols = [
                'designation', 'impact_probability', 
                'palermo_scale_max', 'torino_scale_max',
                'on_sentry_list'
            ]
            available_cols = [c for c in sentry_cols if c in data['sentry'].columns]
            
            merged = merged.merge(
                data['sentry'][available_cols],
                on='designation',
                how='left',
                suffixes=('', '_sentry')
            )
        
        # Merge with NeoWs data (by designation/ID)
        if not data['neows'].empty:
            # Match on designation or name
            neows_cols = [
                'id', 'name', 'diameter_km_avg', 
                'orbital_period_days', 'eccentricity', 
                'is_hazardous', 'absolute_magnitude'
            ]
            available_cols = [c for c in neows_cols if c in data['neows'].columns]
            
            # Try to merge (this might be tricky due to naming differences)
            # For now, we'll keep them separate and note which need manual matching
            
        print(f"  ✅ Merged into {len(merged):,} records")
        
        return merged
    
    def export_dataset(self, df: pd.DataFrame):
        """
        Export processed dataset in multiple formats.
        
        Args:
            df: Processed DataFrame
        """
        print("\n💾 Exporting processed dataset...")
        
        timestamp = datetime.now().strftime('%Y%m%d')
        
        # Export to Parquet (efficient)
        parquet_path = self.processed_path / f'asteroid_dataset_{timestamp}.parquet'
        df.to_parquet(parquet_path, index=False)
        print(f"  ✅ Parquet: {parquet_path}")
        
        # Export to CSV (Kaggle-friendly)
        csv_path = self.processed_path / f'asteroid_dataset_{timestamp}.csv'
        df.to_csv(csv_path, index=False)
        print(f"  ✅ CSV: {csv_path}")
        
        # Export summary stats to JSON
        summary = {
            'generated_at': datetime.now().isoformat(),
            'total_records': len(df),
            'date_range': {
                'start': df['close_approach_date'].min() if 'close_approach_date' in df.columns else None,
                'end': df['close_approach_date'].max() if 'close_approach_date' in df.columns else None
            },
            'threat_distribution': df['threat_category'].value_counts().to_dict() if 'threat_category' in df.columns else {},
            'columns': list(df.columns)
        }
        
        json_path = self.processed_path / f'dataset_summary_{timestamp}.json'
        with open(json_path, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        print(f"  ✅ Summary: {json_path}")
        
        # File sizes
        print(f"\n  📦 File Sizes:")
        print(f"     • Parquet: {parquet_path.stat().st_size / 1024 / 1024:.2f} MB")
        print(f"     • CSV: {csv_path.stat().st_size / 1024 / 1024:.2f} MB")
    
    def process_all(self) -> pd.DataFrame:
        """
        Run the complete processing pipeline.
        
        Returns:
            Final processed DataFrame
        """
        print("\n" + "="*60)
        print("🔧 Don't Look Up: Dataset Processing Pipeline")
        print("   Created by Abdullah Hasan Dafa (@hasandafa)")
        print("="*60)
        
        # Load raw data
        raw_data = self.load_raw_data()
        
        # Clean each dataset
        cleaned_data = {
            'close_approaches': self.clean_close_approaches(raw_data['close_approaches']),
            'sentry': self.clean_sentry_data(raw_data['sentry']),
            'neows': self.clean_neows_data(raw_data['neows'])
        }
        
        # Merge everything
        merged = self.merge_datasets(cleaned_data)
        
        # Calculate risk scores
        final = self.calculate_risk_scores(merged)
        
        # Export
        self.export_dataset(final)
        
        print("\n" + "="*60)
        print("✨ PROCESSING COMPLETE!")
        print("="*60)
        print(f"📊 Final dataset: {len(final):,} records")
        print(f"📁 Saved to: {self.processed_path}")
        print("\n☕ Dataset ready for Kaggle upload!")
        print("   (Or your next existential crisis)")
        
        return final


def main():
    """
    Main execution function.
    """
    try:
        processor = AsteroidDataProcessor()
        df = processor.process_all()
        
        print("\n✅ SUCCESS!")
        print("📝 Next steps:")
        print("   1. Check data/processed/ folder for your datasets")
        print("   2. Review 02_exploring_armageddon.ipynb")
        print("   3. Upload to Kaggle when ready!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("💡 Make sure you've run scripts/fetch_nasa_data.py first")


if __name__ == "__main__":
    main()