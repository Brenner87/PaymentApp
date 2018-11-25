from logger import logConfig

log=logConfig(name=__name__).get_logger()


log.fatal('this is fatal message from {}'.format(__name__))