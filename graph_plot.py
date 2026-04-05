import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from io import BytesIO

def generate_inventory_plot(df, sku):
    sku_df = df[df['SKU'] == sku].sort_values('Period')

    periods = sku_df['Period']
    inventory = sku_df['Inventory']
    max_inventory = float(sku_df['MaxInventory'].iloc[0])
    demand = sku_df['DemandQty']
    order_qty = sku_df['OrderQty']
    safety_stock = sku_df['SafetyStock'].iloc[0]

    fig = Figure(figsize=(12, 6))
    ax = fig.subplots()

    ax.plot(periods, inventory, marker='o', label='Inventory', color='blue')
    ax.plot(periods, sku_df['MaxInventory'].astype(float), linestyle='--', marker='s', color='maroon', label='Max Inventory')
    ax.bar(periods, demand, alpha=0.3, color='orange', label='Demand Qty')
    ax.scatter(periods, order_qty, marker='^', s=80, color='green', label='Order Qty')
    ax.axhline(y=safety_stock, color='red', linestyle='--', label='Safety Stock')

    ax.set_xlabel('Period')
    ax.set_ylabel('Quantity')
    ax.set_title(f'Inventory, Demand, Orders for {sku}')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)

    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return buf