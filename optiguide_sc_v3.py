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

load_dotenv()
API_KEY = os.getenv("API")
if not API_KEY:
    raise RuntimeError("Missing API environment variable 'API'")

# Build LLM config once (module-level)
llm_config = {
    "config_list": [
        {"model": "gpt-5-mini", "api_key": API_KEY}
    ]
}
config_list = llm_config["config_list"]

# Read the helper files as text once at startup
with open("source_code.py", "r", encoding="utf-8") as f:
    SOURCE_CODE_TEXT = f.read()

with open("question_example.py", "r", encoding="utf-8") as f:
    EXAMPLE_QA_TEXT = f.read()

# Initialize OptiGuideAgent once (module-level)
optiguide_agent = OptiGuideAgent(
    name="OptiGuide",
    source_code=SOURCE_CODE_TEXT,
    debug_times=3,
    example_qa=EXAMPLE_QA_TEXT,
    llm_config={
        "seed": 429,
        "config_list": config_list,
    }
)

# Create a reusable user proxy (if needed)
user = UserProxyAgent("user", max_consecutive_auto_reply=1,
                      human_input_mode="NEVER", code_execution_config=False)

def process_query(user_input: str, reinit_files: bool = False) -> dict:
    """
    Process a user query and return a dict with results.
    If reinit_files=True, re-read source files and reinitialize agent (useful for dev).
    """
    if reinit_files:
        # optional: re-read files and re-init agent for live edits
        with open("source_code.py", "r", encoding="utf-8") as f:
            source_code = f.read()
        with open("question_example.py", "r", encoding="utf-8") as f:
            example_qa = f.read()
        # reinitialize agent if necessary (costly)
        # optiguide_agent = OptiGuideAgent(...)

    # Use the existing agent and user proxy to run the chat
    # Note: autogen API may be synchronous or async; adapt if needed
    ans = user.initiate_chat(optiguide_agent, message=user_input)
    # ans may be an object; extract summary or text
    answer_summary = getattr(ans, "summary", None)
    # fallback to string representation
    if answer_summary is None:
        answer_summary = str(ans)

    return {"response": answer_summary}