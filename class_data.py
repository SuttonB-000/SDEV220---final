"""Product classes for the coffee shop inventory project."""


class coffee:
    """One coffee product and its current stock quantity."""

    def __init__(self, name, origin, roast, qty, unit, bestby):
        if qty < 0:
            raise ValueError("Starting quantity cannot be negative")
        self.name = name
        self.origin = origin
        self.roast = roast
        self.qty = qty
        self.unit = unit
        self.bestby = bestby

    def addStock(self, amount):
        if amount <= 0:
            raise ValueError("Quantity to add must be greater than zero")
        self.qty += amount
        return self.qty

    def removeStock(self, amount):
        if amount <= 0:
            raise ValueError("Quantity to remove must be greater than zero")
        if amount > self.qty:
            raise ValueError("Cannot remove more than the quantity on hand")
        self.qty -= amount
        return self.qty

    def getQty(self):
        return self.qty


class donuts:
    """One donut product and its current stock quantity."""

    def __init__(self, name, qty=0, bestby=7):
        if qty < 0:
            raise ValueError("Starting quantity cannot be negative")
        self.name = name
        self.qty = qty
        self.bestby = bestby

    def addStock(self, amount):
        if amount <= 0:
            raise ValueError("Quantity to add must be greater than zero")
        self.qty += amount
        return self.qty

    def removeStock(self, amount):
        if amount <= 0:
            raise ValueError("Quantity to remove must be greater than zero")
        if amount > self.qty:
            raise ValueError("Cannot remove more than the quantity on hand")
        self.qty -= amount
        return self.qty

    def getQty(self):
        return self.qty


class Inventory:
    """A collection of products managed by the coffee shop."""

    def __init__(self):
        self.products = {}

    def add_product(self, product):
        if product.name in self.products:
            raise ValueError(f"A product named '{product.name}' already exists")
        self.products[product.name] = product

    def get_product(self, name):
        try:
            return self.products[name]
        except KeyError:
            raise ValueError(f"Product '{name}' was not found") from None

    def get_product_names(self):
        return list(self.products.keys())

    def get_low_stock(self, threshold):
        if threshold < 0:
            raise ValueError("Low-stock threshold cannot be negative")
        return [
            product for product in self.products.values()
            if product.getQty() <= threshold
        ]
