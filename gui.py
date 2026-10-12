import tkinter as tk
from datetime import datetime
from tkinter import messagebox
import ttkbootstrap as ttk
from class_data import Inventory, coffee, donuts

LOW_STOCK_THRESHOLD = 5

#window start
window = ttk.Window(themename="minty-dark")
window.title('Coffee Shop Inventory')
window.geometry('760x700')
window.minsize(680, 620)

# window label
title_label = ttk.Label(window, text='Coffee Shop Inventory', font=('Arial', 24, 'bold'))
title_label.pack(pady=20)

table_filter = tk.StringVar(value="All Products")
filter_frame = ttk.Frame(window, padding=(16, 8))
filter_frame.pack(pady=(0, 5))
ttk.Label(filter_frame, text="Show:").pack(side="left", padx=(0, 5))
table_filter_selector = ttk.Combobox(
    filter_frame,
    textvariable=table_filter,
    values=("All Products", "Coffee", "Donuts"),
    state="readonly",
    width=14,
)
table_filter_selector.pack(side="left")

# Inventory table skeleton. Product rows will be added in a later step.
inventory_columns = ("type", "name", "quantity", "unit", "best_by")
inventory_table = ttk.Treeview(
    window,
    columns=inventory_columns,
    show="headings",
    height=6,
)

inventory_table.heading("type", text="Product Type")
inventory_table.heading("name", text="Product Name")
inventory_table.heading("quantity", text="Quantity")
inventory_table.heading("unit", text="Unit")
inventory_table.heading("best_by", text="Best By")

inventory_table.column("type", width=110, anchor="center")
inventory_table.column("name", width=180)
inventory_table.column("quantity", width=90, anchor="center")
inventory_table.column("unit", width=90, anchor="center")
inventory_table.column("best_by", width=120, anchor="center")

inventory_table.pack(fill="x", padx=20, pady=(0, 15))
style = ttk.Style()
style.configure("Treeview", rowheight=30, font=("Arial", 11))
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
inventory_table.tag_configure("low_stock", foreground="#ff8a80")

#test objects
house_blend = coffee(
    'House Blend',
    'Columbia',
    'Medium',
    12,
    'bags',
    '2027-01-01'
)

glazed_donut = donuts(
    'Glazed Donut',
    18,
    "2026-10-12"
)

espresso_roast = coffee(
    'Espresso Roast',
    'Brazil',
    'Dark',
    8,
    'bags',
    '2027-02-15'
)

decaf_blend = coffee(
    'Decaf Blend',
    'Peru',
    'Medium',
    6,
    'bags',
    '2027-03-01'
)

chocolate_donut = donuts(
    'Chocolate Donut',
    14,
    '2026-10-12'
)

blueberry_donut = donuts(
    'Blueberry Donut',
    10,
    '2026-10-12'
)

# Inventory object stores the products in a dictionary.
inventory = Inventory()
inventory.add_product(house_blend)
inventory.add_product(glazed_donut)
inventory.add_product(espresso_roast)
inventory.add_product(decaf_blend)
inventory.add_product(chocolate_donut)
inventory.add_product(blueberry_donut)

low_stock_label = ttk.Label(window, text="", bootstyle="danger")
low_stock_label.pack(pady=5)

status_label = ttk.Label(window, text="", bootstyle="secondary")
status_label.pack(pady=5)

# product selector and quantity entry
selected_product = tk.StringVar(value='House Blend')

input_frame = ttk.Frame(window, padding=12)
input_frame.pack(pady=10)

ttk.Label(input_frame, text='Select a product:').grid(
    row=0, column=0, sticky='w', padx=(0, 8), pady=5
)

product_selector = ttk.Combobox(
    input_frame,
    textvariable=selected_product,
    values=inventory.get_product_names(),
    state="readonly",
    width=22,
)
product_selector.grid(row=0, column=1, sticky='w', pady=5)

ttk.Label(input_frame, text='Quantity to add or remove:').grid(
    row=1, column=0, sticky='w', padx=(0, 8), pady=5
)

quantity_entry = ttk.Entry(input_frame, width=25)
quantity_entry.grid(row=1, column=1, sticky='w', pady=5)

# Validate the selected product and quantity.
def get_selected_product_and_amount():
    product = inventory.get_product(selected_product.get())

    try:
        amount = int(quantity_entry.get())
    except ValueError:
        raise ValueError('Enter a whole-number quantity.') from None

    if amount <= 0:
        raise ValueError('Quantity must be greater than zero')

    return product, amount

# wiring up gui to manipulate stock data

def add_stock():
    try:
        product, amount = get_selected_product_and_amount()
        product.addStock(amount)
        refresh_stock_labels()
        refresh_inventory_table()
        status_label.config(text=f"Added {amount} to {product.name}.")
        quantity_entry.delete(0, tk.END)
    except ValueError as error:
        messagebox.showerror("Cannot add stock", str(error))

def remove_stock():
    try:
        product, amount = get_selected_product_and_amount()
        product.removeStock(amount)
        refresh_stock_labels()
        refresh_inventory_table()
        status_label.config(text=f"Removed {amount} from {product.name}.")
        quantity_entry.delete(0, tk.END)
    except ValueError as error:
        messagebox.showerror('Cannot remove stock', str(error))


def refresh_stock_labels(event=None):
    product = inventory.get_product(selected_product.get())
    low_stock_products = inventory.get_low_stock(LOW_STOCK_THRESHOLD)
    if product in low_stock_products:
        low_stock_label.config(
            text=f"Low stock: {product.name} has {product.getQty()} remaining."
        )
    else:
        low_stock_label.config(text="")


