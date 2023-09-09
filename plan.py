import csv

# create variable from all input files
master, inventory, undelivered = {}, {}, {}

with open("input_files/master.csv", "r") as master_file:
    reader = csv.DictReader(master_file)
    for row in reader:
        sku, supplier, target, trigger, order_qty = row["sku"], row["supplier"], row["target_stock"], row["trigger_point"], row["order_qty"]
        master[sku] = {"supplier": supplier, "target": target, "trigger": trigger, "order_qty": order_qty}

with open("input_files/inventory.csv", "r") as inventory_file:
    reader = csv.DictReader(inventory_file)
    for row in reader:
        sku, inventory_qty = row["sku"], row["inventory"]
        inventory[sku] = inventory_qty

with open("input_files/undelivered.csv", "r") as undelivered_file:
    reader = csv.DictReader(undelivered_file)
    for row in reader:
        sku, undelivered_qty = row["sku"], row["undelivered"]
        undelivered[sku] = undelivered_qty



