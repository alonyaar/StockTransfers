from Item import *
from TransfersList import *
from StudioEnums import *
from WomenItem import *
from StockParser import *

def main(pathOfStock):
    TransferFromTo.updateToFromDirections()
    parser = StockParser("/Users/NivYaar/Downloads/Try.csv")
    while (not parser.isEOF()):
        item = parser.getNextItem()
        print("=======================")
        print(item.description)
        print("=======================")
        item.printStock()
        item.transfer(2)
        item.printStock()
    TransferList.exportTransfers(1)
    parser.closeParser()
    return



main(1)
