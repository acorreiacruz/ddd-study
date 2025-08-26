from datetime import date
from typing import Any, Dict, List
from uuid import UUID

from pydantic import BaseModel

from src.domain.entity.batch_errors import (
    InsufficientAvailableQuantityError,
    OrderLineAlreadyAllocatedError,
    OrderLineNotAllocatedError,
    SkuDoesNotMatchError,
)
from src.domain.value_object.order_line import OrderLine


class Batch(BaseModel):
    reference: str
    sku: str
    quantity: int
    eta: date | None
    already_allocated: Dict[str, OrderLine]

    def __init__(
        self,
        reference: str,
        sku: str,
        quantity: int,
        eta: date | None = None,
        already_allocated: Dict[str, OrderLine] = {},
        **kwargs,
    ):
        super().__init__(
            reference=reference,
            sku=sku,
            quantity=quantity,
            eta=eta,
            already_allocated=already_allocated,
            **kwargs,
        )

    def allocate(self, order_line: OrderLine) -> None:
        if self.sku != order_line.sku:
            raise SkuDoesNotMatchError()
        elif self.quantity < order_line.quantity:
            raise InsufficientAvailableQuantityError()
        elif order_line.order_id in self.already_allocated:
            raise OrderLineAlreadyAllocatedError(order_line.order_id)
        self.quantity -= order_line.quantity
        self.already_allocated[order_line.order_id] = order_line

    def deallocate(self, order_line: OrderLine) -> None:
        if order_line.sku != self.sku:
            raise SkuDoesNotMatchError()
        elif order_line.order_id not in self.already_allocated:
            raise OrderLineNotAllocatedError(order_line.order_id)
        self.quantity += order_line.quantity
        self.already_allocated[order_line.order_id]

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Batch):
            raise TypeError(
                f"The other parameter must be of type Batch, but was given a type:{type(other)}"
            )
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Batch):
            raise TypeError(
                f"The other parameter must be of type Batch, but was given a type:{type(other)}"
            )
        return self.eta < other.eta
