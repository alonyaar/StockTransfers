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
        warehouse_files = ['WarehouseRishpon.txt', 'WarehouseTachana.txt']
        with open('Transfers/WarehouseTransfers.txt', "wb") as warehouse_transfers:
            warehouse_transfers.write("\n============================================\n".encode('utf8'))
            with open(warehouse_files[0], encoding='utf8') as infile:
                warehouse_transfers.write(":העברות לרשפון\n\n".encode('utf8'))
                for line in infile:
                    warehouse_transfers.write(line.encode('utf_8'))
            os.remove('WarehouseRishpon.txt')
            with open(warehouse_files[1], encoding='utf8') as infile:
                warehouse_transfers.write("\n============================================".encode('utf8'))
                warehouse_transfers.write("\n:העברות לתחנה\n\n".encode('utf8'))
                for line in infile:
                    warehouse_transfers.write(line.encode('utf_8'))
            os.remove('WarehouseTachana.txt')
            warehouse_transfers.write("\n============================================".encode('utf8'))
        return

    """
    Merges the transfers from Rishpon to the other stores.
    The function creates a new file with all of the info and removes the temp files.
    """
    def exportRishponTransfers(path):
        rishpon_files = ['RishponWarehouse.txt', 'RishponTachana.txt']
        with open('Transfers/RishponTransfers.txt', "wb") as rishpon_transfers:
            # with open(rishpon_files[0], encoding='utf8') as infile:
            #     rishpon_transfers.write(":העברות למחסן\n\n".encode('utf8'))
            #     for line in infile:
            #         rishpon_transfers.write(line.encode('utf_8'))
            os.remove('RishponWarehouse.txt')
            with open(rishpon_files[1], encoding='utf8') as infile:
                rishpon_transfers.write("\n============================================".encode('utf8'))
                rishpon_transfers.write("\n:העברות לתחנה\n\n".encode('utf8'))
                for line in infile:
                    rishpon_transfers.write(line.encode('utf_8'))
            os.remove('RishponTachana.txt')
            rishpon_transfers.write("\n============================================".encode('utf8'))
        return

    """
    Merges the transfers from Tachana to the other stores.
    The function creates a new file with all of the info and removes the temp files.
    """
    def exportTachanaTransfers(path):
        tachana_files = ['TachanaWarehouse.txt', 'TachanaRishpon.txt']
        with open('Transfers/TachanaTransfers.txt', "wb") as tachana_transfers:
            # with open(tachana_files[0], encoding='utf8') as infile:
            #     tachana_transfers.write("\n:העברות למחסן\n\n".encode('utf8'))
            #     for line in infile:
            #         tachana_transfers.write(line.encode('utf_8'))
            os.remove('TachanaWarehouse.txt')
            with open(tachana_files[1], encoding='utf8') as infile:
                tachana_transfers.write("\n============================================".encode('utf8'))
                tachana_transfers.write("\n:העברות לרשפון\n\n".encode('utf8'))
                for line in infile:
                    tachana_transfers.write(line.encode('utf_8'))
            os.remove('TachanaRishpon.txt')
            tachana_transfers.write("\n============================================".encode('utf8'))
        return

    """
    Creates 6 different files - each file holds transfers from one store to another.
    """
    def exportSixTransfersList(path):
        fileWarehouseRishpon = open('WarehouseRishpon.txt', 'wb')
        fileWarehouseTachana = open('WarehouseTachana.txt', 'wb')
        fileRishponWarehouse = open('RishponWarehouse.txt', 'wb')
        fileRishponTachana = open('RishponTachana.txt', 'wb')
        fileTachanaWarehouse = open('TachanaWarehouse.txt', 'wb')
        fileTachanaRishpon = open('TachanaRishpon.txt', 'wb')
        transfers = TransferList.transfersDict
        for item in transfers:
            for fromTo in transfers[item]:
                for i in range(len(transfers[item][fromTo])):
                    size = transfers[item][fromTo][i]
                    if size > 0:
                        toWrite = " העברה של" + " " + str(size) + " " + item.description + " " + item.age + " בצבע " + str(item.color) + " במידה "
                        toWrite = Sizes(i).name + toWrite + "\n"
                        if fromTo == tft.WAREHOUSE_TO_RISHPON:
                            fileWarehouseRishpon.write(toWrite.encode('utf8'))
                        elif fromTo == tft.WAREHOUSE_TO_TACHANA:
                            fileWarehouseTachana.write(toWrite.encode('utf8'))
                        elif fromTo == tft.RISHPON_TO_WAREHOUSE:
                            fileRishponWarehouse.write(toWrite.encode('utf8'))
                        elif fromTo == tft.RISHPON_TO_TACHANA:
                            fileRishponTachana.write(toWrite.encode('utf8'))
                        elif fromTo == tft.TACHANA_TO_WAREHOUSE:
                            fileTachanaWarehouse.write(toWrite.encode('utf8'))
                        elif fromTo == tft.TACHANA_TO_RISHPON:
                            fileTachanaRishpon.write(toWrite.encode('utf8'))
        fileRishponTachana.close()
        fileTachanaRishpon.close()
        fileRishponWarehouse.close()
        fileTachanaWarehouse.close()
        fileWarehouseRishpon.close()
        fileWarehouseTachana.close()

# Tests
# item = Item(211, "סקיני פרינט" ,66)
# TransferList.add_transfer(item,tft.WAREHOUSE_TO_RISHPON, tft.RISHPON_TO_WAREHOUSE ,3,4)
# TransferList.add_transfer(item,tft.WAREHOUSE_TO_RISHPON, tft.RISHPON_TO_WAREHOUSE,2,4)
# TransferList.add_transfer(item,tft.TACHANA_TO_RISHPON, tft.RISHPON_TO_TACHANA,3,4)
# TransferList.exportTransfers(2)
