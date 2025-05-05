import csv
import requests
from pathlib import Path
from utils.config import load_config
from utils.logger import log

MALWARE_DB_URL = "https://raw.githubusercontent.com/CYB3RMX/MalwareHashDB/main/HashDB"
KNOWN_MD5_HASHES = set()

def load_signatures():
    global KNOWN_MD5_HASHES
    config = load_config()
    db_file = config['malware_signatures']
    
    try:
        if not Path(db_file).exists():
            sync_repo()
            
        with open(db_file) as f:
            reader = csv.reader(f)
            for row in reader:
                if row:  # Skip empty lines
                    md5_hash = row[0].strip().lower()
                    KNOWN_MD5_HASHES.add(md5_hash)
        log(f"Loaded {len(KNOWN_MD5_HASHES)} MD5 malware hashes")
        
    except Exception as e:
        log(f"Error loading signatures: {str(e)}", 'error')
        KNOWN_MD5_HASHES = set()

def check_malware_signature(md5_hash):
    return md5_hash.lower() in KNOWN_MD5_HASHES

def sync_repo():
    config = load_config()
    db_file = config['malware_signatures']
    
    try:
        log("Syncing with MalwareHashDB...")
        response = requests.get(MALWARE_DB_URL)
        response.raise_for_status()
        
        # Save raw MD5 hashes
        with open(db_file, 'w') as f:
            f.write(response.text)
        
        log(f"Updated MD5 database with {len(response.text.splitlines())} entries")
        return True
        
    except requests.exceptions.RequestException as e:
        log(f"Sync failed: {str(e)}", 'error')
        return False