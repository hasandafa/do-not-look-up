"""
Don't Look Up: NASA Data Fetcher
Created by Abdullah Hasan Dafa (@hasandafa)

This script fetches asteroid data from 3 NASA APIs and saves them locally.
Because someone has to keep tabs on the space rocks while we're busy with TikTok.

APIs we're hitting:
1. Close Approach Data (CAD) - Every asteroid that got too close for comfort
2. Sentry API - The official "should we panic?" list
3. NeoWs API - Asteroid Tinder profiles (size, speed, distance preferences)
"""

import requests
import json
import time
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
from tqdm import tqdm


class NASADataFetcher:
    """
    Fetch asteroid data from NASA APIs with style.
    
    This class handles all the heavy lifting of talking to NASA's servers
    so you can focus on calculating panic levels.
    """
    
    def __init__(self, config_path: str = "../config.yaml"):
        """
        Initialize with existential dread and an API key.
        
        Args:
            config_path: Path to config file (default: ../config.yaml for notebooks)
        """
        self.config = self._load_config(config_path)
        
        # Read API key from text file
        api_key_file = self.config['nasa_api']['api_key_file']
        self.api_key = self._load_api_key(api_key_file)
        
        self.endpoints = self.config['nasa_api']['endpoints']
        self.session = requests.Session()
        
        # Create data directories
        raw_data_path = self.config['paths']['data']['raw']
        self.raw_data_path = Path(raw_data_path)
        self.raw_data_path.mkdir(parents=True, exist_ok=True)
        
        print("🚀 NASA Data Fetcher initialized!")
        print("📡 Ready to download some doom data...")
    
    def _load_config(self, config_path: str) -> Dict:
        """
        Load configuration from YAML file.
        
        Args:
            config_path: Path to config.yaml file
            
        Returns:
            Configuration dictionary
        """
        config_file = Path(config_path)
        
        if not config_file.exists():
            raise FileNotFoundError(
                f"🚨 Config file not found: {config_file.absolute()}\n\n"
                "Setup instructions:\n"
                "1. Make sure config.yaml exists in project root\n"
                "2. If not, copy: cp config.yaml.example config.yaml\n"
                f"3. Current directory: {Path.cwd()}\n"
                f"4. Looking for config at: {config_file.absolute()}"
            )
        
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        # Store config directory for relative path resolution
        config['_config_dir'] = config_file.parent.absolute()
        
        return config
    
    def _load_api_key(self, key_file: str) -> str:
        """
        Load NASA API key from text file.
        
        Args:
            key_file: Filename of text file containing API key (relative to config)
            
        Returns:
            API key as string
        """
        # API key file is in same directory as config file
        config_dir = self.config.get('_config_dir', Path.cwd())
        key_path = config_dir / key_file
        
        try:
            with open(key_path, 'r') as f:
                api_key = f.read().strip()
            
            if not api_key:
                raise ValueError(
                    "🚨 Your nasa_api_key.txt file is empty!\n"
                    "Add your NASA API key to the file (just the key, nothing else)\n"
                    "Get one free at https://api.nasa.gov/"
                )
            
            print(f"✅ API key loaded from {key_path}")
            print(f"🔑 Key preview: {api_key[:10]}...{api_key[-5:]}")
            return api_key
            
        except FileNotFoundError:
            raise FileNotFoundError(
                f"🚨 File '{key_path}' not found!\n\n"
                "Setup instructions:\n"
                "1. Create a file named 'nasa_api_key.txt' in project root\n"
                "2. Get your free NASA API key at https://api.nasa.gov/\n"
                "3. Paste ONLY the API key into the file (no quotes, no extra text)\n"
                "4. Save and run this script again\n\n"
                "Example nasa_api_key.txt content:\n"
                "abcdef123456789YOURKEY\n\n"
                "NASA won't judge your doomsday tracking hobby. Promise."
            )
    
    def _make_request(self, url: str, params: Dict = None, 
                     retry_count: int = 0) -> Optional[Dict]:
        """
        Make HTTP request with retry logic.
        
        Because sometimes NASA's servers are busy tracking actual threats.
        """
        max_retries = self.config['data_collection']['max_retries']
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            # Be nice to NASA's servers
            time.sleep(self.config['nasa_api']['rate_limit']['delay_between_requests'])
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            if retry_count < max_retries:
                print(f"⚠️  Request failed, retrying ({retry_count + 1}/{max_retries})...")
                time.sleep(2 ** retry_count)
                return self._make_request(url, params, retry_count + 1)
            else:
                print(f"❌ Failed after {max_retries} retries: {e}")
                return None
    
    def fetch_close_approaches(self) -> pd.DataFrame:
        """
        Fetch Close Approach Data (CAD).
        
        Returns every asteroid that came suspiciously close to Earth.
        """
        print("\n📡 Fetching Close Approach Data...")
        print("(Every time an asteroid said 'hey there' to Earth)")
        
        date_config = self.config['data_collection']['date_range']
        distance_config = self.config['data_collection']['distance']
        
        params = {
            'date-min': date_config['start'],
            'date-max': date_config['end'],
            'dist-max': distance_config['max_au'],
            'sort': 'date',
            'fullname': 'true'
        }
        
        url = self.endpoints['close_approach']
        data = self._make_request(url, params)
        
        if not data:
            print("❌ Failed to fetch close approach data")
            return pd.DataFrame()
        
        fields = data.get('fields', [])
        records = data.get('data', [])
        
        df = pd.DataFrame(records, columns=fields)
        
        # Save raw data
        output_path = self.raw_data_path / 'close_approaches_raw.json'
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Fetched {len(df):,} close approaches")
        print(f"💾 Saved to {output_path}")
        
        return df
    
    def fetch_sentry_objects(self) -> pd.DataFrame:
        """
        Fetch Sentry Risk Table.
        
        This is NASA's official "these asteroids might hit us" list.
        """
        print("\n📡 Fetching Sentry Risk Table...")
        print("(The 'maybe panic?' list)")
        
        url = self.endpoints['sentry']
        data = self._make_request(url)
        
        if not data:
            print("❌ Failed to fetch Sentry data")
            return pd.DataFrame()
        
        # Sentry API returns data in "data" array (updated format)
        if 'data' in data and isinstance(data['data'], list):
            # Direct array format (current API)
            sentry_objects = data['data']
            print(f"✅ Fetched {len(sentry_objects):,} high-risk asteroids")
        elif 'sentry' in data:
            # Old format: dictionary of objects
            sentry_objects = []
            for des, obj_data in data['sentry'].items():
                obj_data['designation'] = des
                sentry_objects.append(obj_data)
            print(f"✅ Fetched {len(sentry_objects):,} high-risk asteroids")
        else:
            print("⚠️  Unexpected Sentry data format")
            sentry_objects = []
        
        df = pd.DataFrame(sentry_objects)
        
        # Save raw data
        output_path = self.raw_data_path / 'sentry_objects_raw.json'
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        if len(df) > 0:
            print(f"   (Don't worry, 'high-risk' is relative)")
            print(f"💾 Saved to {output_path}")
        else:
            print(f"   No high-risk asteroids found (that's good news!)")
        
        return df
    
    def fetch_neows_data(self, batch_size: int = 7) -> pd.DataFrame:
        """
        Fetch Near Earth Object Web Service (NeoWs) data.
        
        This gives us the juicy details about each asteroid.
        """
        print("\n📡 Fetching NeoWs Data...")
        print("(The asteroid dating profiles)")
        
        date_config = self.config['data_collection']['date_range']
        start_date = datetime.strptime(date_config['start'], '%Y-%m-%d')
        end_date = datetime.strptime(date_config['end'], '%Y-%m-%d')
        
        all_asteroids = []
        current_date = start_date
        
        total_days = (end_date - start_date).days
        iterations = total_days // batch_size + 1
        
        print(f"📅 Fetching from {start_date.date()} to {end_date.date()}")
        print(f"⏱️  This might take a while. Maybe grab a coffee?")
        
        with tqdm(total=iterations, desc="Fetching NeoWs") as pbar:
            while current_date < end_date:
                batch_end = min(current_date + timedelta(days=batch_size), end_date)
                
                params = {
                    'start_date': current_date.strftime('%Y-%m-%d'),
                    'end_date': batch_end.strftime('%Y-%m-%d'),
                    'api_key': self.api_key
                }
                
                url = f"{self.endpoints['neows']}/feed"
                data = self._make_request(url, params)
                
                if data and 'near_earth_objects' in data:
                    for date, objects in data['near_earth_objects'].items():
                        all_asteroids.extend(objects)
                
                current_date = batch_end + timedelta(days=1)
                pbar.update(1)
        
        df = pd.DataFrame(all_asteroids)
        
        # Save raw data
        output_path = self.raw_data_path / 'neows_data_raw.json'
        with open(output_path, 'w') as f:
            json.dump({'asteroids': all_asteroids}, f, indent=2)
        
        print(f"\n✅ Fetched {len(df):,} asteroid records")
        print(f"💾 Saved to {output_path}")
        
        return df
    
    def fetch_all_data(self) -> Dict[str, pd.DataFrame]:
        """
        Fetch everything from all 3 NASA APIs.
        
        This is the main event. Grab your popcorn.
        """
        print("\n" + "="*60)
        print("🚀 Don't Look Up: NASA Data Collection")
        print("   Created by Abdullah Hasan Dafa (@hasandafa)")
        print("="*60)
        
        start_time = time.time()
        
        data = {
            'close_approaches': self.fetch_close_approaches(),
            'sentry': self.fetch_sentry_objects(),
            'neows': self.fetch_neows_data()
        }
        
        elapsed = time.time() - start_time
        
        print("\n" + "="*60)
        print("✨ DATA COLLECTION COMPLETE!")
        print("="*60)
        print(f"⏱️  Time elapsed: {elapsed:.1f} seconds")
        print(f"📊 Close Approaches: {len(data['close_approaches']):,} records")
        print(f"📊 Sentry Objects: {len(data['sentry']):,} records")
        print(f"📊 NeoWs Data: {len(data['neows']):,} records")
        print(f"\n💾 All raw data saved to: {self.raw_data_path}")
        print("\n☕ Go grab a coffee. You've earned it.")
        print("   (The apocalypse can wait)")
        
        return data


