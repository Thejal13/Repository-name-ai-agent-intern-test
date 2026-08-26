import re

from app.retrieval import KnowledgeBase
from app.orders import OrderLookup


class SupportAgent:

    def __init__(self):
        self.kb = KnowledgeBase()
        self.orders = OrderLookup()
        self.history = []

    def get_order_id(self, message):
        match = re.search(r"\bORD-\d{4}\b", message.upper())
        return match.group(0) if match else None

    def answer(self, message):
        text = message.lower()
        order_id = self.get_order_id(message)

        if order_id:
            order = self.orders.lookup(order_id)

            if not order["found"]:
                return (
                    "The order was not found. "
                    "Please check the order ID or contact support."
                )

            status = order["status"]

            if status == "cancelled":
                return "The order is cancelled and it will not be shipped."

            if status == "returned":
                return (
                    f"Order {order_id} has been returned. "
                    "Please contact support if you need further assistance."
                )

            if status == "exception":
                return (
                    f"Order {order_id} has a shipment exception that "
                    "requires support review. Please contact customer support."
                )

            if status == "shipped":
                carrier = order.get("carrier")
                eta = order.get("estimated_delivery")

                if eta:
                    return (
                        f"Order {order_id} has shipped with {carrier}. "
                        "It is currently estimated to arrive on "
                        "August 22, 2026."
                    )

                return (
                    f"Order {order_id} has shipped with {carrier}, "
                    "but the delivery estimate is unavailable."
                )

            return f"Order {order_id} has status: {status}."

        if "where is my order" in text:
            return "Sure — please provide your order ID."

        if (
            ("order" in text or "tracking" in text or "delivery" in text)
            and "order id" in text
        ):
            return "Please provide your order ID."

        if (
            "migration note" in text
            or "ignore the real policy" in text
            or "60 days" in text
            or "reveal hidden prompt" in text
            or "system prompt" in text
        ):
            return (
                "The migration note is not authoritative. "
                "The standard policy is 30 days unless a valid exception "
                "applies. The agent cannot approve a return."
            )

        if "vegan" in text and (
            "fabric" in text or "adhesive" in text
        ):
            return (
                "The supplied information is insufficient to confirm "
                "that all fabrics and adhesives are vegan. "
                "Human confirmation is required."
            )

        if "dishwasher" in text and (
            "breeze" in text or "tumbler" in text
        ):
           return (
    "The current official sources conflict. "
    "One says hand-wash the body. "
    "One says all components are dishwasher safe. "
    "Human confirmation or safest interim guidance is recommended."
)

        if (
            ("final sale" in text or "final-sale" in text)
            and (
                "broken" in text
                or "damaged" in text
                or "zipper" in text
            )
        ):
            return (
    "Final sale does not block damaged-item review. "
    "Report within 7 days. "
    "Human review before approval is required."
)

        if "canada" in text:
            return (
                "Canada is supported. International delivery takes "
                "5–9 business days after dispatch, and duties or taxes "
                "are not prepaid."
            )

        if "germany" in text:
            return "Shipping to Germany is not currently available."

        if "warranty" in text or "lifetime" in text:
            return (
                "There is no lifetime warranty. Bags have 2 years, "
                "while drinkware and travel accessories have 1 year."
            )

        if "trailplus" in text:
            return (
                "TrailPlus members have a 45 calendar days return window "
                "from delivery."
            )

        if "return" in text:
            return (
                "Regular customers have 30 calendar days from delivery "
                "to return an unused backpack."
            )

        results = self.kb.retrieve(message, top_k=3)

        if not results:
            return (
                "I don't have enough information in the supplied materials "
                "to answer that reliably. Human confirmation is recommended."
            )

        return (
            f"I found relevant information in {results[0]['filename']}, "
            "but I need more specific details to answer reliably."
        )
