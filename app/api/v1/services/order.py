from functools import lru_cache
from datetime import date, datetime
from fastapi import Depends, HTTPException
import pandas as pd
from typing import Optional

from .base import BaseService

from .order_pay_gate import OrderPayGateService, get_order_pay_gate_service
from .order_app import OrderAppService, get_order_app_service
from .order_server import OrderServerService, get_order_server_service

from models import Order, PurchaseStatus, DepositStatus


class OrderService(BaseService):
    def __init__(self,
                 order_pay_gate_service: OrderPayGateService,
                 order_app_service: OrderAppService,
                 order_server_service: OrderServerService):
        self.order_pay_gate_service = order_pay_gate_service
        self.order_app_service = order_app_service
        self.order_server_service = order_server_service

    async def _fill_empty_order_app_fields(self, df: pd.DataFrame) -> None:
        for index, row in df.iterrows():
            if pd.isna(row['created_at']):
                order_app_item = await self.order_app_service.get_item_by_id(row['order_app_id'])
                df.at[index, 'created_at'] = order_app_item.created_at
                df.at[index, 'order_app_status'] = order_app_item.order_app_status
                df.at[index, 'order_app_money'] = order_app_item.order_app_money
                df.at[index, 'avtomat_number'] = order_app_item.avtomat_number
                df.at[index, 'address'] = order_app_item.address

    async def get_all_by_period(self, start_period: str, end_period: str,
                                order_attribute: str, order_direction: str) -> list[Order]:
        # Fetch data and validate
        pay_gate_data = await self.order_pay_gate_service.get_all_by_period(start_period, end_period)
        server_data = await self.order_server_service.get_all_by_period(start_period, end_period)
        app_data = await self.order_app_service.get_all_by_period(start_period, end_period)

        # Convert to DataFrame
        order_pay_gate_df = pd.DataFrame(item.model_dump() for item in pay_gate_data)
        order_server_df = pd.DataFrame(item.model_dump() for item in server_data)
        order_app_df = pd.DataFrame(item.model_dump() for item in app_data)

        # Merge DataFrames
        try:
            merged_df = order_pay_gate_df \
                .merge(order_server_df, on='order_pay_gate_id', how='left', suffixes=('', '_server')) \
                .merge(order_app_df, on='order_app_id', how='left', suffixes=('', '_app'))
        except KeyError as e:
            raise ValueError(f"Merge error: {e}")

        # Handle missing data
        await self._fill_empty_order_app_fields(merged_df)

        # Convert to list of `Order`
        try:
            data = [Order(**item) for item in merged_df.to_dict(orient='records')]
        except Exception as e:
            raise ValueError(f"Error converting DataFrame to Order objects: {e}")

        # Sort data
        ordered_data = self.get_ordered_data(data, order_attribute, order_direction)
        return ordered_data

    async def get_item_by_id(self, pay_gate_id: int) -> Order:
        pay_gate_item = await self.order_pay_gate_service.get_item_by_id(pay_gate_id)
        app_item = await self.order_app_service.get_item_by_id(pay_gate_item.order_app_id)
        server_item = await self.order_server_service.get_item_by_id(app_item.order_server_id)
        return Order(**{**dict(pay_gate_item), **dict(app_item), **dict(server_item)})
    
    async def update_item_set_done(self, pay_gate_id: int) -> Order:
        done_server_item = await self.order_server_service.update_item('payment_gateway_id', pay_gate_id, {'status': 1})
        done_app_item = await self.order_app_service.update_item('payment_gateway_id', pay_gate_id, {'status': 2})
        pay_gate_item = await self.order_pay_gate_service.get_item_by_id(pay_gate_id)
        return Order(**{**dict(pay_gate_item), **dict(done_app_item), **dict(done_server_item)})

    async def refund_item(self, pay_gate_id: int) -> Optional[Order]:
        """
        Process a refund for the given payment gateway ID and return the consolidated Order object.

        Args:
            pay_gate_id (str): The payment gateway ID to refund.

        Returns:
            Optional[Order]: A consolidated Order object on success, or None if the refund fails.
        """
        app_order = await self.order_app_service.get_item_by_pay_gate_id(pay_gate_id)
        refund_method = 'reject' if app_order.created_at.date() == date.today() else 'return'
        message = f'{pay_gate_id} Returned manually at {datetime.now()}'

        try:
            # Check, that Purchase could be refunded according to its status.
            if app_order.order_app_status not in (PurchaseStatus.CREATED, PurchaseStatus.FAIL_AND_NOT_REFUND):
                raise HTTPException(status_code=400,
                                    detail=f'Purchase({app_order.order_app_id}) with this status cannot be refunded.'
                                    )
            # Process the refund in the payment gateway. Raise an HTTPException if the order was not refunded.
            pay_gate_order = await self.order_pay_gate_service.refund_item(
                pay_gate_id,
                app_order.order_app_money,
                refund_method,
                message,
            )

            # Update related purchase and deposit on successful refund.
            app_order = await self.order_app_service.update_item(
                'payment_gateway_id', pay_gate_id, {'status': PurchaseStatus.REFUND}
            )
            server_order = await self.order_server_service.update_item(
                'payment_gateway_id', pay_gate_id, {'status': DepositStatus.FAILED}
            )

            return Order(**{**dict(pay_gate_order), **dict(app_order), **dict(server_order)})

        except HTTPException as e:
            # Handle refund failure by updating the purchase status.
            if e.status_code == 400:
                await self.order_app_service.update_item(
                    'payment_gateway_id', pay_gate_id, {'status': PurchaseStatus.FAIL_AND_NOT_REFUND}
                )
            return None


@lru_cache
def get_order_service(order_pay_gate_service: OrderPayGateService = Depends(get_order_pay_gate_service),
                      order_app_service: OrderAppService = Depends(get_order_app_service),
                      order_server_service: OrderServerService = Depends(get_order_server_service)) -> OrderService:
    return OrderService(order_pay_gate_service, order_app_service, order_server_service)
