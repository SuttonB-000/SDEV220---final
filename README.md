# Coffee Shop Inventory

Coffee shop inventory, a python based desktop app
to track coffee shop inventory. Two sample product types
are used, coffee and donuts, but more can be added by
the user.

This app includes low stock alerts, a filterable table
to display product types and a simple crud interface.

this app requires, tkinter, and TTKBootStrap, make 
sure both are installed and avaialble in the 
environment. To launch `python3 gui.py`

## Class Diagram

```mermaid
classDiagram
    class Inventory {
        +products: dict
        +add_product(product)
        +get_product(name)
        +get_product_names()
        +get_low_stock(threshold)
    }

    class coffee {
        +name
        +origin
        +roast
        +qty
        +unit
        +bestby
        +addStock(amount)
        +removeStock(amount)
        +getQty()
    }

    class donuts {
        +name
        +qty
        +bestby
        +addStock(amount)
        +removeStock(amount)
        +getQty()
    }

    Inventory "1" o-- "0..*" coffee : stores
    Inventory "1" o-- "0..*" donuts : stores
```

`Inventory` stores coffee and donut product objects, and each product manages its own stock quantity.
