import shutil
from pathlib import Path
from utils.logger import log

def quarantine_file(file_path, quarantine_dir):
    try:
        Path(quarantine_dir).mkdir(exist_ok=True)
        dest = Path(quarantine_dir) / Path(file_path).name
        shutil.move(file_path, dest)
        log(f"Quarantined file: {file_path}", 'warning')
        return True
    except Exception as e:
        log(f"Quarantine failed: {str(e)}", 'error')
        return False