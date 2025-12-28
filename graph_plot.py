import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_inventory_info(df, sku):
    # Select specified SKU to plot
    sku_df = df[df['SKU'] == sku].sort_values('Period')

    periods = sku_df['Period']
    inventory = sku_df['Inventory']
    max_inventory = float(sku_df['MaxInventory'].iloc[0])
    demand = sku_df['DemandQty']
    order_qty = sku_df['OrderQty']
    safety_stock = sku_df['SafetyStock'].iloc[0]

    plt.figure(figsize=(12,6))

    plt.plot(periods, inventory, marker='o', label='Inventory', color='blue')

    plt.plot(periods, sku_df['MaxInventory'].astype(float), linestyle='--', marker='s', color='maroon', label='Max Inventory')


    plt.bar(periods, demand, alpha=0.3, color='orange', label='Demand Qty')

    plt.scatter(periods, order_qty, marker='^', s=80, color='green', label='Order Qty')

    plt.axhline(y=safety_stock, color='red', linestyle='--', label='Safety Stock')

    plt.xlabel('Period')
    plt.ylabel('Quantity')
    plt.title(f'Inventory, Demand, Orders for {sku}')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()
