from enum import Enum

NUM_OF_SIZES_WOMEN = 6
NUM_OF_SIZES_GIRLS = 11
NUM_OF_STORES = 3

class Stores(Enum):
    WAREHOUSE = 0
    RISHPON = 1
    TACHANA = 2

    """
    The function gets the store number as it represented in the business system
    and returns its representation as an enum.
    """
    def getStore(storeRepr):
        if storeRepr == 1:
            return Stores.WAREHOUSE
        elif storeRepr == 10:
            return Stores.RISHPON
        elif storeRepr == 12:
            return Stores.TACHANA

class WomenSizes(Enum):
    W = 5
    XL = 4
    L = 3
    M = 2
    S = 1
    XS = 0

class EventsSizes(Enum):
    XXS = 0
    XS = 1
    S = 2
    M = 3
    L = 4
    XL = 5
    XXL = 6
    Y = 7
    W = 8

class TransferFromTo(Enum):
    WAREHOUSE_TO_RISHPON = (Stores.WAREHOUSE, Stores.RISHPON, None)
    WAREHOUSE_TO_TACHANA = (Stores.WAREHOUSE, Stores.TACHANA, None)
    RISHPON_TO_WAREHOUSE = (Stores.RISHPON, Stores.WAREHOUSE, None)
    RISHPON_TO_TACHANA = (Stores.RISHPON, Stores.TACHANA, None)
    TACHANA_TO_WAREHOUSE = (Stores.TACHANA, Stores.WAREHOUSE, None)
    TACHANA_TO_RISHPON = (Stores.TACHANA, Stores.RISHPON, None)

    def __init__(self, fromStore, toStore, oppositeDirection):
        self.fromStore = fromStore
        self.toStore = toStore
        self.toFrom = oppositeDirection
        return

    def updateToFromDirections():
        TransferFromTo.WAREHOUSE_TO_RISHPON.toFrom = TransferFromTo.RISHPON_TO_WAREHOUSE
        TransferFromTo.WAREHOUSE_TO_TACHANA.toFrom = TransferFromTo.TACHANA_TO_WAREHOUSE
        TransferFromTo.RISHPON_TO_WAREHOUSE.toFrom = TransferFromTo.WAREHOUSE_TO_RISHPON
        TransferFromTo.RISHPON_TO_TACHANA.toFrom = TransferFromTo.TACHANA_TO_RISHPON
        TransferFromTo.TACHANA_TO_WAREHOUSE.toFrom = TransferFromTo.WAREHOUSE_TO_TACHANA
        TransferFromTo.TACHANA_TO_RISHPON.toFrom = TransferFromTo.RISHPON_TO_TACHANA
        return

WomenSizesDict = {0:"XS", 1: "S", 2:"M", 3:"L", 4:"XL", 5:"W"}
GirlsSizesDict = {0:"01", 1: "02", 2:"04", 3:"06", 4:"08", 5:"10", 6:"12", 7:"14", 8:"16", 9:"18", 10:"20"}
EventsSizesDict = {0:"XXS", 1: "XS", 2:"S", 3:"M", 4:"L", 5:"XL", 6:"XL", 7:"Y", 8:"W"}

# ColorsDict = {'01':'לבן',
#               '02':'שמנת',
#               '03':'בז׳',
#               '04':'מוקה',
#               '05':'אבן',
#               '06':'חאקי',
#               '07':'חום',
#               '08':'מחולק חאקי',
#               '09':'חציל',
#               '10':'כחול',
#               '100':'ג׳ינס בהיר',
#               '101':'זית כהה',
#               '11':'נייבי',
#               '12':'תכלת',
#               '13':'ג׳ינס',
#               '14':'טורקיז',
#               '15':'תכלת מלנז׳',
#               '16':'לורקס בהיר',
#               '17':'לורקס כהה',
#               '18':'קרם',
#               '19':'כחול מחולק',
#               '20':'ירוק',
#               '21':'זית',
#               '22':'בקבוק',
#               '23':'קיווי',
#               '24':'ליים',
#               '25':'אפור בהיר',
#               '26':'בטיק',
#               '27':'אפור כהה',
#               '28':'שחור מט',
#               '29':'נחש',
#               '30':'אדום',
#               '31':'כתום',
#               '32':'צהוב',
#               '33':'חרדל',
#               '34':'ורוד',
#               '35':'בזוקה',
#               '36':'פוקסיה',
#               '37':'צבעוני',
#               '38':'כתום מלאנז׳',
#               '39':'סקרלט',
#               '40':'אפרסק',
#               '41':'כחול פסים',
#               '42':'שחור פסים',
#               '43':'כחול ים',
#               '44':'פרחוני',
#               '45':'מנומר בהיר',
#               '46':'ורוד עתיק',
#               '47':'שחור מודפס',
#               '48':'כחול כהה',
#               '49':'נייבי מחולק',
#               '50':'מרנגו מחולק',
#               '51':'פטרול',
#               '52':'שחור משולב',
#               '53':'בורדו',
#               '54':'קאמל',
#               '55':'מנטה',
#               '56':'זית מחולק',
#               '57':'פודרה',
#               '58':'כחול מודפס',
#               '59':'מודפס',
#               '60':'אפור',
#               '61':'אפור מלנז׳',
#               '62':'מלנז׳ בהיר',
#               '63':'מלנז׳ כהה',
#               '64':'אפור עכבר',
#               '65':'מרנגו',
#               '66':'שחור',
#               '67':'סגול לילך',
#               '68':'זהב',
#               '69':'כסף',
#               '70':'לבן חלק',
#               '71':'שחור לבן',
#               '72':'לבן מבריק',
#               '73':'שחור רקום',
#               '74':'ורוד בייבי',
#               '75':'ג׳ינס שחור',
#               '76':'ג׳ינס מחולק',
#               '77':'לבן מחולק',
#               '78':'ורוק חולק',
#               '79':'ורוד כהה',
#               '80':'קורל',
#               '81':'בייבי מחולק',
#               '82':'קקאו',
#               '83':'ג׳ינס כהה',
#               '84':'אפור מטליק',
#               '85':'שחור מבריק',
#               '86':'ג׳ינס דק שחור',
#               '87':'ג׳ינס דק כחול',
#               '88':'לבן רקום',
#               '89':'לבן מודפס',
#               '90':'שחור מחולק',
#               '91':'מרנגו כהה',
#               '92':'חום בהיר',
#               '93':'ברונזה',
#               '94':'שחור משופשף',
#               '95':'אפור מבריק',
#               '96':'חום כהה',
#               '97':'אפור מחולק',
#               '98':'סגול',
#               '99':'מנומר',
#               "":""
#               }
