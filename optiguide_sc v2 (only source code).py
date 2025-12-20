# Commented out IPython magic to ensure Python compatibility.
# %pip install gurobipy>=10
import gurobipy as gp
from gurobipy import GRB, Model


# %pip install autogen
import autogen
from autogen.agentchat import Agent, UserProxyAgent


# %pip install optiguide
from optiguide.optiguide import OptiGuideAgent

import pandas as pd
import re
import requests  # for loading the example source code
import openai
import os
from dotenv import load_dotenv

import json
import requests
import time
from scipy.stats import norm
from pathlib import Path
from typing import Dict, Union, Optional

import matplotlib.pyplot as plt


"""**Initialisation**"""

# Create an environment with your WLS license
load_dotenv()
WLSACCESSID = os.getenv("WLSACCESSID")
WLSSECRET = os.getenv("WLSSECRET")
LICENSEID = int(os.getenv("LICENSEID"))
print(WLSACCESSID, WLSSECRET, LICENSEID)
params = {
"WLSACCESSID": WLSACCESSID,
"WLSSECRET": WLSSECRET,
"LICENSEID": LICENSEID,
}
env = gp.Env(params=params)

# Prompt for the OpenAI key securely
API_KEY = os.getenv("API")
if not API_KEY:
    raise RuntimeError("Missing API environment variable 'API'")

# Build config in memory
llm_config = {
    "config_list": [
        {
            "model": "gpt-5-mini",
            "api_key": API_KEY,
        }
    ]
}

config_list = llm_config["config_list"]

"""**Supply Chain File (csv)**"""

import pandas as pd
forecast_series = pd.read_csv(r"Demand_Forecast.csv")
forecast_series["Forecasted_Demand"] = forecast_series["Forecasted_Demand"].astype(int)

demand_std_by_sku = (
    forecast_series.groupby('SKU')['Forecasted_Demand'].std()
)
forecast_series["Date"] = pd.to_datetime(forecast_series["Date"])

# Sort by SKU then Date
forecast_series = forecast_series.sort_values(["SKU", "Date"])

# Create a within-SKU sequence index: 0,1,2,... for each SKU group
forecast_series["t"] = forecast_series.groupby("SKU").cumcount()

# Pivot: rows = position in the sequence, columns = SKU, values = Forecasted_Demand
demand_df = forecast_series.pivot(index="t", columns="SKU", values="Forecasted_Demand").reset_index(drop=True)

demand_std_df = demand_df.std().astype(int)


import pandas as pd
import numpy as np
from typing import Union, Dict, Optional
from scipy.stats import norm
import gurobipy as gp
from gurobipy import GRB





### Visualisation ###

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

###
### Optiguide Initialisation 
###

with open("source-code.py", "r", encoding="utf-8") as f:
    source_code = f.read()

with open("question_example.py", "r", encoding="utf-8") as f:
    example_qa = f.read()


agent = OptiGuideAgent(name="OptiGuide",
                  source_code = source_code,
                   debug_times=3,
                  example_qa=example_qa,
                llm_config={
        "seed": 42,
        "config_list": config_list,
    })

user = UserProxyAgent("user", max_consecutive_auto_reply=0,
                         human_input_mode="NEVER", code_execution_config=False)

ans = user.initiate_chat(agent, message="If SKU 449_Australia demand drops by 20% after period 6, what is the impact  ")
print(ans.summary)