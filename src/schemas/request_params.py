from enum import Enum


class OrderByQueryParam(str, Enum):
    AVTOMAT_NUMBER = 'avtomat_number'
    ADDRESS = 'address'
    TIME = 'time'
    BILL_NOT_WORK = 'bill_not_work'
    COIN_NOT_WORK = 'coin_not_work'
    BILL_NOT_WORK_MONEY = 'bill_not_work_money'
    COIN_NOT_WORK_MONEY = 'coin_not_work_money'


class OrderDirectionQueryParam(str, Enum):
    ASCENDING = 'asc'
    DESCENDING = 'desc'
