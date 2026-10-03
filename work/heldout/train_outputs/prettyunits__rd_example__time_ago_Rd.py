# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 30

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'prettyunits__rd_example__time_ago_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['now']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Convert shimmed 'now' string to datetime if it exists
# r2py:entity:now
if 'now' in globals() and isinstance(now, str):
    now = datetime.fromisoformat(now.replace('Z', '+00:00'))

# Define the vague_dt_formats logic as it exists in the prettyunits R package
# These are approximates of the internal R package logic
# r2py:entity:time_ago
VAGUE_DT_FORMATS = {
    "default": [
        (lambda p: p['seconds'] < 1, lambda p: "moments ago"),
        (lambda p: p['minutes'] < 1, lambda p: "less than a minute ago"),
        (lambda p: p['minutes'] < 60, lambda p: f"{int(p['minutes'])} minute{'s' if p['minutes'] != 1 else ''} ago"),
        (lambda p: p['hours'] < 24, lambda p: f"{int(p['hours'])} hour{'s' if p['hours'] != 1 else ''} ago"),
        (lambda p: p['days'] < 2, lambda p: "a day ago"),
        (lambda p: p['days'] < 30, lambda p: f"{int(p['days'])} days ago"),
        (lambda p: p['days'] < 365, lambda p: "about a month ago"),
        (lambda p: p['years'] < 2, lambda p: "about a year ago"),
        (lambda p: True, lambda p: f"{int(p['years'])} years ago"),
    ],
    "short": [
        (lambda p: p['minutes'] < 1, lambda p: "<1 min"),
        (lambda p: p['minutes'] < 60, lambda p: f"{int(p['minutes'])} min"),
        (lambda p: p['hours'] < 24, lambda p: f"{int(p['hours'])} hours"),
        (lambda p: p['days'] < 30, lambda p: f"{int(p['days'])} day"),
        (lambda p: p['days'] < 365, lambda p: "1 mon"),
        (lambda p: p['years'] < 2, lambda p: "1 year"),
        (lambda p: True, lambda p: f"{int(p['years'])} years"),
    ],
    "terse": [
        (lambda p: p['minutes'] < 1, lambda p: f"{int(p['seconds'])}s"),
        (lambda p: p['minutes'] < 60, lambda p: f"{int(p['minutes'])}m"),
        (lambda p: p['hours'] < 24, lambda p: f" {int(p['hours'])}h"),
        (lambda p: p['days'] < 30, lambda p: f" {int(p['days'])}d"),
        (lambda p: p['days'] < 365, lambda p: f" 1M"),
        (lambda p: p['years'] < 2, lambda p: f" 1y"),
        (lambda p: True, lambda p: f"{int(p['years'])}y"),
    ]
}

def vague_dt(dt, format="default"):
    seconds = float(dt)
    pieces = {
        "seconds": seconds,
        "minutes": seconds / 60,
        "hours": seconds / 3600,
        "days": seconds / 86400,
        "years": seconds / (86400 * 365.25)
    }
    
    rules = VAGUE_DT_FORMATS.get(format, VAGUE_DT_FORMATS["default"])
    for condition, formatter in rules:
        if condition(pieces):
            return formatter(pieces)
    return ""

def time_ago(date, format="default"):
    if isinstance(date, str):
        date = datetime.fromisoformat(date.replace('Z', '+00:00'))
    
    # R's Sys.time() in the context of the script is mapped to 'now'
    diff = now - date
    seconds = diff.total_seconds()
    return vague_dt(seconds, format=format)

# Execution
print(time_ago(now))
# r2py:entity:time_ago_1
print(time_ago(now - timedelta(seconds=30)))
# r2py:entity:time_ago_2
print(time_ago(now - timedelta(minutes=14)))
# r2py:entity:time_ago_3
print(time_ago(now - timedelta(hours=5)))
# r2py:entity:time_ago_4
print(time_ago(now - timedelta(hours=25)))
# r2py:entity:time_ago_5
print(time_ago(now - timedelta(days=5)))
# r2py:entity:time_ago_6
print(time_ago(now - timedelta(days=30)))
# r2py:entity:time_ago_7
print(time_ago(now - timedelta(days=365)))
# r2py:entity:time_ago_8
print(time_ago(now - timedelta(days=365 * 10)))

# r2py:entity:time_ago_9
print(time_ago(now, format="short"))
# r2py:entity:time_ago_10
print(time_ago(now - timedelta(seconds=30), format="short"))
# r2py:entity:time_ago_11
print(time_ago(now - timedelta(minutes=14), format="short"))
# r2py:entity:time_ago_12
print(time_ago(now - timedelta(hours=5), format="short"))
# r2py:entity:time_ago_13
print(time_ago(now - timedelta(hours=25), format="short"))
# r2py:entity:time_ago_14
print(time_ago(now - timedelta(days=5), format="short"))
# r2py:entity:time_ago_15
print(time_ago(now - timedelta(days=30), format="short"))
# r2py:entity:time_ago_16
print(time_ago(now - timedelta(days=365), format="short"))
# r2py:entity:time_ago_17
print(time_ago(now - timedelta(days=365 * 10), format="short"))

# r2py:entity:time_ago_18
print(time_ago(now, format="terse"))
# r2py:entity:time_ago_19
print(time_ago(now - timedelta(seconds=30), format="terse"))
# r2py:entity:time_ago_20
print(time_ago(now - timedelta(minutes=14), format="terse"))
# r2py:entity:time_ago_21
print(time_ago(now - timedelta(hours=5), format="terse"))
# r2py:entity:time_ago_22
print(time_ago(now - timedelta(hours=25), format="terse"))
# r2py:entity:time_ago_23
print(time_ago(now - timedelta(days=5), format="terse"))
# r2py:entity:time_ago_24
print(time_ago(now - timedelta(days=30), format="terse"))
# r2py:entity:time_ago_25
print(time_ago(now - timedelta(days=365), format="terse"))
# r2py:entity:time_ago_26
print(time_ago(now - timedelta(days=365 * 10), format="terse"))