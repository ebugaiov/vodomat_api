from functools import lru_cache

from fastapi import Depends

import pandas as pd

from .base import BaseService

from .order_pay_gate import OrderPayGateService, get_order_pay_gate_service
from .order_app import OrderAppService, get_order_app_service
from .order_server import OrderServerService, get_order_server_service

from api.v1.models import Order


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
        order_pay_gate_df = pd.DataFrame(item.model_dump() for item in
                                         (await self.order_pay_gate_service.get_all_by_period(start_period,
                                                                                              end_period)))
        order_server_df = pd.DataFrame(item.model_dump() for item in
                                       (await self.order_server_service.get_all_by_period(start_period, end_period)))
        order_app_df = pd.DataFrame(item.model_dump() for item in
                                    (await self.order_app_service.get_all_by_period(start_period, end_period)))
        merged_df = order_pay_gate_df \
            .merge(order_server_df, on='order_pay_gate_id', how='left', suffixes=('', '_')) \
            .merge(order_app_df, on='order_app_id', how='left', suffixes=('', '_'))
        await self._fill_empty_order_app_fields(merged_df)
        data = [Order(**item) for item in merged_df.to_dict(orient='records')]
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


@lru_cache
def get_order_service(order_pay_gate_service: OrderPayGateService = Depends(get_order_pay_gate_service),
                      order_app_service: OrderAppService = Depends(get_order_app_service),
                      order_server_service: OrderServerService = Depends(get_order_server_service)) -> OrderService:
    return OrderService(order_pay_gate_service, order_app_service, order_server_service)
