from enum import Enum
from TransfersList import TransferList
from StudioEnums import *
import platform


class Item:

    desired_stock_rishpon = 0
    desired_stock_tachana = 0

    def __init__(self, code, description, color):
        self.code = code
        self.description = description
        self.color = color
        self.age = ""
        self.stock = []
        self.desired_stock = []
        self.initialStock = []
        self.isFewSizes = False
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
        raise NotImplementedError("Please Implement this method")

    """
    Writes the stock to HTML file - Each row is written into a <p> tag.
    """
    def writeStockToFile(self, fileToWrite):
        raise NotImplementedError("Please Implement this method")

    """
    Update the actual stock of a given size for this item.
    """
    def update_stock(self, store, size, amount):
        self.stock[store.value][size] = amount
        return

    """
    Update the desired stock of a given size for this item.
    """
    def update_desired_stock(self, store, size, amount):
        self.desired_stock[store.value][size] = amount

    """
    Updates all of the stock within a given store by the entered amounts.
    """
    def updateStockByStore(self, store, xs, s, m, l, xl, w):
        raise NotImplementedError("Please Implement this method")

    """
    Auto fills the desired stock of the item with the current desired stock value.
    """
    def auto_update_desired_stock(self, numOfSizes):
        for size in range(numOfSizes):
            self.update_desired_stock(Stores.RISHPON, size, Item.desired_stock_rishpon)
        for size in range(numOfSizes):
            self.update_desired_stock(Stores.TACHANA, size, Item.desired_stock_tachana)
        return

    """
    Updates the desired stock value for Rishpon and Tachana.
    """
    def update_desired_values(rishpon, tachana):
        Item.desired_stock_rishpon = rishpon
        Item.desired_stock_tachana = tachana
        return

    """
    Updates the desired stock of the item according to the current stock in stores.
    This may help when the given desired stock is lower than the correct desired amount
    so the program can automaticlly learn the amount that should be held in each store.
    """
    def update_desired_stock_from_current_stock(self, store, numOfSizes):
        num_of_sizes_higher_than_desired = 0
        num_of_non_zero_sizes = 0
        desired_stock = desired_rishpon if store == Stores.RISHPON else desired_tachana
        for size in range(numOfSizes):
            if self.stock[store.value][size] > 0:
                num_of_non_zero_sizes += 1
            if self.stock[store.value][size] > desired_stock:
                num_of_sizes_higher_than_desired += 1
        if num_of_sizes_higher_than_desired / num_of_non_zero_sizes >= 0.5:
            self.desired_stock = [x + 1 for x in self.desired_stock]
        return

    """
    Makes the transfers of the current item between the stores.
    """
    def transfer(self, numOfSizes, warnings_file):
        # First transfer from Warehouse to stores and check for negative stock.
        for size in range(numOfSizes):
            self.checkStockValidity(size, warnings_file)  # Checks for negative stock
            rishpon_dist, tachana_dist = self.getDistances(size)
            if rishpon_dist > 0:    # TRANSFER FROM WAREHOUSE TO RISHPON
                while (rishpon_dist > 0 and self.stock[Stores.WAREHOUSE.value][size] > 0):
                    self.transferFromTo(TransferFromTo.WAREHOUSE_TO_RISHPON, size, 1)
                    rishpon_dist -= 1

            if tachana_dist > 0:   # TRANSFER FROM WAREHOUSE TO TACHANA
                while (tachana_dist > 0 and self.stock[Stores.WAREHOUSE.value][size] > 0):
                    self.transferFromTo(TransferFromTo.WAREHOUSE_TO_TACHANA, size, 1)
                    tachana_dist -= 1

        # Empty warehouse if only few pieces left there.
        # self.transferLastPiecesFromWarehouse()

        # Then transfer between stores.
        for size in range(numOfSizes):
            rishpon_dist, tachana_dist = self.getDistances(size)
            # TRANSFER FROM RISHPON TO TACHANA
            while tachana_dist > 0 and rishpon_dist < tachana_dist:
                rishpon_dist, tachana_dist = self.getDistances(size)
                self.transferFromTo(TransferFromTo.RISHPON_TO_TACHANA, size, 1)
                tachana_dist -= 1
                rishpon_dist += 1

            # Transfer from Tachana to Rishpon if the dist' of Rishpon is higher.
            while rishpon_dist > 0 and (tachana_dist <= 0 or (rishpon_dist - tachana_dist >= 2)):
                rishpon_dist, tachana_dist = self.getDistances(size)
                if rishpon_dist == 1 and tachana_dist == 0:  # Keep it as is
                    break
                else:
                    self.transferFromTo(TransferFromTo.TACHANA_TO_RISHPON, size, 1)
                    tachana_dist += 1
                    rishpon_dist -= 1

            # If Tachana has more stock than Rishpon - Transfer it to Rishpon
            extraAmount =  self.stock[Stores.TACHANA.value][size] - self.stock[Stores.RISHPON.value][size]
            if extraAmount > 0:
                self.transferFromTo(TransferFromTo.TACHANA_TO_RISHPON, size, extraAmount)

        if not self.isFewSizes:  # Transfer between stores if one store has only few pieces left.
            self.transferLastPiecesFromStores(warnings_file)
        return

    """
    Checks if the stock of a given size is negative in one of the stores.
    """
    def checkStockValidity(self, size, warnings_file):
        negativeStockWarning = "<p style='color:red;'> מלאי שלילי עבור פריט " + self.description + " בצבע " + self.color + " במחסן!" + " </p>"
        if self.stock[Stores.WAREHOUSE.value][size] < 0:
            self.stock[Stores.WAREHOUSE.value][size] = 0
            warnings_file.write(negativeStockWarning.encode("utf8"))
        if self.stock[Stores.RISHPON.value][size] < 0:
            self.stock[Stores.RISHPON.value][size] = 0
            warnings_file.write(negativeStockWarning.encode("utf8"))
        if self.stock[Stores.TACHANA.value][size] < 0:
            self.stock[Stores.TACHANA.value][size] = 0
            warnings_file.write(negativeStockWarning.encode("utf8"))
        return

    """
    Tansfers last pieces between the stores if the stock is not full enough.
    """
    def transferLastPiecesFromStores(self, warnings_file, numOfSizes, sizesDict):
        num_of_sizes_rishpon = 0
        num_of_items_rishpon = 0
        num_of_sizes_tachana = 0
        num_of_items_tachana = 0
        sizes_rishpon_for_warning = ""
        sizes_tachana_for_warning = ""

        # Calculates the num of pieces & num of different sizes in each store.
        for size in range(numOfSizes):
            if self.stock[Stores.RISHPON.value][size] > 0:
                sizes_rishpon_for_warning += str(sizesDict[size]) + "_&_"
                num_of_sizes_rishpon += 1
                num_of_items_rishpon += self.stock[Stores.RISHPON.value][size]
            if self.stock[Stores.TACHANA.value][size] > 0:
                sizes_tachana_for_warning += str(sizesDict[size]) + "_&_"
                num_of_sizes_tachana += 1
                num_of_items_tachana += self.stock[Stores.TACHANA.value][size]

        lastPiecesWarning = "<p> נשארו המידות " + sizes_tachana_for_warning[:-3] + " מדגם " + self.description + " בצבע " + self.color + " בסה״כ " + str(num_of_items_tachana) + " פריטים אחרונים בתחנה"+ " </p>"
        if num_of_items_tachana == 0:  # If Tachana's stock is empty.
            return
        if num_of_sizes_tachana == 1:     # Transfers stock if only one size remain and the size is different than rishpon
            if num_of_items_tachana == 1:
                self.transferAllStockOfStore(TransferFromTo.TACHANA_TO_RISHPON)
            else:
                warnings_file.write(lastPiecesWarning.encode("utf8"))
        if num_of_items_tachana == 2 and num_of_sizes_tachana == 2:  # Transfer items to Rishpon
            shouldTransferAll = self.checkForLastSizePair()
            if shouldTransferAll:
                self.transferAllStockOfStore(TransferFromTo.TACHANA_TO_RISHPON)
            else:
                warnings_file.write(lastPiecesWarning.encode("utf8"))
        elif num_of_items_tachana > 2 and num_of_sizes_tachana == 2:
            warnings_file.write(lastPiecesWarning.encode("utf8"))
        return

    """
    Checks whether or not the whole stock of the warehouse should be transferred
    to the stores. If it should, decide to which store according to the distances.
    As the distance higher, it means that the stock in that store is lower.
    The function returns the new distances of the stores (in a tuple).
    """
    def transferLastPiecesFromWarehouse(self,numOfSizes):
        num_of_sizes_warehouse = 0
        num_of_items_warehouse = 0

        for size in range(numOfSizes):
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
    def transferAllStockOfWarehouse(self, numOfSizes):
        for size in range(numOfSizes):
            rishpon_dist, tachana_dist = self.getDistances(size)
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
    def transferAllStockOfStore(self, fromToStore, numOfSizes):
        fromStore = fromToStore.fromStore
        for size in range(numOfSizes):
            amount = self.stock[fromStore.value][size]
            if amount > 0:
                self.transferFromTo(fromToStore, size, amount)
        return

    """
    Checks if the sizes remain in the Tachana Store are too different from one another.
    If they are close return False, else True.
    """
    def checkForLastSizePair(self):
        raise NotImplementedError("Please Implement this method in subClasses")

    """
    Transfers the item in the given size from 'fromStore' to 'toStore' (kept inside
    'fromToStore') in the given amount.
    params: 'fromToStore' is from type TransferFromTo enum.
    """
    def transferFromTo(self, fromToStore, size, amount):
        self.stock[fromToStore.fromStore.value][size] -= amount
        self.stock[fromToStore.toStore.value][size] += amount
        TransferList.add_transfer(self, fromToStore, size, amount)
        return

    """
    Returns the distance between the desired stock of the given size in rishpon and tachana.
    """
    def getDistances(self, size):
        rishpon_dist = self.desired_stock[Stores.RISHPON.value][size] - self.stock[Stores.RISHPON.value][size]
        tachana_dist = self.desired_stock[Stores.TACHANA.value][size] - self.stock[Stores.TACHANA.value][size]
        return rishpon_dist, tachana_dist

    """
    Sets the item to be an item with small range of sizes that shouldn't be
    transfered if few pieces left in store.
    """
    def setItemAsFewSizes(self):
        self.isFewSizes = True
        return

    """
    Gets the number of sizes that this item may have.
    """
    def getNumOfSizes(self):
        raise NotImplementedError("Please Implement this method")

    """
    Saves the current 'stock' field in the 'initialStock' field.
    """
    def saveInitialStock(self, numOfSizes):
        self.initialStock = [[self.stock[y][x] for x in range(numOfSizes) ] for y in range(NUM_OF_STORES)]

    """
    Returns True if this item in size 'size' doesn't exist in the given 'store'.
    """
    def isEmpty(self, store, size):
        return self.initialStock[store.value][size] == 0
