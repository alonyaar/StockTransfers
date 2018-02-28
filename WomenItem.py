from Item import *
from StudioEnums import *
from StudioEnums import WomenSizes as ws
class WomenItem(Item):
    def __init__(self, code, description, color):
        super().__init__(code, description, color)
        self.age = "נשים"
        self.stock = [[0 for x in range(NUM_OF_SIZES_WOMEN)] for y in range(NUM_OF_STORES)]
        self.desired_stock = [[0 for x in range(NUM_OF_SIZES_WOMEN)] for y in range(NUM_OF_STORES)]
        self.auto_update_desired_stock()
        return

    """
    Auto fills the desired stock of the item with 2 of each size in Rishpon and
    1 in Tachana.
    """
    def auto_update_desired_stock(self):
        super().auto_update_desired_stock(NUM_OF_SIZES_WOMEN)
        return
        
    """
    Makes the transfers of the current item between the stores.
    """
    def transfer(self, warnings_file):
        super().transfer(NUM_OF_SIZES_WOMEN, warnings_file)
        return
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
    Updates all of the stock within a given store by the entered amounts.
    """
    def updateStockByStore(self, store, xs, s, m, l, xl, w):
        self.update_stock(store, ws.XS.value, xs)
        self.update_stock(store, ws.S.value, s)
        self.update_stock(store, ws.M.value, m)
        self.update_stock(store, ws.L.value, l)
        self.update_stock(store, ws.XL.value, xl)
        self.update_stock(store, ws.W.value, w)
        return

    """
    Tansfers last pieces between the stores if the stock is not full enough.
    """
    def transferLastPiecesFromStores(self, warnings_file):
        super().transferLastPiecesFromStores(warnings_file, NUM_OF_SIZES_WOMEN, WomenSizesDict)

    """
    Checks whether or not the whole stock of the warehouse should be transferred
    to the stores. If it should, decide to which store according to the distances.
    As the distance higher, it means that the stock in that store is lower.
    The function returns the new distances of the stores (in a tuple).
    """
    def transferLastPiecesFromWarehouse(self):
        super().transferLastPiecesFromWarehouse(NUM_OF_SIZES_WOMEN)

    """
    Transfers the last pieces that remain in the Warehouse.
    """
    def transferAllStockOfWarehouse(self):
        super().transferAllStockOfWarehouse(NUM_OF_SIZES_WOMEN)

    """
    Transfers the last pieces that remain in 'fromStore' to 'toStore'.
    params: fromStore and toStore are of type Stores enum.
    """
    def transferAllStockOfStore(self, fromToStore):
        super().transferAllStockOfStore(fromToStore, NUM_OF_SIZES_WOMEN)

    """
    Checks if the sizes remain in the Tachana Store are too different from one another.
    If they are close return False, else True.
    """
    def checkForLastSizePair(self):
        if self.stock[Stores.TACHANA.value][ws.XL.value] > 0 and self.stock[Stores.TACHANA.value][ws.L.value] > 0:
            return SizePairs.XL_L
        elif self.stock[Stores.TACHANA.value][ws.XL.value] > 0 and self.stock[Stores.TACHANA.value][ws.M.value] > 0:
            return SizePairs.XL_M
        elif self.stock[Stores.TACHANA.value][ws.XL.value] > 0 and self.stock[Stores.TACHANA.value][ws.S.value] > 0:
            return SizePairs.XL_S
        elif self.stock[Stores.TACHANA.value][ws.XL.value] > 0 and self.stock[Stores.TACHANA.value][ws.XS.value] > 0:
            return SizePairs.XL_XS
        elif self.stock[Stores.TACHANA.value][ws.L.value] > 0 and self.stock[Stores.TACHANA.value][ws.XS.value] > 0:
            return SizePairs.L_XS
        else:
            return SizePairs.NO_PAIR

    """
    Gets the number of sizes that should exist for this item.
    """
    def getNumOfSizes(self):
        return NUM_OF_SIZES_WOMEN
