import json
from pathlib import Path

# Add these constants at the top
CONFIG_FILE = 'telperion_config.json'
DEFAULT_CONFIG = {
    "scan_paths": ["/"],
    "quarantine_dir": "quarantine",
    "scan_interval": 7,
    "sync_interval": 7,
    "network_monitoring": False,
    "malware_signatures": "md5_hashdb.csv"  # Changed to CSV extension
}

def load_config():
    # Now using the properly defined CONSTANT
    if not Path(CONFIG_FILE).exists():
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f)
        return DEFAULT_CONFIG
    with open(CONFIG_FILE) as f:
        return json.load(f)

def update_config(new_settings):
    config = load_config()
    config.update(new_settings)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)