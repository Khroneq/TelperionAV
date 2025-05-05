import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .filehash import calculate_md5
from .quarantine import quarantine_file
from utils.config import load_config
from utils.logger import log
from modules.samples import check_malware_signature

class ScanHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.scan_file(event.src_path)

    # In the ScanHandler class
    def scan_file(self, file_path):
        md5_hash = calculate_md5(file_path)
        if not md5_hash:
            return

        if check_malware_signature(md5_hash):
            log(f"Malware detected: {file_path} (MD5: {md5_hash})", 'warning')
            quarantine_file(file_path, load_config()['quarantine_dir'])

def initial_scan():
    config = load_config()
    log("🚀 Starting initial system scan...")
    file_count = 0
    start_time = time.time()
    
    for scan_path in config['scan_paths']:
        for root, dirs, files in os.walk(scan_path):
            for file in files:
                file_path = os.path.join(root, file)
                ScanHandler().scan_file(file_path)
                file_count += 1
                if file_count % 100 == 0:  # Update every 100 files
                    log(f"🔍 Scanned {file_count} files...")
    
    duration = time.time() - start_time
    log(f"✅ Initial scan completed: {file_count} files scanned in {duration:.2f} seconds")

def start_monitoring():
    config = load_config()
    observer = Observer()
    event_handler = ScanHandler()
    
    log("👀 Starting real-time monitoring...")
    log(f"📁 Watching directories: {', '.join(config['scan_paths'])}")
    
    for path in config['scan_paths']:
        if os.path.exists(path):
            observer.schedule(event_handler, path, recursive=True)
    
    observer.start()
    try:
        while True:
            time.sleep(5)
            log("🔄 Monitoring active...")  # Heartbeat message
    except KeyboardInterrupt:
        observer.stop()
    observer.join()