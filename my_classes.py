'''Classes related to SDEV 220 - final project'''

# is one coffee product not full inventory
class coffee:
    def __init__(self, name, origin, roast, qty, unit, bestby):
    # this will run automatically anytime a new coffee is added
        self.name = name
        self.origin = origin
        self.roast = roast
        self.qty = qty
        self.unit = unit
        self.bestby = bestby

    # add qty on hand
    def addStock(self, amount, unit):
        self.qty += amount
        self.unit = unit

    # remove stock on hand
    def removeStock(self, amount):
        if amount <= self.quantity:
            self.qty -= amount
        else:
            print('Not enough in stock')

    # check quantity
    def getQty(self):
        return self.quantity

