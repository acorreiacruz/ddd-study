from datetime import date
from typing import List

from src.domain.entity.batch import Batch
from src.domain.service import allocate_order_line
from src.domain.value_object.order_line import OrderLine


def test_must_prioritize_the_batch_in_stock_in_relation_to_what_will_arrive():
    batch_in_stock: Batch = Batch("REFERENCE-12349", "BATCH-SKU-1", 100)
    batch_will_arrive: Batch = Batch(
        "REFERENCE-12349", "BATCH-SKU-1", 100, date(2025, 10, 2)
    )
    batchs: List[Batch] = [
        batch_will_arrive,
        batch_in_stock,
    ]
    order_line = OrderLine("ORDER-ID-12134", "BATCH-SKU-1", 30)
    allocate_order_line(order_line=order_line, batchs=batchs)
    assert batch_in_stock.quantity == 70
