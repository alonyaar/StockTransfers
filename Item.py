from enum import Enum
from TransfersList import TransferList
from StudioEnums import *

NUM_OF_SIZES = 6
NUM_OF_STORES = 3
DESIRED_STOCK_RISHPON = 3
DESIRED_STOCK_TACHANA = 2

class Item:
    def __init__(self, code, description, color, isOneSize=False):
        self.code = code
        self.description = description
        self.color = color
        self.age = "נשים"
        self.stock = [[0 for x in range(NUM_OF_SIZES)] for y in range(NUM_OF_STORES)]
        self.desired_stock = [[0 for x in range(NUM_OF_SIZES)] for y in range(NUM_OF_STORES)]
        self.isOneSize = isOneSize
        return

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        return self.code == other.code

    def __ne__(self, other):
        return not(self == other)

    """
    Prints the stock of the item in a friendly representation.
    """
    def printStock(self):
        stock_repr = "           |XS|S |M |L |XL|W |\n"
        stock_repr += "Warehouse: " + str(self.stock[Stores.WAREHOUSE.value]) + "\n"
        stock_repr += "Rishpon:   " + str(self.stock[Stores.RISHPON.value]) + "\n"
        stock_repr += "Tachana:   " + str(self.stock[Stores.TACHANA.value]) + "\n"
        print(stock_repr)
        return

    """
    Update the actual stock of a given size for this item.
    """
    def update_stock(self, store, size, amount):
        self.stock[store][size] = amount
        return

    """
    Update the desired stock of a given size for this item.
    """
    def update_desired_stock(self, store, size, amount):
        self.desired_stock[store][size] = amount

    """
    Updates all of the stock within a given store by the entered amounts.
    """
    def updateStockByStore(self, store, xs, s, m, l, xl, w):
        self.update_stock(store, Sizes.XS.value, xs)
        self.update_stock(store, Sizes.S.value, s)
        self.update_stock(store, Sizes.M.value, m)
        self.update_stock(store, Sizes.L.value, l)
        self.update_stock(store, Sizes.XL.value, xl)
        self.update_stock(store, Sizes.W.value, w)
        return

    """
    Auto fills the desired stock of the item with 2 of each size in Rishpon and
    1 in Tachana.
    """
    def auto_update_desired_stock(self):
        for size in range(NUM_OF_SIZES):
            self.update_desired_stock(Stores.RISHPON.value, size, DESIRED_STOCK_RISHPON)
        for size in range(NUM_OF_SIZES):
            self.update_desired_stock(Stores.TACHANA.value, size, DESIRED_STOCK_TACHANA)
        return

    """
    Checks if the stock of a given size is negative in one of the stores.
    """
    def checkStockValidity(self, size, warnings_file):
        if self.stock[Stores.WAREHOUSE.value][size] < 0:
            print("NEGATIVE STOCK ALERT:", self.description, self.color, "has", self.stock[Stores.WAREHOUSE.value][size], "in warehouse!")
            # WRITE WARNING NEGATIVE STOCK IN Stores.WAREHOUSE.value
            pass
        if self.stock[Stores.RISHPON.value][size] < 0:
            print("NEGATIVE STOCK ALERT:", self.description, self.color, "has", self.stock[Stores.RISHPON.value][size], "in Rishpon!")
            # WRITE WARNING NEGATIVE STOCK IN Stores.RISHPON.value
            pass
        if self.stock[Stores.TACHANA.value][size] < 0:
            print("NEGATIVE STOCK ALERT:", self.description, self.color, "has", self.stock[Stores.TACHANA.value][size], "in Tachana!")
            # WRITE WARNING NEGATIVE STOCK IN Stores.TACHANA.value
            pass
    """
    Tansfers last pieces between the stores if the stock is not full enough.
    """
    def transferLastPiecesFromStores(self, warnings_file):
        num_of_sizes_rishpon = 0
        num_of_items_rishpon = 0
        num_of_sizes_tachana = 0
        num_of_items_tachana = 0

        # Calculates the num of pieces & num of different sizes in each store.
        for size in range(NUM_OF_SIZES):
            self.checkStockValidity(size, warnings_file)  # Checks for negative stock
            if self.stock[Stores.RISHPON.value][size] > 0:
                num_of_sizes_rishpon += 1
                num_of_items_rishpon += self.stock[Stores.RISHPON.value][size]
            if self.stock[Stores.TACHANA.value][size] > 0:
                num_of_sizes_tachana += 1
                num_of_items_tachana += self.stock[Stores.TACHANA.value][size]

        if num_of_items_tachana == 0:  # If Tachana's stock is empty.
            return

        if num_of_sizes_tachana == 1:       # Transfers stock if only one size remain
            self.transferAllStockOfStore(TransferFromTo.TACHANA_TO_RISHPON)
        if num_of_sizes_tachana == 2:      # If only two sizes remain:
            sizePair = self.checkForLastSizePair()
        if num_of_items_tachana == 2 and num_of_sizes_tachana == 2:  # Transfer items to Rishpon
            self.transferAllStockOfStore(TransferFromTo.TACHANA_TO_RISHPON)
        elif num_of_items_tachana > 2 and num_of_sizes_tachana == 2:
            print("Attention: Only" ,sizePair.name, "remain of", self.description, self.color, "total of", num_of_items_tachana, "items !!!")
            pass
            # Print Warning that stock is almost over in Tachana with the sizes.

        return

    """
    Checks whether or not the whole stock of the warehouse should be transferred
    to the stores. If it should, decide to which store according to the distances.
    As the distance higher, it means that the stock in that store is lower.
    The function returns the new distances of the stores (in a tuple).
    """
    def transferLastPiecesFromWarehouse(self):
        num_of_sizes_warehouse = 0
        num_of_items_warehouse = 0

        for size in range(NUM_OF_SIZES):
            if self.stock[Stores.WAREHOUSE.value][size] > 0:
                num_of_sizes_warehouse += 1
                num_of_items_warehouse += self.stock[Stores.WAREHOUSE.value][size]

        if num_of_items_warehouse == 0:
            return

        if num_of_sizes_warehouse == 1 and num_of_items_warehouse == 1:
            self.transferAllStockOfWarehouse()
        if num_of_sizes_warehouse == 2 and num_of_items_warehouse == 2:
            self.transferAllStockOfWarehouse()
        return

    """
    Transfers the last pieces that remain in the Warehouse.
    """
    def transferAllStockOfWarehouse(self):
        for size in range(NUM_OF_SIZES):
            rishpon_dist = self.desired_stock[Stores.RISHPON.value][size] - self.stock[Stores.RISHPON.value][size]
            tachana_dist = self.desired_stock[Stores.TACHANA.value][size] - self.stock[Stores.TACHANA.value][size]
            if self.stock[Stores.WAREHOUSE.value][size] > 0:
                if rishpon_dist >= tachana_dist and rishpon_dist >= 0:
                    self.transferFromTo(TransferFromTo.WAREHOUSE_TO_RISHPON, size, 1)
                if tachana_dist > rishpon_dist and tachana_dist >= 0:
                    self.transferFromTo(TransferFromTo.WAREHOUSE_TO_TACHANA, size, 1)
        return

    """
    Transfers the last pieces that remain in 'fromStore' to 'toStore'.
    params: fromStore and toStore are of type Stores enum.
    """
    def transferAllStockOfStore(self, fromToStore):
        fromStore = fromToStore.fromStore
        for size in range(NUM_OF_SIZES):
            if self.stock[fromStore.value][size] > 0:
                self.transferFromTo(fromToStore, size, 1)
        return

    """
    Checks if the sizes remain in the Tachana Store are too different from one another.
    """
    def checkForLastSizePair(self):
        if self.stock[Stores.TACHANA.value][Sizes.XL.value] > 0 and self.stock[Stores.TACHANA.value][Sizes.L.value] > 0:
            return SizePairs.XL_L
        elif self.stock[Stores.TACHANA.value][Sizes.XL.value] > 0 and self.stock[Stores.TACHANA.value][Sizes.M.value] > 0:
            return SizePairs.XL_M
        elif self.stock[Stores.TACHANA.value][Sizes.XL.value] > 0 and self.stock[Stores.TACHANA.value][Sizes.S.value] > 0:
            return SizePairs.XL_S
        elif self.stock[Stores.TACHANA.value][Sizes.XL.value] > 0 and self.stock[Stores.TACHANA.value][Sizes.XS.value] > 0:
            return SizePairs.XL_XS
        elif self.stock[Stores.TACHANA.value][Sizes.L.value] > 0 and self.stock[Stores.TACHANA.value][Sizes.XS.value] > 0:
            return SizePairs.L_XS
        else:
            return SizePairs.NO_PAIR

    """
    Transfers the item in the given size from 'fromStore' to 'toStore' (kept inside
    'fromToStore') in the given amount.
    params: 'fromToStore' is from type TransferFromTo enum.
    """
    def transferFromTo(self, fromToStore, size, amount):
        self.stock[fromToStore.fromStore.value][size] -= 1
        self.stock[fromToStore.toStore.value][size] += 1
        TransferList.add_transfer(self, fromToStore, size, amount)
        return

    """
    Returns the distance between the desired stock of the given size in rishpon and tachana.
    """
    def getDistances(self, size):
        rishpon_dist = self.desired_stock[Stores.RISHPON.value][size] - self.stock[Stores.RISHPON.value][size]
        tachana_dist = self.desired_stock[Stores.TACHANA.value][size] - self.stock[Stores.TACHANA.value][size]
        return rishpon_dist, tachana_dist
