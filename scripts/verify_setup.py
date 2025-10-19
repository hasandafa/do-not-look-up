"""
Don't Look Up: Setup Verification Script
Created by Abdullah Hasan Dafa (@hasandafa)

This script verifies that your setup is correct before fetching data.
Run this first to make sure everything is configured properly.

Usage:
    python scripts/verify_setup.py
"""

import sys
from pathlib import Path
import yaml


def print_header():
    """Print script header."""
    print("\n" + "="*60)
    print("🔍 Don't Look Up: Setup Verification")
    print("   Created by Abdullah Hasan Dafa (@hasandafa)")
    print("="*60 + "\n")


def check_file_exists(filepath: str, name: str, required: bool = True) -> bool:
    """
    Check if a file exists.
    
    Args:
        filepath: Path to file
        name: Display name for the file
        required: Whether file is required
        
    Returns:
        True if exists (or not required), False otherwise
    """
    if Path(filepath).exists():
        print(f"✅ {name}: Found")
        return True
    else:
        if required:
            print(f"❌ {name}: NOT FOUND (required)")
            return False
        else:
            print(f"⚠️  {name}: NOT FOUND (optional)")
            return True


def check_api_key() -> bool:
    """
    Check if NASA API key is configured correctly.
    
    Returns:
        True if key is valid, False otherwise
    """
    print("\n📡 Checking NASA API Key...")
    print("-" * 60)
    
    # Check if key file exists
    key_file = "nasa_api_key.txt"
    if not Path(key_file).exists():
        print(f"❌ File '{key_file}' not found!")
        print("\n📝 Setup instructions:")
        print("   1. Create a file named 'nasa_api_key.txt'")
        print("   2. Get your free API key at https://api.nasa.gov/")
        print("   3. Paste ONLY your API key into the file")
        print("   4. Save and run this script again")
        print("\n   Example content:")
        print("   abcdef123456789YOURKEY")
        return False
    
    # Read and validate key
    try:
        with open(key_file, 'r') as f:
            api_key = f.read().strip()
        
        if not api_key:
            print(f"❌ File '{key_file}' is empty!")
            print("   Add your NASA API key to the file")
            return False
        
        if api_key == "YOUR_NASA_API_KEY_HERE":
            print(f"❌ Still using placeholder key!")
            print("   Replace with your actual API key from https://api.nasa.gov/")
            return False
        
        if len(api_key) < 20:
            print(f"⚠️  API key seems short ({len(api_key)} characters)")
            print("   NASA keys are usually 40 characters")
            print("   Make sure you copied the full key")
        
        print(f"✅ API key found: {api_key[:10]}...{api_key[-5:]}")
        print(f"   Length: {len(api_key)} characters")
        return True
        
    except Exception as e:
        print(f"❌ Error reading API key: {e}")
        return False


def check_config() -> bool:
    """
    Check if config.yaml is set up correctly.
    
    Returns:
        True if config is valid, False otherwise
    """
    print("\n⚙️  Checking Configuration File...")
    print("-" * 60)
    
    config_file = "config.yaml"
    
    if not Path(config_file).exists():
        print(f"❌ File '{config_file}' not found!")
        print("\n📝 Setup instructions:")
        print("   cp config.yaml.example config.yaml")
        return False
    
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        print(f"✅ config.yaml loaded successfully")
        
        # Check API key file setting
        if 'nasa_api' in config and 'api_key_file' in config['nasa_api']:
            key_file = config['nasa_api']['api_key_file']
            print(f"✅ API key file setting: {key_file}")
        else:
            print(f"⚠️  API key file setting not found in config")
        
        # Check paths
        if 'paths' in config:
            print(f"✅ Paths configured")
        else:
            print(f"⚠️  Paths not configured")
        
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ Error parsing config.yaml: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading config.yaml: {e}")
        return False


def check_dependencies() -> bool:
    """
    Check if required Python packages are installed.
    
    Returns:
        True if all dependencies installed, False otherwise
    """
    print("\n📦 Checking Python Dependencies...")
    print("-" * 60)
    
    required_packages = [
        'pandas',
        'numpy',
        'requests',
        'yaml',
        'plotly',
        'matplotlib',
        'seaborn',
        'tqdm'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package if package != 'yaml' else 'PyYAML')
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing {len(missing_packages)} package(s)")
        print("\n📝 Install missing packages:")
        print("   pip install -r requirements.txt")
        return False
    
    return True


