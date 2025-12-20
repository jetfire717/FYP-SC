"""
-----------
Question: What if service level for all SKUs become 90%?
Answer Code:
```python
service_level_target = 0.9
```

Question: What if holding cost increase by 20% for all SKUs?
Answer Code:
try:
    if isinstance(holding_cost, dict):
        # scale every provided SKU value safely
        holding_cost = {sku: 1.2 * float(val) for sku, val in holding_cost.items()}
    else:
        # scalar or None: scale scalar or use default 2.0
        holding_cost = 1.2 * float(holding_cost) if holding_cost is not None else 1.2 * 2.0
except Exception:
    # fallback: set a safe scalar if anything unexpected happens
    holding_cost = 1.2 * 2.0

```
"""