from Item import *
from StudioEnums import *

class GirlsItem(Item):
    def __init__(self, code, description, color):
        super().__init__(code, description, color)
        self.age = "ילדות"
        self.stock = [[0 for x in range(NUM_OF_SIZES_GIRLS)] for y in range(NUM_OF_STORES)]
        self.desired_stock = [[0 for x in range(NUM_OF_SIZES_GIRLS)] for y in range(NUM_OF_STORES)]
        self.auto_update_desired_stock()
        return

    """
    Auto fills the desired stock of the item with 2 of each size in Rishpon and
    1 in Tachana.
    """
    def auto_update_desired_stock(self):
        super().auto_update_desired_stock(NUM_OF_SIZES_GIRLS)
        return

    """
    Makes the transfers of the current item between the stores.
    """
    def transfer(self, warnings_file):
        super().transfer(NUM_OF_SIZES_GIRLS, warnings_file)
        return

    """
    Prints the stock of the item in a friendly representation.
    """
    def printStock(self):
        stock_repr = "           |01|02|04|06|08|10|12|14|16|18|20\n"
        stock_repr += "Warehouse: " + str(self.stock[Stores.WAREHOUSE.value]) + "\n"
        stock_repr += "Rishpon:   " + str(self.stock[Stores.RISHPON.value]) + "\n"
        stock_repr += "Tachana:   " + str(self.stock[Stores.TACHANA.value]) + "\n"
        print(stock_repr)
        return

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
    Tansfers last pieces between the stores if the stock is not full enough.
    """
    def transferLastPiecesFromStores(self, warnings_file):
        super().transferLastPiecesFromStores(warnings_file, NUM_OF_SIZES_GIRLS, GirlsSizesDict)

    """
    Checks whether or not the whole stock of the warehouse should be transferred
    to the stores. If it should, decide to which store according to the distances.
    As the distance higher, it means that the stock in that store is lower.
    The function returns the new distances of the stores (in a tuple).
    """
    def transferLastPiecesFromWarehouse(self):
        super().transferLastPiecesFromWarehouse(NUM_OF_SIZES_GIRLS)

    """
    Transfers the last pieces that remain in the Warehouse.
    """
    def transferAllStockOfWarehouse(self):
        super().transferAllStockOfWarehouse(NUM_OF_SIZES_GIRLS)

    """
    Transfers the last pieces that remain in 'fromStore' to 'toStore'.
    params: fromStore and toStore are of type Stores enum.
    """
    def transferAllStockOfStore(self, fromToStore):
        super().transferAllStockOfStore(fromToStore, NUM_OF_SIZES_GIRLS)

    """
    Checks if the sizes remain in the Tachana Store are too different from one another.
    If they are close return False, else True.
    """
    def checkForLastSizePair(self):
        return False
        if self.stock[Stores.TACHANA.value][Sizes.XL.value] > 0 and self.stock[Stores.TACHANA.value][Sizes.L.value] > 0:
            return True
        elif self.stock[Stores.TACHANA.value][Sizes.XL.value] > 0 and self.stock[Stores.TACHANA.value][Sizes.M.value] > 0:
            return True
        elif self.stock[Stores.TACHANA.value][Sizes.XL.value] > 0 and self.stock[Stores.TACHANA.value][Sizes.S.value] > 0:
            return True
        elif self.stock[Stores.TACHANA.value][Sizes.XL.value] > 0 and self.stock[Stores.TACHANA.value][Sizes.XS.value] > 0:
            return True
        elif self.stock[Stores.TACHANA.value][Sizes.L.value] > 0 and self.stock[Stores.TACHANA.value][Sizes.XS.value] > 0:
            return True
        else:
            return False

    """
    Gets the number of sizes that should exist for this item.
    """
    def getNumOfSizes(self):
        return NUM_OF_SIZES_GIRLS
