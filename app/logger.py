import logging
import logging.config
import json
import os

class logConfig:
    def __init__(self, name=None, logLevel='INFO', logConFile='log_config.json', logOut='console'):
        self.name=name or __name__
        self.logConFile=logConFile
        self.logOut=logOut
        self.logLevel=logLevel


    def get_logger(self,):
        handlers = {'console': ['console'], 'logFile': ['logFile'], 'all': ['condole', 'logFile']}
        posLogLvls = ['DEBUG', 'INFO', 'WARN', 'CRITICAL', 'FATAL']
        dictLogConfig = self.readJsonConf(self.logConFile)
        dictLogConfig["loggers"][self.name] = dictLogConfig["loggers"].pop("myApp")
        if self.logLevel not in posLogLvls:
            print('Possible log levels are: {}, {}, {}, {}, {}.\n\
                          Your {} level is unavailable.\n\
                          Setting log level to default value'.format(*posLogLvls, self.logLevel))
        else:
            dictLogConfig["loggers"][self.name]["level"] = self.logLevel
        if self.logOut not in handlers.keys():
            print('Log output can be only {}, {} or {}. Setting default value'.format(*handlers.keys()))
        else:
            dictLogConfig["loggers"][self.name]["handlers"] = handlers[self.logOut]

        logging.config.dictConfig(dictLogConfig)
        logger = logging.getLogger(self.name)
        return logger

    def readJsonConf(self, logConFile):
        if os.path.exists(logConFile):
            with open(logConFile) as fh:
                try:
                    dictLogConfig = json.loads(fh.read())
                except Exception as err:
                    print('Was not able to parse json log config: {}'.format(err))
                    return None
                return dictLogConfig

    # def debug(self, msg):
    #     self.logger.debug(msg)
    #
    # def info(self, msg):
    #     self.logger.info(msg)
    #
    # def warning(self, msg):
    #     self.logger.warning(msg)
    #
    # def error(self, msg):
    #     self.logger.error(msg)
    #
    # def fatal(self, msg):
    #     self.logger.fatal(msg)

