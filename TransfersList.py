from StudioEnums import TransferFromTo as tft
from StudioEnums import *
from collections import OrderedDict
import platform
import os

TABLE_HEADLINE_RISHPON = """<tr>
    <th colspan="7">
    <h2>העברות מרשפון</h2>
    </th>
    </tr>
    """

TABLE_HEADLINE_WAREHOUSE = """<tr>
    <th colspan="7">
    <h2>העברות מהמחסן</h2>
    </th>
    </tr>
    """

TABLE_HEADLINE_TACHANA = """<tr>
    <th colspan="7">
    <h2>העברות מהתחנה</h2>
    </th>
    </tr>
    """

TABLE_PROPERTIES = """<tr>
  <th></th>
  <th>שם פריט</th>
  <th>נשים/ילדות</th>
  <th>צבע</th>
  <th>מידה</th>
  <th>כמות</th>
  <th>עבור</th>
  </tr>"""

"""
This class is a 'static' class that holds all of the transfers that should be carried out.
"""
class TransferList:

    transfersDict = OrderedDict()

    """
    Adds to the transfers dictionary a new transfer.
    The function gets the item that should be transfers with its size and amount.
    In addition the 'transferFromTo' indicates from where to where the items should
    be transfered and the 'transferToFrom' should be used in order to check if the
    item should already be transfered in the other direction.
    """
    def add_transfer(item, fromToStore, size, amount):
        transferFromTo = fromToStore
        transferToFrom = fromToStore.toFrom
        transfers = TransferList.transfersDict
        if item not in transfers:
            transfers[item] = {}

        TransferList.checkForChainTransfer(item, transferFromTo, size, amount)

        if transferFromTo not in transfers[item]:
            transfers[item][transferFromTo] = [0 for x in range(item.getNumOfSizes())]

        # Checks if the item in the given size should be transfered in the other direction.
        if transferToFrom in transfers[item] and transfers[item][transferToFrom][size] > 0:
            transfers[item][transferToFrom][size] -= 1
        else:
            transfers[item][transferFromTo][size] += 1
        return

    """
    Checks if the item is transfered from Warehouse to Rishpon and then to Tachana.
    If it is, change the transfer so it will be sent directly from Warehouse to Tachana.
    """
    def checkForChainTransfer(item, transferFromTo, size, amount):
        transfers = TransferList.transfersDict
        if transferFromTo == TransferFromTo.RISHPON_TO_TACHANA:
            warehouse_to_rishpon = TransferFromTo.WAREHOUSE_TO_RISHPON
            if warehouse_to_rishpon in transfers[item] and transfers[item][warehouse_to_rishpon][size] > 0:
                if TransferFromTo.WAREHOUSE_TO_TACHANA not in transfers[item]:
                    transfers[item][TransferFromTo.WAREHOUSE_TO_TACHANA] = [0 for x in range(item.getNumOfSizes())]
                transfers[item][warehouse_to_rishpon][size] -= 1
                transfers[item][TransferFromTo.WAREHOUSE_TO_TACHANA][size] += 1
                return

        if transferFromTo == TransferFromTo.TACHANA_TO_RISHPON:
            warehouse_to_tachana = TransferFromTo.WAREHOUSE_TO_TACHANA
            if warehouse_to_tachana in transfers[item] and transfers[item][warehouse_to_tachana][size] > 0:
                if TransferFromTo.WAREHOUSE_TO_RISHPON not in transfers[item]:
                    transfers[item][TransferFromTo.WAREHOUSE_TO_RISHPON] = [0 for x in range(item.getNumOfSizes())]
                transfers[item][warehouse_to_tachana][size] -= 1
                transfers[item][TransferFromTo.WAREHOUSE_TO_RISHPON][size] += 1
                return
        return

    """
    Exports 3 files of transfers for each store.
    If error has occurred while writing to the files - return False, else True.
    """
    def exportTransfers():
        try:
            # Open the Transfers directory on the user's Desktop.
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            new_dir = desktop + "/Transfers"
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)

            fileWarehouse = open(new_dir + '/Warehouse.html', 'wb')
            fileRishpon = open(new_dir + '/Rishpon.html', 'wb')
            fileTachana = open(new_dir + '/Tachana.html', 'wb')

            TransferList.writeHeadOfFile(fileWarehouse, TABLE_HEADLINE_WAREHOUSE)
            TransferList.writeHeadOfFile(fileRishpon, TABLE_HEADLINE_RISHPON)
            TransferList.writeHeadOfFile(fileTachana, TABLE_HEADLINE_TACHANA)

            TransferList.writeTransfersToFiles(fileWarehouse, fileRishpon, fileTachana)

            fileWarehouse.close()
            fileRishpon.close()
            fileTachana.close()
            TransferList.transfersDict = {}
            return True
        except Exception as e:
            print(e)
            return False

    """
    Writes the transfers to the given files.
    """
    def writeTransfersToFiles(fileWarehouse, fileRishpon, fileTachana):
        transfers = TransferList.transfersDict
        for item in transfers:              # Iterate over all of the items
            for fromTo in transfers[item]:  # Iterate over all of the transfers for that item.
                shouldWriteInfo = True      # Indicates whether or not this is the first transfer of the item.
                for i in range(len(transfers[item][fromTo])):  # Iterate over all of the sizes.
                    amount = transfers[item][fromTo][i]
                    if amount > 0:
                        amount = str(amount)
                        if fromTo.fromStore == Stores.WAREHOUSE:
                            TransferList.writeItemToFile(fileWarehouse, item, fromTo.toStore, i, amount, shouldWriteInfo)
                        elif fromTo.fromStore == Stores.RISHPON:
                            TransferList.writeItemToFile(fileRishpon, item, fromTo.toStore, i, amount, shouldWriteInfo)
                        elif fromTo.fromStore == Stores.TACHANA:
                            TransferList.writeItemToFile(fileTachana, item, fromTo.toStore, i, amount, shouldWriteInfo)
                        shouldWriteInfo = False   # If the amount to transfer is positive.

    """
    Writes the styles and headers to the final HTML output file.
    """
    def writeHeadOfFile(transfers_file, titleForThisFile):
        transfers_file.write("<html> <body dir='rtl'>\n".encode("utf8"))
        transfers_file.write("<?php header('Content-Type: text/html; charset=utf-8'); ?>\n".encode("utf8"))
        transfers_file.write("<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />\n".encode("utf8"))
        transfers_file.write("""
            <head>
            <style>
            h2 {
              color: #111;
              font-family: "Alef", Arial, sans-serif;
              color: white;
              font-size: 38px;
              font-weight: 300;
              line-height: 32px;
              font-weight: bold;
              margin: 0 0 3px;
              text-align: center;
            }

            input[type=checkbox] {
              transform: scale(1.5);
            }

            @font-face{
            	font-family: 'Alef';
                font-weight: normal;
            	src: url('Alef-Webfont/Alef-Regular.eot');
            	src: url('Alef-Webfont/Alef-Regular.eot?#iefix') format('embedded-opentype'),
            	     url('Alef-Webfont/Alef-Regular.woff') format('woff'),
            	     url('Alef-Webfont/Alef-Regular.ttf') format('truetype'),
            	     url('Alef-Webfont/Alef-Regular.svg#webfont') format('svg');
            }

            @font-face{
                font-family: 'Alef';
                font-weight: bold;
            	src: url('Alef-Webfont/Alef-Bold.eot');
            	src: url('Alef-Webfont/Alef-Bold.eot?#iefix') format('embedded-opentype'),
            	     url('Alef-Webfont/Alef-Bold.woff') format('woff'),
            	     url('Alef-Webfont/Alef-Bold.ttf') format('truetype'),
            	     url('Alef-Webfont/Alef-Bold.svg#webfont') format('svg');
            }

            tr.itemHead td{
              border-top: : 0.5px solid black;
              border-left: 1px solid #ddd;
              border-right: 1px solid #ddd;
              border-style: solid solid none solid;
              /* font-weight: bold */
            }

            tr.itemReg td{
              border-top: 1px solid #ddd;
              border-left: 1px solid #ddd;
              border-right: 1px solid #ddd;
            }

            #transfers {
                font-family: "Alef", Arial, Helvetica, sans-serif;
                font-weight: normal;
                border-collapse: collapse;
                width: 100%;
            }

            #transfers td, #rishpon th {
                padding: 8px;
            }

            #transfers tr:nth-child(even){background-color: #f2f2f2;}

            #transfers tr:hover {background-color: #bfbfbf;}

            #transfers th {
                border: 2px solid white;
                padding-top: 12px;
                padding-bottom: 12px;
                text-align: center;
                background-color: #f64c4c;
                font-weight: bold;
                color: white;
            }
            </style>
            </head>""".encode("utf8"))
        TransferList.writeTable(transfers_file, titleForThisFile)

    """
    Writes the HTML code to write the next code into the correct table.
    toWhereHeadLine must be one of the HEADLINE constants of this class.
    """
    def writeTable(transfers_file, toWhereHeadLine):
        tableHTMLString = "<table id='transfers'>"
        transfers_file.write(tableHTMLString.encode("utf8"))
        transfers_file.write(toWhereHeadLine.encode("utf8"))
        transfers_file.write(TABLE_PROPERTIES.encode("utf8"))

    """
    Writes the item representation as a row in an HTML table.
    @param size: is from type int.
    @param shouldWriteInfo: If it is True, than this is the first row of the given
    item and all of its data should be written in the table, else the info is empty.
    @variable isStockEmpty: Checks if the current stock in the store is 0 so the
    row in the ouptut will be highlighted.
    """
    def writeItemToFile(transfersFile, item, toStore, size, amount, shouldWriteInfo):
        isStockEmpty = item.isEmpty(toStore, size)
        sizesDict = CharSizesDict if item.code[0] == '3' or item.code[0] == 'A' else NumSizesDict
        size_repr = sizesDict[size]

        description = item.description if shouldWriteInfo else ""
        women_or_girls = item.age if shouldWriteInfo else ""
        color = item.color if shouldWriteInfo else ""
        emptyHighligt = "background-color:#fcd4d4;" if isStockEmpty else ""
        firstRowBold = "itemHead" if shouldWriteInfo else "itemReg"

        openRow = "<tr class='" + firstRowBold + "'>"
        description_string = "\t<td>"+ description +"</td>"
        women_or_girls_string = "\t<td>" + women_or_girls + "</td>"
        color_string = "\t<td>"+ color +"</td>"
        size_string = "\t<td style='"+ emptyHighligt + "'>" + size_repr +"</td>"
        amount_string = "\t<td style='"+ emptyHighligt + "'>" + amount +"</td>"
        toStore_string = "\t<td style='"+ emptyHighligt + "'>" + TransferList.getStoreHebrewName(toStore) + "</td>"

        transfersFile.write(openRow.encode("utf8"))
        transfersFile.write("\t<td><input type='checkbox'></td>".encode("utf8"))
        transfersFile.write(description_string.encode("utf8"))
        transfersFile.write(women_or_girls_string.encode("utf8"))
        transfersFile.write(color_string.encode("utf8"))
        transfersFile.write(size_string.encode("utf8"))
        transfersFile.write(amount_string.encode("utf8"))
        transfersFile.write(toStore_string.encode("utf8"))

    """
    Returns the hebrew name of the given store.
    """
    def getStoreHebrewName(store):
        if store == Stores.WAREHOUSE:
            return "מחסן"
        if store == Stores.RISHPON:
             return "רשפון"
        if store == Stores.TACHANA:
            return "תחנה"
        else:
            return ""
