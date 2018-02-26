from Item import Item
class WomenItem(Item):
    def __init__(self, code, description, color, isOneSize=False):
        super().__init__(code, description, color, isOneSize)
        self.age = "נשים"
        self.stock = [[0 for x in range(NUM_OF_SIZES)] for y in range(NUM_OF_STORES)]
        self.desired_stock = [[0 for x in range(NUM_OF_SIZES)] for y in range(NUM_OF_STORES)]
