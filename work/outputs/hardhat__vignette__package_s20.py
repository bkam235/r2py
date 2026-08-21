# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/hardhat__vignette__package_s20.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hardhat__vignette__package_s20.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['penguins']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from statsmodels.formula.api import ols

# Load penguins dataset (assuming palmerpenguins is available via seaborn or csv)
import seaborn as sns

# r2py:entity:model
def simple_lm(formula, data):
    model = ols(formula, data=data).fit()
    # Store blueprint and model for emulation of hardhat structure
    return {
        "model": model,
        "blueprint": formula,
        "data": data
    }

# r2py:entity:predictors
def forge(data, blueprint):
    # Simplified version of forge to extract predictors
    # In a real scenario, this would handle formula parsing
    return {"predictors": data}

# r2py:entity:predict_simple_lm_bridge
def predict_simple_lm_bridge(type_check, model_obj, predictors):
    # Emulating the hardhat bridge validation logic
    if type_check != "numeric":
        raise TypeError(f"Expected 'numeric', got '{type_check}'")
    
    # Use statsmodels prediction
    model = model_obj["model"]
    return model.predict(predictors["predictors"])

try:
    # Model fitting
# r2py:entity:model
    model = simple_lm("bill_length_mm ~ body_mass_g + species", penguins)

    # Forge predictors
# r2py:entity:predictors
    predictors = forge(penguins, model["blueprint"])["predictors"]

    # Valid call
# r2py:entity:predict_simple_lm_bridge
    print(predict_simple_lm_bridge("numeric", model, predictors))

    # Invalid call (should trigger the TypeError)
# r2py:entity:predict_simple_lm_bridge_1
    print(predict_simple_lm_bridge("numer", model, predictors))
except Exception as e:
    print(e)