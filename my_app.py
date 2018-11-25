import logging
import logging.config
import json
import os

log_level='DEBUG'
handlers=['console', 'logFile']

myJson=open('log_config.json')

dictLogConfig=json.loads(myJson.read())

dictLogConfig["loggers"]["myApp"]["handlers"]=[handlers[0]]
dictLogConfig["loggers"]["myApp"]["level"]='INFO'

logging.config.dictConfig(dictLogConfig)
log=logging.getLogger("myApp")


# 'application' code
# log.debug('debug message')
# log.info('info message')
# log.warn('warn message')
# log.error('error message')
# log.critical('critical message')
# log.warn('something is going wrong')
# jv=json.dumps(dictLogConfig)
# print(jv)

class logConfig:
    def __init__(self,logLevel='INFO', logConFile='log_config.json', logOut='console'):
        handlers = {'console': ['console'], 'logFile': ['logFile'], 'all': ['condole', 'logFile']}
        posLogLvls=['DEBUG', 'INFO', 'WARN', 'CRITICAL', 'FATAL']
        dictLogConfig=self.readJsonConf(logConFile)
        dictLogConfig["loggers"][__name__] = dictLogConfig["loggers"].pop("myApp")
        if logLevel not in posLogLvls:
            print('Possible log levels are: {}, {}, {}, {}, {}.\n\
                  Your {} level is unavailable.\n\
                  Setting log level to default value'.format(*posLogLvls,logLevel))
        else:
            dictLogConfig["loggers"][__name__]["level"] = logLevel
        if logOut not in handlers.keys():
            print('Log output can be only {}, {} or {}. Setting default value'.format(*handlers.keys()))
        else:
            dictLogConfig["loggers"][__name__]["handlers"] = handlers[logOut]

        logging.config.dictConfig(dictLogConfig)
        self.logger=logging.getLogger(__name__)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def fatal(self, msg):
        self.logger.fatal(msg)

    def readJsonConf(self, logConFile):
        if os.path.exists(logConFile):
            with open(logConFile) as fh:
                try:
                    dictLogConfig = json.loads(fh.read())
                except Exception as err:
                    print ('Was not able to parse json log config: {}'.format(err))
                    return None
                return dictLogConfig

print ('='*20)
log1=logConfig('DEBUG')
log1.debug('debug message')
log1.info('info messages')
log1.warning('warn message')
log1.error('error message')
log1.fatal('fatal message')