def main():
    """
    Main execution function.
    
    Run this to download all the doom data from NASA.
    """
    try:
        fetcher = NASADataFetcher(config_path="config.yaml")
        
        data = fetcher.fetch_all_data()
        
        print("\n📈 QUICK STATS:")
        print(f"   • Total unique asteroids tracked: {len(data['neows']):,}")
        print(f"   • High-risk asteroids (Sentry): {len(data['sentry']):,}")
        print(f"   • Close approaches logged: {len(data['close_approaches']):,}")
        
        if len(data['sentry']) > 0:
            print(f"\n⚠️  Should you panic? Nah, we're good.")
            print(f"   (But we're watching {len(data['sentry'])} suspicious ones)")
        else:
            print(f"\n✅ Should you panic? Definitely not.")
            print(f"   (No high-risk asteroids currently tracked)")
        
        print("\n✅ SUCCESS! Raw data collection complete.")
        print("📝 Next step: Run 01_fetch_the_doom.ipynb to explore the data")
        print("   Or run scripts/process_dataset.py to create the final dataset")
        
    except FileNotFoundError:
        print("\n❌ ERROR: config.yaml not found!")
        print("💡 Make sure you're running this from the project root directory")
        print("   Example: python scripts/fetch_nasa_data.py")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("💡 Check your config.yaml and internet connection")
        print("   Also make sure your NASA API key is valid")


if __name__ == "__main__":
    main()