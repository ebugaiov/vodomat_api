from functools import lru_cache

import aiohttp

from fastapi import HTTPException, status

from core import config

from .base import BaseService
from models import OrderPayGate


class OrderPayGateService(BaseService):

    credentials = {
        'login': config.PAYMENT_GATEWAY_LOGIN,
        'password': config.PAYMENT_GATEWAY_PASSWORD,
        'payeeId': config.PAYMENT_GATEWAY_PAYEE_ID
    }

    async def get_all_by_period(self, start_period: str, end_period: str) -> list[OrderPayGate]:
        request_data = {
            'method': 'result',
            'params': {
                'data': {
                    **self.credentials,
                    'startDate': '.'.join(start_period.split('-')[::-1]),
                    'endDate': '.'.join(end_period.split('-')[::-1])
                }
            }
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(config.PAYMENT_GATEWAY_URL, json=request_data) as resp:
                if resp.status == 200:
                    resp_data = await resp.json()
                    return [OrderPayGate.model_validate(item) for item in resp_data]
                else:
                    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                        detail='Portmone Service is down')

    async def get_item_by_id(self, pk: int) -> OrderPayGate:
        request_data = {
            'method': 'result',
            'params': {
                'data': {
                    **self.credentials,
                    'shopbillId': pk
                }
            }
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(config.PAYMENT_GATEWAY_URL, json=request_data) as resp:
                if resp.status == 200:
                    resp_data = await resp.json()
                    if not isinstance(resp_data, list):
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Portmone Item not found')
                    return OrderPayGate.model_validate(resp_data[0])
                else:
                    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                        detail='Portmone Service is down')


@lru_cache
def get_order_pay_gate_service() -> OrderPayGateService:
    return OrderPayGateService()
