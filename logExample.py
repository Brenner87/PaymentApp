import logging
import logging.config



class ExampleLogger1(object):

    def __init__(self, path, name=None, (sad)
        self.name = name or __name__
        self.path = path  # Add here path verification and default scenario logic

    def get_logger(self):
        logging.config.fileConfig(self.path, disable_existing_loggers=False)
        logger = logging.getLogger(self.name)
        return logger


class ExampleLogger2(object):
    def __init__(self, path, name=None, (sad)
        self.name = name or __name__
        self.path = path  # Add here path verification and default scenario logic
        logging.config.fileConfig(self.path, disable_existing_loggers=False)
        self.logger = logging.getLogger(self.name)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)


if __name__ == '__main__':
    log = ExampleLogger1('your_path_to_conf').get_logger()
    log.debug('debug')
    log.info('info')
    log.warning('warning')
    log.error('error')
    log2 = ExampleLogger2('your_path_to_conf')
    log2.debug('debug')
    log2.info('info')
    log2.warning('warning')
    log2.error('error')