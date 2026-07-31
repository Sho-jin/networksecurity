import os
from datetime import datetime
import logging

LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

log_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

os.makedirs(os.path.dirname(log_path), exist_ok=True)

log_file_path = os.path.join( log_path, LOG_FILE)

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)