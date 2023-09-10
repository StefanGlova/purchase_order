import csv, json, math

# create variable from all input files
master, inventory, undelivered, suppliers = {}, {}, {}, {}

with open("input_files/master.csv", "r") as master_file:
    reader = csv.DictReader(master_file)
    for row in reader:
        sku, supplier, target, trigger, order_qty = row["sku"], row["supplier"], int(row["target_stock"]), int(row["trigger_point"]), int(row["order_qty"])
        master[sku] = {"supplier": supplier, "target": target, "trigger": trigger, "order_qty": order_qty}
        suppliers[supplier] = {}

with open("input_files/inventory.csv", "r") as inventory_file:
    reader = csv.DictReader(inventory_file)
    for row in reader:
        sku, inventory_qty = row["sku"], int(row["inventory"])
        try: # Next occurance in the file
            inventory[sku] += inventory_qty
        except KeyError: # First occurance in the file
            inventory[sku] = inventory_qty

with open("input_files/undelivered.csv", "r") as undelivered_file:
    reader = csv.DictReader(undelivered_file)
    for row in reader:
        sku, undelivered_qty = row["sku"], int(row["undelivered"])
        try: # Next occurance in the file
            undelivered[sku] += undelivered_qty
        except KeyError: # First occurance in the file
            undelivered[sku] = undelivered_qty

# calculate what to order
for sku in master:
    trigger, target = master[sku]["trigger"], master[sku]["target"]
    try:
        current_qty = inventory[sku] + undelivered[sku]
    except KeyError: # Error occurs if there is nothing on undelivered PO
        current_qty = inventory[sku]
    if current_qty < trigger: 
        to_order, supplier = master[sku]["order_qty"], master[sku]["supplier"]
        suppliers[supplier][sku] = to_order * math.ceil((target - current_qty) / to_order)

# create output file for new order in csv format grouped by supplier
with open("output/output.csv", "w", newline="") as output_file:
    fieldnames = ["supplier", "sku", "order_qty"]
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    for supplier in suppliers:
        for sku in suppliers[supplier]:
            qty = suppliers[supplier][sku]
            writer.writerow({"supplier": supplier, "sku": sku, "order_qty": qty})
    
# create output file for new order in json format, grouped by supplier
with open("output/output.json", "w") as output_json_file:
    json.dump(suppliers, output_json_file, indent=4)
