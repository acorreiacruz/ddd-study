from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrderLine(BaseModel):
    order_id: str
    sku: str
    quantity: int
    model_config = ConfigDict(frozen=True)

    def __init__(
        self,
        order_id: str,
        sku: str,
        quantity: int,
        **kwargs,
    ):
        super().__init__(order_id=order_id, sku=sku, quantity=quantity, **kwargs)

    def __eq__(self, order_line) -> bool:
        if not isinstance(order_line, OrderLine):
            raise TypeError(f"The other parameter must be OrderLine type, but was given a type: {type(order_line)}")
        return self.sku == order_line.sku and self.quantity == order_line.quantity
