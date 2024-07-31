import logging
from concurrent.futures import ThreadPoolExecutor
import asyncio

logger = logging.getLogger('django')

executor = ThreadPoolExecutor(max_workers=5)

def async_log(message, level='info'):
    if level == 'info':
        executor.submit(logger.info, message)
    elif level == 'error':
        executor.submit(logger.error, message)
    elif level == 'warning':
        executor.submit(logger.warning, message)
    elif level == 'debug':
        executor.submit(logger.debug, message)
    elif level == 'critical':
        executor.submit(logger.critical, message)