def check_directory_structure() -> bool:
    """
    Check if required directories exist (or can be created).
    
    Returns:
        True if structure is OK, False otherwise
    """
    print("\n📁 Checking Directory Structure...")
    print("-" * 60)
    
    required_dirs = [
        'scripts',
        'notebooks',
        'kaggle'
    ]
    
    optional_dirs = [
        'data',
        'data/raw',
        'data/processed',
        'logs'
    ]
    
    all_ok = True
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ - NOT FOUND")
            all_ok = False
    
    for dir_path in optional_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/ (will be created automatically)")
        else:
            print(f"⚠️  {dir_path}/ (will be created automatically)")
    
    return all_ok


def check_notebooks() -> bool:
    """
    Check if Jupyter notebooks exist.
    
    Returns:
        True if notebooks found, False otherwise
    """
    print("\n📓 Checking Jupyter Notebooks...")
    print("-" * 60)
    
    notebooks = [
        'notebooks/01_fetch_the_doom.ipynb',
        'notebooks/02_exploring_armageddon.ipynb'
    ]
    
    all_found = True
    
    for notebook in notebooks:
        if Path(notebook).exists():
            print(f"✅ {notebook}")
        else:
            print(f"❌ {notebook} - NOT FOUND")
            all_found = False
    
    return all_found


def test_api_connection() -> bool:
    """
    Test connection to NASA API (optional).
    
    Returns:
        True if connection successful, False otherwise
    """
    print("\n🌐 Testing NASA API Connection...")
    print("-" * 60)
    
    try:
        import requests
        
        # Read API key
        with open('nasa_api_key.txt', 'r') as f:
            api_key = f.read().strip()
        
        # Test simple endpoint
        url = "https://api.nasa.gov/neo/rest/v1/neo/browse"
        params = {'api_key': api_key, 'page': 0, 'size': 1}
        
        print("   Sending test request to NASA API...")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            print("✅ NASA API connection successful!")
            print(f"   Status: {response.status_code}")
            return True
        elif response.status_code == 403:
            print("❌ API key rejected (403 Forbidden)")
            print("   Your API key might be invalid")
            print("   Get a new key at https://api.nasa.gov/")
            return False
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("⚠️  Connection timeout (NASA servers might be slow)")
        print("   Your setup is probably fine, try running the script")
        return True
    except requests.exceptions.ConnectionError:
        print("⚠️  Connection error (check your internet)")
        return False
    except Exception as e:
        print(f"⚠️  Could not test connection: {e}")
        print("   Your setup might still be fine")
        return True


def print_summary(results: dict):
    """
    Print summary of verification results.
    
    Args:
        results: Dictionary of check results
    """
    print("\n" + "="*60)
    print("📊 VERIFICATION SUMMARY")
    print("="*60 + "\n")
    
    total = len(results)
    passed = sum(results.values())
    
    for check, status in results.items():
        emoji = "✅" if status else "❌"
        print(f"{emoji} {check}")
    
    print("\n" + "-"*60)
    print(f"Results: {passed}/{total} checks passed")
    print("-"*60 + "\n")
    
    if passed == total:
        print("🎉 ALL CHECKS PASSED!")
        print("\n✅ Your setup is complete!")
        print("\n📝 Next steps:")
        print("   1. Run: python scripts/fetch_nasa_data.py")
        print("   2. Then: python scripts/process_dataset.py")
        print("   3. Or open: notebooks/01_fetch_the_doom.ipynb")
        print("\n🚀 Happy asteroid tracking!")
    else:
        print("⚠️  SOME CHECKS FAILED")
        print("\n📝 Please fix the issues above before continuing.")
        print("\nNeed help? Check:")
        print("   - README.md")
        print("   - QUICK_START.md")
        print("   - GitHub Issues: github.com/hasandafa/do-not-look-up")


def main():
    """Main verification function."""
    print_header()
    
    results = {
        'API Key File': check_api_key(),
        'Config File': check_config(),
        'Python Dependencies': check_dependencies(),
        'Directory Structure': check_directory_structure(),
        'Jupyter Notebooks': check_notebooks(),
    }
    
    # Optional API test
    if results['API Key File'] and results['Config File']:
        print("\n🧪 Running Optional Tests...")
        print("-" * 60)
        results['API Connection'] = test_api_connection()
    
    print_summary(results)
    
    # Exit code
    if all(results.values()):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()