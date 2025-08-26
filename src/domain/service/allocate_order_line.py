from typing import List

from src.domain.entity.batch import Batch
from src.domain.value_object.order_line import OrderLine


def allocate_order_line(order_line: OrderLine, batchs: List[Batch] = []) -> str:
    batch: Batch | None = next(
        (batch for batch in sorted(batchs) if batch.sku == order_line.sku),
        None,
    )
    batch.allocate(order_line)
    return batch.reference


class BatchNotFoundError(Exception):
    def __init__(self, sku: str):
        super().__init__(f"Batch not found. There is no batch with sku: {sku}")
