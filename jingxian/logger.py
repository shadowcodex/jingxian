# logger.py
import logging

# Configure basic logging format (e.g., include timestamp and level)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_logger(name):
    """Get a logger with the given name."""
    return logging.getLogger(name)
