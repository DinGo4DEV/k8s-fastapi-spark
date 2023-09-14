import sys
from loguru import logger
from . import logging

logging.init_logging()
fmt = "<g>{time}</g> | <lvl>{level}</lvl> | [ <blue>{name}</> ] <cyan>{file}</cyan>:<cyan>{line}</cyan> - <lvl>{message}</>"
logger.remove()  # Remove all handlers added so far, including the default one.
logger.add(sys.stderr, level="WARNING",format=fmt)
logger.add(sys.stdout, level="INFO",format=fmt)

logger.add("console.log",level="INFO", format=fmt,rotation="500 MB")