from ninja import Field, Schema


class OrderCreatePayloadSchema(Schema):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class OrderSchema(Schema):
    order_id: int
    product_id: int
    quantity: int
