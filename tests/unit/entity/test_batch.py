from datetime import date
from uuid import uuid4

from pytest import fixture, raises

from src.domain.entity.batch import Batch
from src.domain.entity.batch_errors import (
    InsufficientAvailableQuantityError,
    OrderLineAlreadyAllocatedError,
    OrderLineNotAllocatedError,
    SkuDoesNotMatchError,
)
from src.domain.value_object.order_line import OrderLine


@fixture()
def batch():
    return Batch("BOSS-ARMCHAIR", "BATCH-SKU-123123", 30, date.today())


def test_must_allocate_a_order_line(batch):
    order_line: OrderLine = OrderLine("some_reference", "BATCH-SKU-123123", 10)
    assert batch.quantity == 30
    batch.allocate(order_line)
    assert batch.quantity == 20


def test_must_not_allocate_a_order_line_with_different_sku(batch):
    order_line: OrderLine = OrderLine("some_reference", "BATCH-SKU-1231", 10)
    with raises(SkuDoesNotMatchError) as error:
        batch.allocate(order_line)
    assert str(error.value) == "The batch sku does not match with the order line sku"


def test_must_not_allocate_a_order_line_when_insufficient_available_quantity(batch):
    order_line: OrderLine = OrderLine("some_reference", "BATCH-SKU-123123", 100)
    with raises(InsufficientAvailableQuantityError) as error:
        batch.allocate(order_line)
    assert str(error.value) == "Insufficient available quantity to allocation"


def test_must_not_allocate_the_same_order_line_twice_in_a_row(
    batch,
):
    order_line: OrderLine = OrderLine("some_reference", "BATCH-SKU-123123", 10)
    batch.allocate(order_line)
    with raises(OrderLineAlreadyAllocatedError) as error:
        batch.allocate(order_line)
    assert (
        str(error.value)
        == f"Already exists a order line allocated with this order_id: {order_line.order_id}"
    )


def test_must_deallocate_a_allocated_order_line(
    batch,
):
    order_line: OrderLine = OrderLine("some_reference", "BATCH-SKU-123123", 10)
    batch.allocate(order_line)
    assert batch.quantity == 20
    batch.deallocate(order_line)
    assert batch.quantity == 30


def test_must_not_deallocate_a_order_line_not_allocated(
    batch,
):
    order_line: OrderLine = OrderLine("some_reference", "BATCH-SKU-123123", 10)
    with raises(OrderLineNotAllocatedError) as error:
        batch.deallocate(order_line)
    assert (
        str(error.value)
        == f"There is no order line allocated with this order_id: {order_line.order_id}"
    )


def test_must_not_deallocate_a_order_line_with_different_sku(
    batch,
):
    order_line: OrderLine = OrderLine("some_reference", "BATCH-SKU-1231", 10)
    with raises(SkuDoesNotMatchError) as error:
        batch.deallocate(order_line)
    assert str(error.value) == "The batch sku does not match with the order line sku"


def test_must_be_possible_compare_batchs_by_beta(
    batch,
):
    older_batch = Batch("BOSS-ARMCHAIR", "BATCH-SKU-123123", 30, date(2020, 10, 20))
    assert batch > older_batch
    assert older_batch < batch


def test_must_not_be_possible_compare_batch_instance_is_greater_than_with_another_instance_type(
    batch,
):
    with raises(TypeError) as error:
        assert batch > 100
    assert (
        str(error.value)
        == f"The other parameter must be of type Batch, but was given a type:{type(100)}"
    )

def test_must_not_be_possible_compare_batch_instance_is_less_than_with_another_instance_type(
    batch,
):
    with raises(TypeError) as error:
        assert batch < 100
    assert (
        str(error.value)
        == f"The other parameter must be of type Batch, but was given a type:{type(100)}"
    )
