import os
from dotenv import load_dotenv
from logging import config as logging_config

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

load_dotenv()

PROJECT_NAME = os.getenv('PROJECT_NAME', 'Vodomat API')
API_VERSION = os.getenv('API_VERSION', '1.0.0')

SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DATABASE_SERVER_HOST = os.getenv('DATABASE_SERVER_HOST', '127.0.0.1')
DATABASE_SERVER_PORT = os.getenv('DATABASE_SERVER_PORT', 3306)
DATABASE_SERVER_NAME = os.getenv('DATABASE_SERVER_NAME', 'test')
DATABASE_SERVER_USER = os.getenv('DATABASE_SERVER_USER', 'root')
DATABASE_SERVER_PASSWORD = os.getenv('DATABASE_SERVER_PASSWORD', 'password')

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
