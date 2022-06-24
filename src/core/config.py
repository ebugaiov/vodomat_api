import os
from dotenv import load_dotenv
from logging import config as logging_config

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

load_dotenv()

PROJECT_NAME = os.getenv('PROJECT_NAME', 'Vodomat API')
API_VERSION = os.getenv('API_VERSION', '3.0.0')

SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DATABASE_HOST = os.getenv('DATABASE_HOST', '127.0.0.1')
DATABASE_PORT = os.getenv('DATABASE_PORT', 3306)
DATABASE_NAME = os.getenv('DATABASE_NAME', 'test')
DATABASE_USER = os.getenv('DATABASE_USER', 'root')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'password')

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