def format_best_by(best_by):
    """Format YYYY-MM-DD for display without changing the stored value."""
    try:
        return datetime.strptime(str(best_by), "%Y-%m-%d").strftime("%m/%d/%Y")
    except ValueError:
        return str(best_by)


def format_donut_quantity(quantity):
    """Show quantities above one dozen as dozens plus individual donuts."""
    if quantity <= 12:
        return str(quantity)

    dozens, individuals = divmod(quantity, 12)
    return f"{dozens} dzn {individuals} indiv"


def refresh_inventory_table(event=None):
    # Remove the rows currently displayed in the table.
    for row_id in inventory_table.get_children():
        inventory_table.delete(row_id)

    # Group coffee products together, then donut products, by name.
    products_to_display = sorted(
        inventory.products.values(),
        key=lambda product: (
            0 if isinstance(product, coffee) else 1,
            product.name,
        ),
    )

    # Add the products that match the selected filter.
    for product in products_to_display:
        if isinstance(product, coffee):
            product_type = "Coffee"
            quantity = product.getQty()
            unit = product.unit
        else:
            product_type = "Donut"
            quantity = format_donut_quantity(product.getQty())
            unit = "" if product.getQty() > 12 else "indiv"

        if table_filter.get() == "Coffee" and product_type != "Coffee":
            continue
        if table_filter.get() == "Donuts" and product_type != "Donut":
            continue

        tags = ("low_stock",) if product.getQty() <= LOW_STOCK_THRESHOLD else ()
        inventory_table.insert(
            "",
            "end",
            values=(
                product_type,
                product.name,
                quantity,
                unit,
                format_best_by(product.bestby),
            ),
            tags=tags,
        )


def open_add_product_form():
    form = ttk.Toplevel(window)
    form.title("Add Product")
    form.geometry("380x430")
    form.transient(window)

    product_type = tk.StringVar(value="Coffee")
    fields = {}

    ttk.Label(form, text="Product type:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    type_selector = ttk.Combobox(
        form,
        textvariable=product_type,
        values=("Coffee", "Donut"),
        state="readonly",
    )
    type_selector.grid(row=0, column=1, padx=10, pady=5)

    def add_field(row, label_text, field_name):
        ttk.Label(form, text=label_text).grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry = ttk.Entry(form)
        entry.grid(row=row, column=1, padx=10, pady=5)
        fields[field_name] = entry

    add_field(1, "Name:", "name")
    add_field(2, "Starting quantity:", "quantity")
    add_field(3, "Best-by date:", "bestby")

    coffee_fields = ttk.Frame(form)
    coffee_fields.grid(row=4, column=0, columnspan=2, sticky="ew")

    ttk.Label(coffee_fields, text="Origin:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    fields["origin"] = ttk.Entry(coffee_fields)
    fields["origin"].grid(row=0, column=1, padx=10, pady=5)
    ttk.Label(coffee_fields, text="Roast:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    fields["roast"] = ttk.Entry(coffee_fields)
    fields["roast"].grid(row=1, column=1, padx=10, pady=5)
    ttk.Label(coffee_fields, text="Unit:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    fields["unit"] = ttk.Entry(coffee_fields)
    fields["unit"].grid(row=2, column=1, padx=10, pady=5)

    def update_type_fields(event=None):
        if product_type.get() == "Coffee":
            coffee_fields.grid()
        else:
            coffee_fields.grid_remove()

    type_selector.bind("<<ComboboxSelected>>", update_type_fields)
    update_type_fields()

    def save_product():
        name = fields["name"].get().strip()
        bestby = fields["bestby"].get().strip()
        if not name or not bestby:
            messagebox.showerror("Missing information", "Enter a product name and best-by date.", parent=form)
            return

        try:
            quantity = int(fields["quantity"].get())
        except ValueError:
            messagebox.showerror("Invalid quantity", "Enter a whole-number starting quantity.", parent=form)
            return

        if quantity < 0:
            messagebox.showerror("Invalid quantity", "Starting quantity cannot be negative.", parent=form)
            return

        try:
            if product_type.get() == "Coffee":
                origin = fields["origin"].get().strip()
                roast = fields["roast"].get().strip()
                unit = fields["unit"].get().strip()
                if not origin or not roast or not unit:
                    raise ValueError("Enter the coffee origin, roast, and unit.")
                product = coffee(name, origin, roast, quantity, unit, bestby)
            else:
                product = donuts(name, quantity, bestby)

            inventory.add_product(product)
        except ValueError as error:
            messagebox.showerror("Cannot add product", str(error), parent=form)
            return

        product_selector.configure(values=inventory.get_product_names())
        selected_product.set(product.name)
        refresh_stock_labels()
        status_label.config(text=f"Added new product: {product.name}.")
        form.destroy()

    ttk.Button(form, text="Save Product", command=save_product, bootstyle="success").grid(
        row=5, column=0, columnspan=2, pady=12
    )


product_selector.bind("<<ComboboxSelected>>", refresh_stock_labels)
table_filter_selector.bind("<<ComboboxSelected>>", refresh_inventory_table)
refresh_stock_labels()
refresh_inventory_table()

# gui buttons for the above logic
action_frame = ttk.Frame(window, padding=(12, 4))
action_frame.pack()
ttk.Button(action_frame, text='Add Stock', command=add_stock, bootstyle="success").pack(side="left", padx=5)
ttk.Button(action_frame, text='Remove Stock', command=remove_stock, bootstyle="danger outline").pack(side="left", padx=5)
ttk.Button(action_frame, text='Add Product', command=open_add_product_form, bootstyle="primary").pack(side="left", padx=5)

window.mainloop()
