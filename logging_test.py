import logging
log_format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s'
log=logging.getLogger(__name__)
log.setLevel(logging.INFO)
formatter=logging.Formatter(log_format)
#file_handler=logging.FileHandler('PaymetnApp.log')
#file_handler.setFormatter(formatter)
stream_handler=logging.StreamHandler()
stream_handler.setFormatter(formatter)
#logger.addHandler(file_handler)
log.addHandler(stream_handler)


log.info('hi There')
log.fatal('we are doomed')
log.critical('we are near to be doomed')



