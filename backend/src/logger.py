import logging
import os
import sys
from logging.handlers import RotatingFileHandler#which prevents your log file from getting too large during local testing.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, 'app.log')

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    
    # Avoid duplicate handlers if get_logger is called multiple times
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # Professional format: Timestamp - Module Name - Level - [File:Line] - Message
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )
        
        # File Handler (5MB per file, keeps 3 backups)
        file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
        file_handler.setFormatter(formatter)
        
        # Stream Handler (to see logs in your terminal/cmd)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        
    return logger