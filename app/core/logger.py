import os
import sys
import logging

from .core.config import config


cfg = config('log')

loggers = {}

def get_logger(filename):
    global loggers

    if filename in loggers:
        logger = loggers[filename]
    else:
        if not os.path.exists(cfg['path']):
            os.mkdir(cfg['path'])
        filepath = os.path.join(cfg['path'], filename + '.log')
        logger = logging.getLogger()
        logger.setLevel(cfg['level'])
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        if cfg['stdout']:
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setLevel(cfg['level'])
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

        file_handler = logging.handlers.TimedRotatingFileHandler(
            filepath, when="d", interval=1, backupCount=10, encoding='utf-8')
        file_handler.setLevel(cfg['level'])
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        loggers[filename] = logger
    return logger
