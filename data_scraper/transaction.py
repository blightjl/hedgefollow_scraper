from enum import Enum, auto

# stat class that will hold two pieces of information of a transaction:
# - raw (the total transaction value)
# - percentage (the percentage of the transaction value that was moved)

class TRANSACTION_TYPE(Enum):
    BOUGHT = auto()
    SOLD = auto()
    SALE_PLAN = auto()

class Transaction:
    def __init__(self, raw: float, percentage: float, type: TRANSACTION_TYPE):
        self.raw: float = raw
        self.percentage: float  = percentage
        self.type: TRANSACTION_TYPE = type

    def __self__(self):
        return f"{self.type} : ${self.raw} : {self.percentage}%"
    