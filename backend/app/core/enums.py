from enum import Enum

class PaymentType(str, Enum):
    Card = "Card"
    UPI = "UPI"
    Cash = "Cash"
    Checque = "Checque"

class PaymentStatus(str, Enum):
    Paid = "Paid"
    Partially_paid = "Partially Paid"
    Unpaid = "Unpaid"


class OrderStatus(str, Enum):
    Completed = "Completed"
    Payment_Pending = "Payment Pending"
    Cancelled = "Cancelled"

