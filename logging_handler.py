import logging
from logging.handlers import RotatingFileHandler

class logging_handler:
    def startup(self, format_, path_, maxBytes_, backupCount_):
        try:
            log_formatter = logging.Formatter(format_)
            self.my_handler = RotatingFileHandler(path_, mode='a', maxBytes=maxBytes_, 
                                    backupCount=backupCount_, encoding=None, delay=0)
            self.my_handler.setFormatter(log_formatter)
            self.my_handler.setLevel(logging.INFO)

            self.stream_handler = logging.StreamHandler()
            self.stream_handler.setFormatter(log_formatter)
            self.stream_handler.setLevel(logging.INFO)
            return True
        except Exception as e:
            print(f'Logging Failed, Exception:{e}')
            return False
        
    def set_logger(self, logger_name):
        app_log = logging.getLogger(logger_name)
        app_log.setLevel(logging.INFO)

        app_log.addHandler(self.my_handler)
        app_log.addHandler(self.stream_handler)
        return app_log