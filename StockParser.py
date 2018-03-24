from WomenItem import WomenItem
from GirlsItem import GirlsItem
from EventsItem import EventsItem
from StudioEnums import *
import platform
import codecs

CODE_INDEX = 0
DESCRIPTION_INDEX = 1
COLOR_INDEX = 3
COLOR_DESCRIPTION = 4
STORE_INDEX = 5
SIZES_FIRST_INDEX = 10
ONE_SIZE_INDEX = 18
TWO_SIZES_ONLY = 40

class StockParser:
    def __init__(self, path):
        self.stockFile = codecs.open(path, 'rb')
        self.curCode = ""
        self.curLine = None
        return

    """
    Closes the parser with all of its I/O.
    """
    def closeParser(self):
        self.stockFile.close()
        return

    """
    Checks if end of file reached while parsing the stock file.
    """
    def isEOF(self):
        return (not self.curLine and self.curLine != None)

    """
    Creates a new instance of type Item that is parsed out of the stock file.
    The function fills the item's stock in any store that appears in the stock
    file.
    """
    def getNextItem(self):
        if self.curLine == None:      # If this is the first item in the file.
            self.curLine = self.stockFile.readline().decode("utf8")
            self.curLine = self.stockFile.readline().decode("utf8")
        if self.isEOF():  # If EOF reached
            return None
        if self.curLine.strip()[0] == ',':
            return None

        item = self.startNewItem()

        self.curLine = self.stockFile.readline().decode("utf8")
        splitted_newLine = self.curLine.split(',')
        code = splitted_newLine[CODE_INDEX] + splitted_newLine[COLOR_INDEX] if self.curLine else ""
        # Continue building the current item as long as it has more stores.
        while (self.curLine and self.curCode == code):
            item = self.parseStockFromLine(item, splitted_newLine)
            StockParser.checkIfFewSizes(item, splitted_newLine)
            self.curLine = self.stockFile.readline().decode("utf8")
            splitted_newLine = self.curLine.split(',')
            code = splitted_newLine[CODE_INDEX] + splitted_newLine[COLOR_INDEX] if self.curLine else ""
        item.saveInitialStock()
        return item

    """
    Creates a new instance of the current item and fills it with the stock in
    the first store that appears.
    """
    def startNewItem(self):
        splitted_item = self.curLine.split(',')
        self.curCode = splitted_item[CODE_INDEX] + splitted_item[COLOR_INDEX]
        item = None
        item_type = splitted_item[CODE_INDEX][0]
        color = splitted_item[COLOR_INDEX] + " - " + splitted_item[COLOR_DESCRIPTION]

        if item_type == '3' or splitted_item[CODE_INDEX][0:2] == 'A3':
            item = WomenItem(self.curCode, splitted_item[DESCRIPTION_INDEX], color)
        elif item_type == '2':
            item = GirlsItem(self.curCode, splitted_item[DESCRIPTION_INDEX], color)
        elif item_type == 'A' and splitted_item[CODE_INDEX][1] == '2':
            item = EventsItem(self.curCode, splitted_item[DESCRIPTION_INDEX], color)
        self.parseStockFromLine(item, splitted_item)
        StockParser.checkIfFewSizes(item,splitted_item)
        return item

    """
    Parses the stock out of the current line and fills the 'stock' field in the
    current item.
    """
    def parseStockFromLine(self, item, splitted_line):
        if splitted_line[STORE_INDEX] == '':  # If the store is not recognized
            return item
        store = Stores.getStore(int(splitted_line[STORE_INDEX]))
        if store == None:
            return item
        num_of_sizes = item.getNumOfSizes()
        splitted_line = splitted_line[SIZES_FIRST_INDEX:]
        for size in range(num_of_sizes):
            if splitted_line[size].strip() != "":
                item.update_stock(store, size, int(splitted_line[size]))
        return item

    """
    Checks if the given item should be set as a ONE-SIZE item.
    """
    def checkIfFewSizes(item, splitted_line):
        if item.code[1:3] == str(TWO_SIZES_ONLY):
            item.setItemAsFewSizes()

        if item.code[CODE_INDEX] == '3':
            if splitted_line[ONE_SIZE_INDEX] != "":
                item.setItemAsFewSizes()
