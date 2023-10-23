import os
from dotenv import load_dotenv
from logging import config as logging_config

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

load_dotenv()

PROJECT_NAME = os.getenv('PROJECT_NAME', 'Vodomat API')
API_VERSION = os.getenv('API_VERSION', '1.0.0')
DESCRIPTION = """
### <span style='color:#0f3057'>System for remote monitoring and control of vending water machine.</span>
"""
CONTACT = {
    'name': 'Evgeniy Bugaiov',
    'email': 'evgeniy.bugaiov@gmail.com'
}

SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DATABASE_SERVER_HOST = os.getenv('DATABASE_SERVER_HOST', '127.0.0.1')
DATABASE_SERVER_PORT = os.getenv('DATABASE_SERVER_PORT', 3306)
DATABASE_SERVER_NAME = os.getenv('DATABASE_SERVER_NAME', 'test')
DATABASE_SERVER_USER = os.getenv('DATABASE_SERVER_USER', 'root')
DATABASE_SERVER_PASSWORD = os.getenv('DATABASE_SERVER_PASSWORD', 'password')

DATABASE_APP_HOST = os.getenv('DATABASE_APP_HOST', '127.0.0.1')
DATABASE_APP_PORT = os.getenv('DATABASE_APP_PORT', 5432)
DATABASE_APP_NAME = os.getenv('DATABASE_APP_NAME', 'vodomat_pay')
DATABASE_APP_USER = os.getenv('DATABASE_APP_USER', 'vodomat')
DATABASE_APP_PASSWORD = os.getenv('DATABASE_APP_PASSWORD', 'vodomat')

PAYMENT_GATEWAY_URL=os.getenv('PAYMENT_GATEWAY_URL')
PAYMENT_GATEWAY_LOGIN=os.getenv('PAYMENT_GATEWAY_LOGIN')
PAYMENT_GATEWAY_PASSWORD=os.getenv('PAYMENT_GATEWAY_PASSWORD')
PAYMENT_GATEWAY_PAYEE_ID=os.getenv('PAYMENT_GATEWAY_PAYEE_ID')

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
