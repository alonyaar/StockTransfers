from StudioEnums import TransferFromTo as tft
from StudioEnums import *
import os

"""
This class is a 'static' class that holds all of the transfers that should be carried out.
"""
class TransferList:

    transfersDict = {}

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
            transfers[item][transferFromTo] = [0,0,0,0,0,0]

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
                    transfers[item][TransferFromTo.WAREHOUSE_TO_TACHANA] = [0,0,0,0,0,0]
                transfers[item][warehouse_to_rishpon][size] -= 1
                transfers[item][TransferFromTo.WAREHOUSE_TO_TACHANA][size] += 1
                return

        if transferFromTo == TransferFromTo.TACHANA_TO_RISHPON:
            warehouse_to_tachana = TransferFromTo.WAREHOUSE_TO_TACHANA
            if warehouse_to_tachana in transfers[item] and transfers[item][warehouse_to_tachana][size] > 0:
                if TransferFromTo.WAREHOUSE_TO_RISHPON not in transfers[item]:
                    transfers[item][TransferFromTo.WAREHOUSE_TO_RISHPON] = [0,0,0,0,0,0]
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
            warehouse_transfers.write("<html> <body dir='rtl'>".encode('utf8'))
            with open(warehouse_files[0], encoding='utf8') as infile:
                TransferList.writeHeadlineTransferTo(warehouse_transfers, "רשפון")
                for line in infile:  # Copys all of the first file into the new file
                    if line.startswith("<html>") or line.endswith("</html>"):
                        pass
                    warehouse_transfers.write(line.encode('utf_8'))
            os.remove('WarehouseRishpon.html')
            with open(warehouse_files[1], encoding='utf8') as infile:
                TransferList.writeHeadlineTransferTo(warehouse_transfers, "תחנה")
                for line in infile:
                    if line.startswith("<html>") or line.endswith("</html>"):
                        pass
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

        #UnComment if transfer to Warehouse is needed

        #     with open(rishpon_files[0], encoding='utf8') as infile:
        #         TransferList.writeHeadlineTransferTo(rishpon_transfers, "מחסן")
        #         for line in infile:  # Copys all of the first file into the new file
        #             if line.startswith("<html>") or line.endswith("</html>"):
        #                 pass
        #             rishpon_transfers.write(line.encode('utf_8'))

            os.remove('RishponWarehouse.html')
            with open(rishpon_files[1], encoding='utf8') as infile:
                TransferList.writeHeadlineTransferTo(rishpon_transfers, "תחנה")
                for line in infile:  # Copys all of the first file into the new file
                    if line.startswith("<html>") or line.endswith("</html>"):
                        pass
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

        #UnComment if transfer to Warehouse is needed

        #     with open(tachana_files[0], encoding='utf8') as infile:
        #         TransferList.writeHeadlineTransferTo(tachana_transfers, "מחסן")
        #         for line in infile:  # Copys all of the first file into the new file
        #             if line.startswith("<html>") or line.endswith("</html>"):
        #                 pass
        #             tachana_transfers.write(line.encode('utf_8'))

            os.remove('TachanaWarehouse.html')
            with open(tachana_files[1], encoding='utf8') as infile:
                TransferList.writeHeadlineTransferTo(tachana_transfers, "רשפון")
                for line in infile:  # Copys all of the first file into the new file
                    if line.startswith("<html>") or line.endswith("</html>"):
                        pass
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
        TransferList.writeHtmlHeader(fileW2R, fileW2T, fileR2W, fileR2T, fileT2W, fileT2R)
        transfers = TransferList.transfersDict
        for item in transfers:
            for fromTo in transfers[item]:
                for i in range(len(transfers[item][fromTo])):
                    amount = transfers[item][fromTo][i]
                    if amount > 0:
                        toWrite = "<p><input type='checkbox'> העברה של " + str(amount) + " " + item.description + " " + item.age + " בצבע " + str(item.color) + " במידה " + Sizes(i).name + "</p>\n"
                        if fromTo == tft.WAREHOUSE_TO_RISHPON:
                            fileW2R.write(toWrite.encode('utf8'))
                        elif fromTo == tft.WAREHOUSE_TO_TACHANA:
                            fileW2T.write(toWrite.encode('utf8'))
                        elif fromTo == tft.RISHPON_TO_WAREHOUSE:
                            fileR2W.write(toWrite.encode('utf8'))
                        elif fromTo == tft.RISHPON_TO_TACHANA:
                            fileR2T.write(toWrite.encode('utf8'))
                        elif fromTo == tft.TACHANA_TO_WAREHOUSE:
                            fileT2W.write(toWrite.encode('utf8'))
                        elif fromTo == tft.TACHANA_TO_RISHPON:
                            fileT2R.write(toWrite.encode('utf8'))
        TransferList.writeHtmlFooter(fileW2R, fileW2T, fileR2W, fileR2T, fileT2W, fileT2R)
        fileR2T.close()
        fileT2R.close()
        fileR2W.close()
        fileT2W.close()
        fileW2R.close()
        fileW2T.close()


    def writeHtmlHeader(w2r, w2t, r2w, r2t, t2w, t2r):
        string = "<html> <body dir='rtl'>\n"
        w2r.write(string.encode('utf8'))
        w2t.write(string.encode('utf8'))
        r2w.write(string.encode('utf8'))
        r2t.write(string.encode('utf8'))
        t2w.write(string.encode('utf8'))
        t2r.write(string.encode('utf8'))
    def writeHtmlFooter(w2r, w2t, r2w, r2t, t2w, t2r):
        string = "</body></html>"
        w2r.write(string.encode('utf8'))
        w2t.write(string.encode('utf8'))
        r2w.write(string.encode('utf8'))
        r2t.write(string.encode('utf8'))
        t2w.write(string.encode('utf8'))
        t2r.write(string.encode('utf8'))

    def writeHeadlineTransferTo(file, toWhere):
        file.write("<p><b>==================================</b></p>".encode('utf8'))
        transferString = "<p><b>" + "העברות ל"+ toWhere + "</b></p>"
        file.write(transferString.encode('utf8'))
        file.write("<p><b>==================================</b></p>".encode('utf8'))

# Tests
# item = Item(211, "סקיני פרינט" ,66)
# TransferList.add_transfer(item,tft.WAREHOUSE_TO_RISHPON, tft.RISHPON_TO_WAREHOUSE ,3,4)
# TransferList.add_transfer(item,tft.WAREHOUSE_TO_RISHPON, tft.RISHPON_TO_WAREHOUSE,2,4)
# TransferList.add_transfer(item,tft.TACHANA_TO_RISHPON, tft.RISHPON_TO_TACHANA,3,4)
# TransferList.exportTransfers(2)
