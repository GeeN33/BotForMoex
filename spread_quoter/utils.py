from typing import List, Optional

from spread_quoter.modelsPy import OrderDetail


def filter_order(orders: List[OrderDetail],
                 client_order_id:str,
                 limit_price:float,
                 quantity:float) -> ( List[OrderDetail],  Optional[OrderDetail]):

    for i, order in enumerate(orders):
        if order.order.client_order_id == client_order_id:
            if order.order.limit_price.value == limit_price  and order.order.type == 'ORDER_TYPE_LIMIT':
                if order.status == 'ORDER_STATUS_NEW' and order.order.quantity.value == quantity:
                    return orders, orders.pop(i)
                if order.status == 'ORDER_STATUS_PARTIALLY_FILLED' and order.order.quantity.value == quantity:
                    return orders, orders.pop(i)

    return orders,  None


def check_order(orders: List[OrderDetail], order_id:str) -> bool:

    for order in orders:
        if order.order_id == order_id: return True

    return False