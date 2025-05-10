"""logger.py.

This module configures the logging for the application.
"""

import logging
from contextvars import ContextVar

from automation.settings import LOG_FORMAT, LOG_LEVEL

# Context variable to job-id
job_id_var: ContextVar[str] = ContextVar("job_id", default="N/A")

class ContextJobIdFilter(logging.Filter):
    """Filter to add job-id to log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Add job-id to log records."""
        record.job_id = job_id_var.get()
        return True

def setup_logger(name: str) -> logging.Logger:
    """Configure a logger with the given name."""
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        handler.addFilter(ContextJobIdFilter())
        logger.addHandler(handler)
        logger.setLevel(LOG_LEVEL)
    return logger

# configure all main loggers
def configure_all_loggers() -> logging.Logger:
    """Configure all loggers for the application."""
    main_logger = setup_logger("app")

    # integrate with uvicorn loggers
    for uvicorn_logger in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        logger = logging.getLogger(uvicorn_logger)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        handler.addFilter(ContextJobIdFilter())
        logger.addHandler(handler)
        logger.setLevel(LOG_LEVEL)

    return main_logger

# initialize main logger
logger = configure_all_loggers()
