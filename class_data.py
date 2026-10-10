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
    def addStock(self, amount):
        if amount <= 0:
            raise ValueError('Quantity must be more than 0')
        self.qty += amount

    # remove stock on hand
    def removeStock(self, amount):
        if amount > self.qty:
            raise ValueError('Value must be less than whats on hand')
        if amount <= 0:
            raise ValueError('Value must be more than zero')
        self.qty -= amount

    # check quantity
    def getQty(self):
        return self.qty

class donuts:
    def __init__(self, name, qty=0, bestby=7):
        self.name = name
        self.qty = qty
        self.bestby = bestby

    def addStock(self, amount):
        if amount <= 0:
            raise ValueError('Quantity must be more than 0')

        self.qty += amount
        return self.qty

    def removeStock(self,amount):
        if amount <= 0:
            raise ValueError('quanity must be more than zero')
        if amount >= self.qty:
            raise ValueError('quantity cant be more than whats on hand')
            

