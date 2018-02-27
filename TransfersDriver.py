from Item import *
from TransfersList import *
from StudioEnums import *
from WomenItem import *
from StockParser import *

def main():
    TransferFromTo.updateToFromDirections()
    parser = StockParser("/Users/NivYaar/Downloads/Try.csv")
    while (not parser.isEOF()):
        item = parser.getNextItem()
        print("=======================")
        print(item.description)
        print("=======================")
        item.printStock()
        item.transfer()
        item.printStock()
    TransferList.exportTransfers(1)
    parser.closeParser()
    return



# Tests
# item = WomenItem(2, "סקיני פרינט" ,66)
# item.updateStockByStore(Stores.WAREHOUSE, 0, 0, 0, 1, 0, 0)
# item.updateStockByStore(Stores.RISHPON,   2, 2, 1, 2, 0, 0)
# item.updateStockByStore(Stores.TACHANA,   1, 2, 1, 2, 0, 0)
#
# item.auto_update_desired_stock()
# item.printStock()
# # main(item)
# item.transfer()
# item.printStock()
# TransferList.exportTransfers("lala")

main()
