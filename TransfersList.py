from StudioEnums import TransferFromTo as tft
from StudioEnums import *
from collections import OrderedDict
import platform
import os

TABLE_HEADLINE_RISHPON = """<tr>
    <th colspan="10">
    <h2>העברות מרשפון</h2>
    </th>
    </tr>
    """

TABLE_HEADLINE_WAREHOUSE = """<tr>
    <th colspan="10">
    <h2>העברות מהמחסן</h2>
    </th>
    </tr>
    """

TABLE_HEADLINE_TACHANA = """<tr>
    <th colspan="10">
    <h2>העברות מהתחנה</h2>
    </th>
    </tr>
    """

TABLE_PROPERTIES = """<tr>
  <th></th>
  <th> ברקוד </th>
  <th>שם פריט</th>
  <th>נשים/ילדות</th>
  <th>צבע</th>
  <th>מידה</th>
  <th>כמות</th>
  <th>עבור</th>
  <th>טבלה</th>
  <th></th>
  </tr>"""


"""
This class is a 'static' class that holds all of the transfers that should be carried out.
"""
class TransferList:

    num_of_items = 0
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

        isChain = TransferList.checkForChainTransfer(item, transferFromTo, size, amount)

        if not isChain:  # If the item should be transfered fromToStore.
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
        isChain = False
        transfers = TransferList.transfersDict
        if transferFromTo == TransferFromTo.RISHPON_TO_TACHANA:
            warehouse_to_rishpon = TransferFromTo.WAREHOUSE_TO_RISHPON
            for i in range(amount):
                if warehouse_to_rishpon in transfers[item] and transfers[item][warehouse_to_rishpon][size] > 0:
                    if TransferFromTo.WAREHOUSE_TO_TACHANA not in transfers[item]:
                        transfers[item][TransferFromTo.WAREHOUSE_TO_TACHANA] = [0 for x in range(item.getNumOfSizes())]
                    transfers[item][warehouse_to_rishpon][size] -= 1
                    transfers[item][TransferFromTo.WAREHOUSE_TO_TACHANA][size] += 1
                    isChain = True

        if transferFromTo == TransferFromTo.TACHANA_TO_RISHPON:
            warehouse_to_tachana = TransferFromTo.WAREHOUSE_TO_TACHANA
            for i in range(amount):
                if warehouse_to_tachana in transfers[item] and transfers[item][warehouse_to_tachana][size] > 0:
                    if TransferFromTo.WAREHOUSE_TO_RISHPON not in transfers[item]:
                        transfers[item][TransferFromTo.WAREHOUSE_TO_RISHPON] = [0 for x in range(item.getNumOfSizes())]
                    transfers[item][warehouse_to_tachana][size] -= 1
                    transfers[item][TransferFromTo.WAREHOUSE_TO_RISHPON][size] += 1
                    isChain = True
        return isChain

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
            TransferList.transfersDict = OrderedDict()
            return True
        except Exception as e:
            raise e
            return False

    """
    Writes the transfers to the given files.
    """
    def writeTransfersToFiles(fileWarehouse, fileRishpon, fileTachana):
        transfers = TransferList.transfersDict
        for item in transfers:              # Iterate over all of the items
            for fromToStore in transfers[item]:  # Iterate over all of the transfers for that item.
                shouldWriteInfo = True      # Indicates whether or not this is the first transfer of the item.
                for i in range(len(transfers[item][fromToStore])):  # Iterate over all of the sizes.
                    TransferList.num_of_items += 1
                    amount = transfers[item][fromToStore][i]
                    if amount > 0:
                        amount = str(amount)
                        if fromToStore.fromStore == Stores.WAREHOUSE:
                            TransferList.writeItemToFile(fileWarehouse, item, fromToStore, i, amount, shouldWriteInfo)
                        elif fromToStore.fromStore == Stores.RISHPON:
                            TransferList.writeItemToFile(fileRishpon, item, fromToStore, i, amount, shouldWriteInfo)
                        elif fromToStore.fromStore == Stores.TACHANA:
                            TransferList.writeItemToFile(fileTachana, item, fromToStore, i, amount, shouldWriteInfo)
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
              font-family: "Arial", Arial, sans-serif;
              color: white;
              font-size: 38px;
              font-weight: 300;
              line-height: 32px;
              font-weight: bold;
              margin: 0 0 3px;
              text-align: center;
            }


            .popup {
                position: relative;
                display: inline-block;
                cursor: pointer;
            }

            /* The actual popup (appears on top) */
            .popup .popuptext {
                visibility: hidden;
                width: 290px;
                background-color: white;
                border: 12px;
                border-color: black;
                color: black;
                text-align: right;
                padding: 8px 5px;
                border: 3px solid black;
                border-radius: 8px;
                position: absolute;
                z-index: 1;
                bottom: 125%;
                left: 1%;
                margin-left: -137px;
            }

            /* Popup arrow */
            .popup .popuptext::after {
                content: "";
                position: absolute;
                top: 102%;
                left: 50%;
                margin-left: -5px;
                border-width: 5px;
                border-style: solid;
                border-color: red transparent transparent transparent;
            }

            /* Toggle this class when clicking on the popup container (hide and show the popup) */
            .popup .show {
                visibility: visible;
            }
            input[type=checkbox] {
              transform: scale(1.5);
            }

            tr.itemHead td{
              border-top: : 0.5px solid black;
              border-left: 1px solid #ddd;
              border-right: 1px solid #ddd;
              border-style: solid solid none solid;
              /* font-weight: bold */
            }

            tr.itemRegular td{
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
                padding-top: 20px;
                padding-bottom: 20px;
                text-align: center;
                background-color: #f64c4c;
                font-weight: bold;
                color: white;
            }

            </style>

            <script>
            // When the user clicks on <div>, open the popup
            function showPopup(pop) {
                var popup = document.getElementById(pop);
                popup.classList.toggle("show");
            }

            // Hides the relevant text when the checkbox is checked.
            function hideText(checkboxElem, rowID_num) {
              var row_size = document.getElementById('row_size_' + rowID_num)
              var row_amount = document.getElementById('row_amount_' + rowID_num)
              var row_toStore = document.getElementById('row_toStore_' + rowID_num)
              if (checkboxElem.checked) {
                row_size.style.opacity = 0;
                row_amount.style.opacity = 0;
                row_toStore.style.opacity = 0;
              } else {
                row_size.style.opacity = 1;
                row_amount.style.opacity = 1;
                row_toStore.style.opacity = 1;
              }
            }

            </script>

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
    def writeItemToFile(transfersFile, item, fromToStore, size, amount, shouldWriteInfo):
        toStore = fromToStore.toStore
        fromStore = fromToStore.fromStore
        isStockEmpty = item.isEmpty(toStore, size)
        sizesDict = CharSizesDict if item.code[0] == '3' or item.code[0] == 'A' else NumSizesDict
        size_repr = sizesDict[size]

        code = item.code if shouldWriteInfo else ""
        description = item.description if shouldWriteInfo else ""
        women_or_girls = item.age if shouldWriteInfo else ""
        color = item.color if shouldWriteInfo else ""
        emptyHighligt = "background-color:#f64c4c;" if isStockEmpty else ""
        firstRowBold = "itemHead" if shouldWriteInfo else "itemRegular"

        openRow = "\n<tr class='" + firstRowBold + "'>"
        checkbox_string = "\n\t<td><input type='checkbox' onchange=\"hideText(this, " + str(TransferList.num_of_items) +")\"></td>"
        code_string = "\n\t<td> " + code + "</td>"
        description_string = "\n\t<td>"+ description +"</td>"
        women_or_girls_string = "\n\t<td>" + women_or_girls + "</td>"
        color_string = "\n\t<td>"+ color +"</td>"
        size_string = "\n\t<td id='row_size_" + str(TransferList.num_of_items) + "'>" + size_repr +"</td>"
        amount_string = "\n\t<td id='row_amount_" + str(TransferList.num_of_items) + "' contenteditable='true'><font size='2'>" + str(item.initialStock[fromStore.value][size]) +"</font><b> / " + amount + "</b></td>"
        toStore_string = "\n\t<td id='row_toStore_" + str(TransferList.num_of_items) + "'>" + TransferList.getStoreHebrewName(toStore) + "</td>"
        emptyAlert_string = "\n\t<td style='width:4em; " + emptyHighligt + "' </td>"

        transfersFile.write(openRow.encode("utf8"))
        transfersFile.write(checkbox_string.encode("utf8"))
        transfersFile.write(code_string.encode("utf8"))
        transfersFile.write(description_string.encode("utf8"))
        transfersFile.write(women_or_girls_string.encode("utf8"))
        transfersFile.write(color_string.encode("utf8"))
        transfersFile.write(size_string.encode("utf8"))
        transfersFile.write(amount_string.encode("utf8"))
        transfersFile.write(toStore_string.encode("utf8"))
        TransferList.writeStockPopup(transfersFile, item)  # Writes the stock to Popup
        transfersFile.write(emptyAlert_string.encode("utf8"))
        return

    """
    Writes the HTML code to add a cell in table that conatins a Popup window of
    the initial stock.
    """
    def writeStockPopup(transfersFile, item):
        popUpHead = """
            \t<td>
            <div class="popup" onclick="showPopup('myPopup""" + str(TransferList.num_of_items) + """')">מלאי
             <span class="popuptext" id='myPopup""" + str(TransferList.num_of_items) + "' dir='ltr'>"

        popUpTail = """
        </span>
        </div>
        </td> """

        transfersFile.write(popUpHead.encode("utf8"))
        item.writeStockToFile(transfersFile)
        transfersFile.write(popUpTail.encode("utf8"))
        return


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
