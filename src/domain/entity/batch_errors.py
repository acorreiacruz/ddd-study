class SkuDoesNotMatchError(Exception):
    def __init__(self):
        super().__init__("The batch sku does not match with the order line sku")


class InsufficientAvailableQuantityError(Exception):
    def __init__(self):
        super().__init__("Insufficient available quantity to allocation")


class OrderLineAlreadyAllocatedError(Exception):
    def __init__(self, order_id: str):
        super().__init__(
            f"Already exists a order line allocated with this order_id: {order_id}"
        )


class OrderLineNotAllocatedError(Exception):
    def __init__(self, order_id: str):
        super().__init__(
            f"There is no order line allocated with this order_id: {order_id}"
        )
