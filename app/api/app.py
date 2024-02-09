from fastapi import FastAPI
from pyaml_env import parse_config
import copy

import logging

logger = None
logger_handler = None

class CustomLogger(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return '[ASKBACKEND-%s-%s] %s' % (self.extra['document_type'],self.extra['id'], msg), kwargs


def logger_create():
    global logger
    global logger_handler
    if logger is not None:    # already created? return existing!
        return logger

    # create a logger for the app
    logger = logging.getLogger(__file__)

    # create console handler and set level to debug
    logger_handler = logging.StreamHandler()
    logger_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '[%(asctime)s,%(levelname)s,%(funcName)s]: %(message)s',
        datefmt='%y/%m/%d %H:%M:%S',
    )
    # add formatter to logger_handler
    logger_handler.setFormatter(formatter)
    # add logger_handler to logger
    logger.addHandler(logger_handler)
    return logger


def logger_destroy():
    global logger
    global logger_handler
    if logger is None:    # already created? return existing!
        return

    logger_handler.close()
    logger.removeHandler(logger_handler)
    logger = None
    logger_handler = None

    return logger


def app_create():
    from ..database.database import session_init
    from ..database.schema import engine_init
    from fastapi.middleware.cors import CORSMiddleware
    from os import environ

    global _app

    # read in description
    description_content = ""
    with open('app/README.md', 'rt') as f:
        description_content = f.read()

    # create app
    _app = FastAPI(description=description_content)

    # add middleware
    _app.add_middleware(CORSMiddleware,
    allow_origins=["http://localhost:80"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    # create logger
    _app.logger = logger_create()
    _app.logger.warning('created logger')


    # set config
    path_config = 'app/config/config.yaml'
  
    _app.logger.info(f'reading config from {path_config}')
    _all_config = parse_config(path_config)
    
    _app.config = copy.deepcopy(_all_config["general"])

    _app.logger.warning('set configuration: {}'.format(_app.config))

    # bind sql_session
    _app.sql_engine= engine_init(_app.config)
    if isinstance(_app.sql_engine, str):
        _app.logger.warning(f"error connecting to db, {_app.sql_engine}")
    _app.sql_session = session_init(_app.sql_engine)

    _app.logger.info('set configuration: {}'.format(_app.config))
    return _app