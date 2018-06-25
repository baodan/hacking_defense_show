from config import Config
import platform
import logging
import sys

LEVEL = {
    'info': logging.INFO,
    'debug': logging.DEBUG,
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'notset': logging.NOTSET,
    'critical': logging.CRITICAL,
}
log_file = Config.LOG_FILE if getattr(Config, 'LOG_FILE', False) else '/var/log/assets/assets.log'
log_level = LEVEL[Config.LOG_LEVEL] if getattr(Config, 'LOG_LEVEL', False) in LEVEL else LEVEL['warning']
# windows上ConcurrentRotatingFileHandler这个handler会有导致程序卡死，linux上无问题
# 暂时采用这种方法解决windows上因卡死导致的调试不方便问题
if str(platform.system()) == "Windows":
    from logging.handlers import RotatingFileHandler as LogHandler
    from logging import StreamHandler
    server_log = StreamHandler()
    server_log.setLevel(logging.DEBUG)
else:
    from cloghandler import ConcurrentRotatingFileHandler as LogHandler
    sys_log = LogHandler(log_file, "a", 20*1024*1024, 10, encoding='UTF-8')
    
    server_log = LogHandler(log_file, "a", 20*1024*1024, 10, encoding='UTF-8')
    server_log.setLevel(log_level)
    server_log.setFormatter(logging.Formatter(
        """%(asctime)s -%(levelname)s in [%(pathname)s:%(lineno)d]:\n%(message)s"""
    ))
    
    error_log = LogHandler(log_file, "a", 20*1024*1024, 10, encoding='UTF-8')
    error_log.setLevel(logging.ERROR)
    error_log.setFormatter(logging.Formatter(
            '%(asctime)s -%(levelname)s in [%(pathname)s:%(lineno)d]: %(message)s'))
    
    logger = logging.getLogger('werkzeug')
    logger.addHandler(sys_log)

