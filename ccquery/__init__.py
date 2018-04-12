import sys
import logging

from . import error, utils, data, preprocessing, ngram

def define_logger(mod_name):
    """Default logging configuration"""

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(
        '%(levelname)s [%(asctime)s] [%(name)s] %(message)s'))

    logger = logging.getLogger(mod_name)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)
    return logger

def define_level(level=logging.WARN):
    """Change logging level"""
    LOGGER.setLevel(level)

LOGGER = define_logger(__name__)
