from StudioEnums import TransferFromTo as tft
from StudioEnums import *
from collections import OrderedDict
import os

TABLE_HEADLINE_WAREHOUSE = """<tr>
    <th colspan="6">
    <h2>העברות למחסן</h2>
    </th>
    </tr>
    """

TABLE_HEADLINE_RISHPON = """<tr>
    <th colspan="6">
    <h2>העברות לרשפון</h2>
    </th>
    </tr>
    """

TABLE_HEADLINE_TACHANA = """<tr>
    <th colspan="6">
    <h2>העברות לתחנה</h2>
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
    """
    def exportTransfers(path):
        TransferList.exportSixTransfersList(path)
        directory = os.path.dirname(__file__)
        filename = os.path.join(directory, '')
        if not os.path.exists(filename + "/Transfers"):
            os.makedirs(filename + "/Transfers")
        TransferList.exportWarehouseTransfers(path)
        TransferList.exportRishponTransfers(path)
        TransferList.exportTachanaTransfers(path)
        TransferList.transfersDict = {}
        return

    """
    Merges the transfers from Warehouse to the other stores.
    The function creates a new file with all of the info and removes the temp files.
    """
    def exportWarehouseTransfers(path):
        warehouse_files = ['WarehouseRishpon.html', 'WarehouseTachana.html']
        with open('Transfers/WarehouseTransfers.html', "wb") as warehouse_transfers:
            TransferList.writeHeadOfFile(warehouse_transfers)
            with open(warehouse_files[0], encoding='utf8') as infile:
                TransferList.writeHeadlineTransferTo(warehouse_transfers, TABLE_HEADLINE_RISHPON, 'rishpon')
                for line in infile:  # Copys all of the first file into the new file
                    warehouse_transfers.write(line.encode('utf_8'))
            os.remove('WarehouseRishpon.html')
            with open(warehouse_files[1], encoding='utf8') as infile:
                TransferList.writeHeadlineTransferTo(warehouse_transfers, TABLE_HEADLINE_TACHANA, 'tachana')
                for line in infile:
                    warehouse_transfers.write(line.encode('utf_8'))
            os.remove('WarehouseTachana.html')
        return

    """
    Merges the transfers from Rishpon to the other stores.
    The function creates a new file with all of the info and removes the temp files.
    """
    def exportRishponTransfers(path):
        rishpon_files = ['RishponWarehouse.html', 'RishponTachana.html']
        with open('Transfers/RishponTransfers.html', "wb") as rishpon_transfers:
            TransferList.writeHeadOfFile(rishpon_transfers)

        #UnComment if transfer to Warehouse is needed

        #     with open(rishpon_files[0], encoding='utf8') as infile:
        #         TransferList.writeHeadlineTransferTo(rishpon_transfers, TABLE_HEADLINE_WAREHOUSE, 'warehouse')
        #         for line in infile:  # Copys all of the first file into the new file
        #             if line.startswith("<html>") or line.endswith("</html>"):
        #                 pass
        #             rishpon_transfers.write(line.encode('utf_8'))

            os.remove('RishponWarehouse.html')
            with open(rishpon_files[1], encoding='utf8') as infile:
                TransferList.writeHeadlineTransferTo(rishpon_transfers, TABLE_HEADLINE_TACHANA, 'tachana')
                for line in infile:  # Copys all of the first file into the new file
                    rishpon_transfers.write(line.encode('utf_8'))
            os.remove('RishponTachana.html')
        return

    """
    Merges the transfers from Tachana to the other stores.
    The function creates a new file with all of the info and removes the temp files.
    """
    def exportTachanaTransfers(path):
        tachana_files = ['TachanaWarehouse.html', 'TachanaRishpon.html']
        with open('Transfers/TachanaTransfers.html', "wb") as tachana_transfers:
            TransferList.writeHeadOfFile(tachana_transfers)

        #UnComment if transfer to Warehouse is needed

        #     with open(tachana_files[0], encoding='utf8') as infile:
        #         TransferList.writeHeadlineTransferTo(tachana_transfers, TABLE_HEADLINE_WAREHOUSE, 'warehouse')
        #         for line in infile:  # Copys all of the first file into the new file
        #             if line.startswith("<html>") or line.endswith("</html>"):
        #                 pass
        #             tachana_transfers.write(line.encode('utf_8'))

            os.remove('TachanaWarehouse.html')
            with open(tachana_files[1], encoding='utf8') as infile:
                TransferList.writeHeadlineTransferTo(tachana_transfers, TABLE_HEADLINE_RISHPON, 'rishpon')
                for line in infile:  # Copys all of the first file into the new file
                    tachana_transfers.write(line.encode('utf_8'))
            os.remove('TachanaRishpon.html')
        return

    """
    Creates 6 different files - each file holds transfers from one store to another.
    """
    def exportSixTransfersList(path):
        fileW2R = open('WarehouseRishpon.html', 'wb')
        fileW2T = open('WarehouseTachana.html', 'wb')
        fileR2W = open('RishponWarehouse.html', 'wb')
        fileR2T = open('RishponTachana.html', 'wb')
        fileT2W = open('TachanaWarehouse.html', 'wb')
        fileT2R = open('TachanaRishpon.html', 'wb')
        transfers = TransferList.transfersDict
        for item in transfers:              # Iterate over all of the items
            for fromTo in transfers[item]:  # Iterate over all of the transfers for that item.
                shouldWriteInfo = True      # Indicates whether or not this is the first transfer of the item.
                for i in range(len(transfers[item][fromTo])):  # Iterate over all of the sizes.
                    amount = transfers[item][fromTo][i]
                    if amount > 0:
                        amount = str(amount)
                        if fromTo == tft.WAREHOUSE_TO_RISHPON:
                            TransferList.writeItemToFile(fileW2R, item, Sizes(i).name, amount, shouldWriteInfo)
                        elif fromTo == tft.WAREHOUSE_TO_TACHANA:
                            TransferList.writeItemToFile(fileW2T, item, Sizes(i).name, amount, shouldWriteInfo)
                        elif fromTo == tft.RISHPON_TO_WAREHOUSE:
                            TransferList.writeItemToFile(fileR2W, item, Sizes(i).name, amount, shouldWriteInfo)
                        elif fromTo == tft.RISHPON_TO_TACHANA:
                            TransferList.writeItemToFile(fileR2T, item, Sizes(i).name, amount, shouldWriteInfo)
                        elif fromTo == tft.TACHANA_TO_WAREHOUSE:
                            TransferList.writeItemToFile(fileT2W, item, Sizes(i).name, amount, shouldWriteInfo)
                        elif fromTo == tft.TACHANA_TO_RISHPON:
                            TransferList.writeItemToFile(fileT2R, item, Sizes(i).name, amount, shouldWriteInfo)
                        shouldWriteInfo = False   # If the amount to transfer is positive.
        fileR2T.close()
        fileT2R.close()
        fileR2W.close()
        fileT2W.close()
        fileW2R.close()
        fileW2T.close()

    """
    Writes the styles and headers to the final HTML output file.
    """
    def writeHeadOfFile(transfers_file):
        transfers_file.write("<html> <body dir='rtl'>\n".encode('utf8'))
        transfers_file.write("<?php header('Content-Type: text/html; charset=utf-8'); ?>\n".encode('utf8'))
        transfers_file.write("<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />\n".encode('utf8'))
        transfers_file.write("""
            <head>
            <style>
            h2 {
              color: #111;
              font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
              color: white;
              font-size: 30px;
              font-weight: 300;
              line-height: 32px;
              font-weight: bold;
              text-decoration: underline;
              margin: 0 0 3px;
              text-align: center;
            }

            #rishpon {
                font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }

            #rishpon td, #rishpon th {
                border: 1px solid #ddd;
                padding: 8px;
            }

            #rishpon tr:nth-child(even){background-color: #f2f2f2;}

            #rishpon tr:hover {background-color: #bfbfbf;}

            #rishpon th {
                padding-top: 12px;
                padding-bottom: 12px;
                text-align: right;
                background-color: #f64c4c;
                font-weight: bold;
                text-decoration: underline;
                color: white;
            }

            #tachana {
              font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
              border-collapse: collapse;
              width: 100%;
            }

            #tachana td, #tachana th {
                border: 1px solid #ddd;
                padding: 8px;
            }

            #tachana tr:nth-child(even){background-color: #f2f2f2;}

            #tachana tr:hover {background-color: #bfbfbf;}

            #tachana th {
                padding-top: 12px;
                padding-bottom: 12px;
                text-align: right;
                background-color: #f64c4c;
                color: white;
            }

            </style>
            </head>""".encode('utf8'))

    """
    Writes the HTML code to write the next code into the correct table.
    toWhereHeadLine must be one of the HEADLINE constants of this class.
    toWhereEnglish must be one of the following: 'rishpon', 'tachana', 'warehouse'.
    """
    def writeHeadlineTransferTo(transfers_file, toWhereHeadLine, toWhereEnglish):
        tableHTMLString = "<table id='" + toWhereEnglish + "'>"
        transfers_file.write(tableHTMLString.encode('utf8'))
        transfers_file.write(toWhereHeadLine.encode('utf8'))
        transfers_file.write(TABLE_PROPERTIES.encode('utf8'))

    """
    Writes the item representation as a row in an HTML table.
    If shouldWriteInfo is True, than this is the first row of the given item and
    all of its data should be written in the table, else the info is empty.
    """
    def writeItemToFile(transfersFile, item, size, amount, shouldWriteInfo):
        description = item.description if shouldWriteInfo else ""
        women_or_girls = ("נשים" if item.code[0] == '3' else "ילדות") if shouldWriteInfo else ""
        color = item.color if shouldWriteInfo else ""
        openRow = "<tr bgcolor=#ffffff>" if shouldWriteInfo else "<tr>"  # Highlight the first row of an item

        description_string = "\t<td>"+ description +"</td>"
        women_or_girls_string = "\t<td>" + women_or_girls + "</td>"
        color_string = "\t<td>"+ color +"</td>"
        size_string = "\t<td>"+ size +"</td>"
        amount_string = "\t<td>"+ amount +"</td>"

        transfersFile.write(openRow.encode('utf8'))
        transfersFile.write("\t<td><input type='checkbox'></td>".encode('utf8'))
        transfersFile.write(description_string.encode('utf8'))
        transfersFile.write(women_or_girls_string.encode('utf8'))
        transfersFile.write(color_string.encode('utf8'))
        transfersFile.write(size_string.encode('utf8'))
        transfersFile.write(amount_string.encode('utf8'))


# Tests
# item = Item(211, "סקיני פרינט" ,66)
# TransferList.add_transfer(item,tft.WAREHOUSE_TO_RISHPON, tft.RISHPON_TO_WAREHOUSE ,3,4)
# TransferList.add_transfer(item,tft.WAREHOUSE_TO_RISHPON, tft.RISHPON_TO_WAREHOUSE,2,4)
# TransferList.add_transfer(item,tft.TACHANA_TO_RISHPON, tft.RISHPON_TO_TACHANA,3,4)
# TransferList.exportTransfers(2)
