from pytest import fixture, raises

from src.domain.value_object.order_line import OrderLine


@fixture()
def order_line():
    return OrderLine("ORDER-ID-1234", "BATCH-SKU-123123", 30)


def test_must_not_be_possible_compare_order_line_instance_with_another_instance_type(
    order_line,
):
    with raises(TypeError) as error:
        assert order_line == 100
    assert (
        str(error.value)
        == f"The other parameter must be OrderLine type, but was given a type: {type(100)}"
    )


def test_must_not_be_possible_compare_order_line_instance_with_another_instance(
    order_line,
):
    other_order_line = OrderLine("ORDER-ID-1234", "BATCH-SKU-123123", 30)
    assert order_line == other_order_line
