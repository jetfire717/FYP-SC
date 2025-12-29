    # %pip install gurobipy>=10
import gurobipy as gp
from gurobipy import GRB, Model


# %pip install autogen
import autogen
from autogen.agentchat import Agent, UserProxyAgent


# %pip install optiguide
from optiguide.optiguide import OptiGuideAgent

import pandas as pd
import numpy as np
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


### Initialisation ###
load_dotenv()
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

### Import Supply Chain File (csv) ###

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


###
### Optiguide Initialisation 
###

with open("source_code.py", "r", encoding="utf-8") as f:
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

user = UserProxyAgent("user", max_consecutive_auto_reply=3,
                         human_input_mode="NEVER", code_execution_config=False)

message = input("Please enter your inventory management query and I will get back to you")
#message= "If SKU 449_Australia demand drops by 20% after period 6, what is the impact?"
ans = user.initiate_chat(agent, message = message)
print(ans.summary)