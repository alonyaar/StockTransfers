from enum import Enum

NUM_OF_SIZES_WOMEN = 6
NUM_OF_SIZES_GIRLS = 6
NUM_OF_STORES = 3

class Stores(Enum):
    WAREHOUSE = 0
    RISHPON = 1
    TACHANA = 2

class Sizes(Enum):
    W = 5
    XL = 4
    L = 3
    M = 2
    S = 1
    XS = 0

class SizePairs(Enum):
    NO_PAIR = 0
    XL_L = 1
    XL_M = 2
    XL_S = 3
    XL_XS = 4
    L_XS = 5

class TransferFromTo(Enum):
    WAREHOUSE_TO_RISHPON = (Stores.WAREHOUSE, Stores.RISHPON, None)
    WAREHOUSE_TO_TACHANA = (Stores.WAREHOUSE, Stores.TACHANA, None)
    RISHPON_TO_WAREHOUSE = (Stores.RISHPON, Stores.WAREHOUSE, None)
    RISHPON_TO_TACHANA = (Stores.RISHPON, Stores.TACHANA, None)
    TACHANA_TO_WAREHOUSE = (Stores.TACHANA, Stores.WAREHOUSE, None)
    TACHANA_TO_RISHPON = (Stores.TACHANA, Stores.RISHPON, None)

    def __init__(self, fromStore, toStore, oppositeDirection):
        self.fromStore = fromStore
        self.toStore = toStore
        self.toFrom = oppositeDirection
        return

    def updateToFromDirections():
        TransferFromTo.WAREHOUSE_TO_RISHPON.toFrom = TransferFromTo.RISHPON_TO_WAREHOUSE
        TransferFromTo.WAREHOUSE_TO_TACHANA.toFrom = TransferFromTo.TACHANA_TO_WAREHOUSE
        TransferFromTo.RISHPON_TO_WAREHOUSE.toFrom = TransferFromTo.WAREHOUSE_TO_RISHPON
        TransferFromTo.RISHPON_TO_TACHANA.toFrom = TransferFromTo.TACHANA_TO_RISHPON
        TransferFromTo.TACHANA_TO_WAREHOUSE.toFrom = TransferFromTo.WAREHOUSE_TO_TACHANA
        TransferFromTo.TACHANA_TO_RISHPON.toFrom = TransferFromTo.RISHPON_TO_TACHANA
        return
