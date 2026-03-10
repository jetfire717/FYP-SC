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


###
### Optiguide Initialisation 
###

with open("source_code.py", "r", encoding="utf-8") as f:
    source_code = f.read()

with open("question_example.py", "r", encoding="utf-8") as f:
    example_qa = f.read()


optiguide_agent = OptiGuideAgent(name="OptiGuide",
                  source_code = source_code,
                   debug_times=3,
                  example_qa=example_qa,
                llm_config={
        "seed": 42,
        "config_list": config_list,
    })

user = UserProxyAgent("user", max_consecutive_auto_reply=1,
                         human_input_mode="ALWAYS", code_execution_config=False)

ans = user.initiate_chat(optiguide_agent, message = input("Please enter your inventory management query and I will get back to you: "))
answer_summary = ans.summary