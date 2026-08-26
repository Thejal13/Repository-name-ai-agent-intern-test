import json
import re
from pathlib import Path

SAFE_FIELDS = {
    "order_id",
    "membership_tier",
    "placed_at",
    "status",
    "status_updated_at",
    "shipped_at",
    "delivered_at",
    "carrier",
    "tracking_number",
    "estimated_delivery",
    "customer_safe_message",
}


class OrderLookup:
    def __init__(self, file_path="data/orders.json"):
        self.file_path = Path(file_path)

        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.snapshot_at = data["snapshot_at"]

        self.orders = {
            order["order_id"]: order
            for order in data["orders"]
        }

    def normalize_order_id(self, order_id):
        if not isinstance(order_id, str):
            return None

        order_id = order_id.strip().upper()
        order_id = re.sub(r"^[^\w-]+|[^\w-]+$", "", order_id)

        return order_id

    def lookup(self, order_id):
        normalized_id = self.normalize_order_id(order_id)

        if not normalized_id:
            return {
                "found": False,
                "error": "A valid order ID is required."
            }

        order = self.orders.get(normalized_id)

        if not order:
            return {
                "found": False,
                "error": "Order ID not found."
            }

        result = {
            "found": True,
            "order_id": order["order_id"],
            "status": order["status"],
        }

        for field in SAFE_FIELDS:
            if field in {"order_id", "status"}:
                continue

            value = order.get(field)

            if value is not None:
                result[field] = value

        result["items"] = [
            {
                "name": item.get("name"),
                "quantity": item.get("quantity"),
                "final_sale": item.get("final_sale"),
            }
            for item in order.get("items", [])
        ]

        if order["status"] in {"cancelled", "returned"}:
            result.pop("carrier", None)
            result.pop("tracking_number", None)
            result.pop("estimated_delivery", None)
            result.pop("shipped_at", None)
            result.pop("delivered_at", None)

        if (
            order["status"] == "shipped"
            and order.get("estimated_delivery") is None
        ):
            result["estimated_delivery"] = None

        if order["status"] == "exception":
            result["human_handoff"] = True

        return result
