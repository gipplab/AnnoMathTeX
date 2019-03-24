#Limit of the number of recommendations that are returned
recommendations_limit = 10


#path to logging config file
from os import getcwd
from os.path import join
logging_config_path = join(getcwd(), 'logging_config.json')

import logging
from logging.config import dictConfig

logging_config = dict(
    version = 1,
    formatters = {
        'f': {'format':
              '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
        },
    handlers = {
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG}
        },
    root = {
        'handlers': ['h'],
        'level': logging.DEBUG,
        },
)

#dictConfig(logging_config)

#__LOGGER__ = logging.getLogger()

#logger = logging.getLogger()
#logger.debug('often makes a very good meal of %s', 'visiting tourists')
