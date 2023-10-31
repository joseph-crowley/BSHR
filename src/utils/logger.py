import logging
import logging.config
import json
import os
from logging.handlers import RotatingFileHandler

# Set up logging directory and file
log_directory = "../logs"
log_file = "application.log"

# Create log directory if it doesn't exist
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Define a JSON formatter
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "time": self.formatTime(record, self.datefmt)
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

# Configure logging
log_config = {
    "version": 1,
    "formatters": {
        "json": {
            "()": JsonFormatter
        }, 
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(module)s - %(funcName)s - %(lineno)d"
        }
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "filename": f"{log_directory}/{log_file}",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "level": "DEBUG"
        }
    },
    "root": {
        "handlers": ["file"],
        "level": "DEBUG"
    }
}

logging.config.dictConfig(log_config)

# Export the logger
logger = logging.getLogger(__name__)
