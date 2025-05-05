import logging
from datetime import datetime
import sys

class ColorFormatter(logging.Formatter):
    COLORS = {
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'INFO': '\033[94m',
        'ENDC': '\033[0m'
    }

    def format(self, record):
        message = super().format(record)
        if record.levelname in self.COLORS:
            message = f"{self.COLORS[record.levelname]}{message}{self.COLORS['ENDC']}"
        return message

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # File handler (full logs)
    file_handler = logging.FileHandler(
        'telperion_scan.log', 
        encoding='utf-8',
        mode='w'
    )
    file_handler.setLevel(logging.INFO)

    # Console handler (real-time updates)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Changed from WARNING

    # Formatting
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%H:%M:%S'
    )
    color_formatter = ColorFormatter(
        '[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(color_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

def log(message, level='info'):
    logger = logging.getLogger()
    if level.lower() == 'warning':
        logger.warning(message)
    elif level.lower() == 'error':
        logger.error(message)
    else:
        logger.info(message)
    logger.handlers[0].flush()  # Force immediate output