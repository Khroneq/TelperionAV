import schedule
import time
import threading
from core.scanner import initial_scan, start_monitoring
from modules.samples import sync_repo, load_signatures
from modules.network_monitor import start_network_monitor
from utils.config import load_config
from utils.logger import setup_logger
from pathlib import Path

def run_scheduler():
    config = load_config()
    schedule.every(config['sync_interval']).days.do(sync_repo)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    setup_logger()
    
    # Initial sync if no DB exists
    config = load_config()
    db_path = Path(config['malware_signatures'])
    
    if not db_path.exists():
        from modules.samples import sync_repo
        sync_repo()

    load_signatures()
    
    # Initial scan
    initial_scan()
    
    # Start monitoring
    monitoring_thread = threading.Thread(target=start_monitoring)
    monitoring_thread.daemon = True
    monitoring_thread.start()
    
    # Schedule updates
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # Network monitoring
    network_thread = threading.Thread(target=start_network_monitor)
    network_thread.daemon = True
    network_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down Telperion Scanner...")

if __name__ == "__main__":
    main()