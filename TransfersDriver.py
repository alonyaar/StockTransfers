from Item import *
from TransfersList import *
from StudioEnums import *
from WomenItem import *

def main(item):
    TransferFromTo.updateToFromDirections()
    item.transfer()
    return



# Tests
item = WomenItem(2, "סקיני פרינט" ,66)
item.updateStockByStore(Stores.WAREHOUSE.value, 1, 2, 0, 0, 1, 0)
item.updateStockByStore(Stores.RISHPON.value,   0, 1, 0, 1, 0, 0)
item.updateStockByStore(Stores.TACHANA.value,   0, 0, 1, 1, 0, 0)

item.auto_update_desired_stock()
item.printStock()
main(item)
item.printStock()
TransferList.exportTransfers("lala")
