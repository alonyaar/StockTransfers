from Item import *
from TransfersList import *
from StudioEnums import *

def main():
    return

def transfer(item, file, look_up_table):
    TransferFromTo.updateToFromDirections()
    for size in range(NUM_OF_SIZES):  # First transfer from Warehouse to stores.
        rishpon_dist, tachana_dist = item.getDistances(size)

        if rishpon_dist > 0:    # TRANSFER FROM WAREHOUSE TO RISHPON
            while (rishpon_dist > 0 and item.stock[Stores.WAREHOUSE.value][size] > 0):
                item.transferFromTo(TransferFromTo.WAREHOUSE_TO_RISHPON, size, 1)
                rishpon_dist -= 1

        if tachana_dist > 0:   # TRANSFER FROM WAREHOUSE TO TACHANA
            while (tachana_dist > 0 and item.stock[Stores.WAREHOUSE.value][size] > 0):
                item.transferFromTo(TransferFromTo.WAREHOUSE_TO_TACHANA, size, 1)
                tachana_dist -= 1

    item.printStock()
    item.transferLastPiecesFromWarehouse()
    item.printStock()

    for size in range(NUM_OF_SIZES):  # Then transfer between storesself.
        rishpon_dist, tachana_dist = item.getDistances(size)
        # TRANSFER FROM RISHPON TO TACHANA
        while tachana_dist > 0 and rishpon_dist < tachana_dist:
            rishpon_dist, tachana_dist = item.getDistances(size)
            item.transferFromTo(TransferFromTo.RISHPON_TO_TACHANA, size, 1)
            tachana_dist -= 1
            rishpon_dist += 1

        # Transfer from Tachana to Rishpon if the dist' of Rishpon is higher.
        while rishpon_dist > 0 and tachana_dist <= 0 or (rishpon_dist - tachana_dist >= 2):
            rishpon_dist, tachana_dist = item.getDistances(size)
            if rishpon_dist == 1 and tachana_dist == 0:  # Keep it as is
                break
            else:
                item.transferFromTo(TransferFromTo.TACHANA_TO_RISHPON, size, 1)
                tachana_dist += 1
                rishpon_dist -= 1

    if !item.isOneSize:
        item.transferLastPiecesFromStores("file of warnings")
    return


# Tests
item = Item(2, "סקיני פרינט" ,66)
item.updateStockByStore(Stores.WAREHOUSE.value, 1, 2, 0, 0, 1, 0)
item.updateStockByStore(Stores.RISHPON.value,   0, 1, 0, 1, 0, 0)
item.updateStockByStore(Stores.TACHANA.value,   0, 0, 1, 1, 0, 0)

item.auto_update_desired_stock()
item.printStock()
transfer(item,1,2)
item.printStock()
TransferList.exportTransfers("lala")
