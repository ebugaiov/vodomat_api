from functools import lru_cache
from typing import Optional
from datetime import datetime
from aiohttp import ClientSession
from fastapi import HTTPException, status

from core import config
from .base import BaseService
from models import OrderPayGate


class OrderPayGateService(BaseService):

    @property
    def credentials(self):
        return {
            'login': config.PAYMENT_GATEWAY_LOGIN,
            'password': config.PAYMENT_GATEWAY_PASSWORD,
            'payeeId': config.PAYMENT_GATEWAY_PAYEE_ID
        }

    @property
    def gateway_url(self):
        return config.PAYMENT_GATEWAY_URL

    async def _post_to_gateway(self, method: str, data: dict) -> dict:
        """
        Helper function to send a POST request to the payment gateway.

        Args:
            method (str): The API method to call.
            data (dict): Data to include in the request payload.

        Returns:
            dict: Parsed JSON response from the gateway.

        Raises:
            HTTPException: If the gateway is unavailable.
        """
        request_data = {
            'method': method,
            'params': {'data': {**self.credentials, **data}}
        }
        async with ClientSession() as session:
            async with session.post(self.gateway_url, json=request_data) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail='Portmone Service is down'
                    )

    async def get_all_by_period(self, start_period: str, end_period: str) -> list[OrderPayGate]:
        """
        Retrieve all records from the gateway within a specific period.

        Args:
            start_period (str): The start date in YYYY-MM-DD format.
            end_period (str): The end date in YYYY-MM-DD format.

        Returns:
            list[OrderPayGate]: A list of validated OrderPayGate objects.
        """
        formatted_data = {
            'startDate': '.'.join(start_period.split('-')[::-1]),
            'endDate': '.'.join(end_period.split('-')[::-1])
        }
        response_data = await self._post_to_gateway('result', formatted_data)
        return [OrderPayGate.model_validate(item) for item in response_data]

    async def get_item_by_id(self, pk: int) -> OrderPayGate:
        """
        Retrieve a specific record from the gateway by its ID.

        Args:
            pk (int): The primary key of the record.

        Returns:
            OrderPayGate: A validated OrderPayGate object.

        Raises:
            HTTPException: If the record is not found or the response format is incorrect.
        """
        response_data = await self._post_to_gateway('result', {'shopbillId': pk})

        if not isinstance(response_data, list) or not response_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Portmone Item not found'
            )

        return OrderPayGate.model_validate(response_data[0])

    async def refund(self, shop_bill_id: str,
                     amount: float,
                     method: str = 'return',
                     message: Optional[str] = None) -> bool:
        """
        Process a refund based on the provided method type.
        There are two types of refunds:
        1. reject: This refund must be processed on the same day and is faster than 'return'.
        2. return: This refund type is slower but can be processed at any time after the payment.

        Args:
            shop_bill_id (str): The ID of the shop bill to refund.
            amount (float): The amount to refund.
            method (str): The refund method ('return' or 'reject'). Defaults to 'return'.
            message (Optional[str]): An optional message for the refund.

        Returns:
            bool: True if the refund is successful, False otherwise.
        """
        message = f'Returned at {datetime.now()}' if message is None else message
        data = {
            'shopbillId': shop_bill_id,
            'returnAmount': amount,
            'message': message
        }
        response_data = await self._post_to_gateway(method, data)
        return response_data[0].get('status') in ('RETURN', 'REJECTED')


@lru_cache
def get_order_pay_gate_service() -> OrderPayGateService:
    return OrderPayGateService()
