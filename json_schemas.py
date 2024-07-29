# if key == tag
# check list of schemas
# if it matches one of them, rename the key to schema title.
# otherwise do nothing
custom_transforms_dict = {
    "CostList": [
        {
            "$schema": "https://json-schema.org/draft-07/schema#",
            "$id": "http://test.com/costlist-cost-schema",
            "title": "Cost",
            "properties": {"CostType": {"type": "string"}, "Value": {"type": "number"}},
            "additionalProperties": True,
        },
        {
            "$schema": "https://json-schema.org/draft-07/schema#",
            "$id": "http://test.com/costlist-quantity-schema",
            "title": "Quantity",
            "properties": {"Units": {"type": "string"}, "Value": {"type": "number"}},
            "additionalProperties": False,
        },
    ]
}