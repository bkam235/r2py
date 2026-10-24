import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_point, facet_wrap

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/reshape2__rd_example__cast_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'reshape2__rd_example__cast_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['ChickWeight', 'airquality', 'french_fries', 'tips']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:suppressPackageStartupMessages
def suppressPackageStartupMessages(expr):
    return expr

# suppressPackageStartupMessages(library(reshape2))
# r2py:entity:import_reshape2
# (R library import)

def clean_print(df, is_dcast=False):
    """Helper to mimic R's cast output by removing axis names."""
    if df is None: return
    temp = df.copy()
    if is_dcast:
        # Remove the pandas integer index to match R's row numbering/lack thereof
        temp = temp.reset_index(drop=True)
        temp.index = temp.index + 1
    
    temp.index.name = None
    if isinstance(temp.columns, pd.MultiIndex):
        temp.columns.names = [None] * len(temp.columns.names)
    else:
        temp.columns.name = None
    print(temp)

# Air quality example
# r2py:entity:names(airquality)
airquality.columns = [c.lower() for c in airquality.columns]

# r2py:entity:aqm
aqm = airquality.melt(id_vars=["month", "day"], var_name="variable", value_name="value").dropna()

# r2py:entity:acast
acast = pd.pivot_table(aqm, index="day", columns=["month", "variable"], values="value")
clean_print(acast)

# r2py:entity:acast_1
acast_1 = pd.pivot_table(aqm, index="month", columns="variable", values="value", aggfunc="mean")
clean_print(acast_1)

# r2py:entity:acast_2
acast_2 = pd.pivot_table(aqm, index="month", columns="variable", values="value", aggfunc="mean", margins=True)
clean_print(acast_2)

# r2py:entity:dcast
dcast_res = pd.pivot_table(aqm, index="month", columns="variable", values="value", aggfunc="mean", margins=True).reset_index()
dcast = dcast_res
clean_print(dcast, is_dcast=True)

# library(plyr)
# r2py:entity:import_plyr
# (R library import)

# r2py:entity:acast_3
acast_3 = pd.pivot_table(aqm[aqm["variable"] == "ozone"], index="variable", columns="month", values="value", aggfunc="mean")
clean_print(acast_3)

# r2py:entity:acast_4
acast_4 = pd.pivot_table(aqm[aqm["month"] == 5], index="variable", columns="month", values="value", aggfunc="mean")
clean_print(acast_4)

# Chick weight example
# r2py:entity:names(ChickWeight)
ChickWeight.columns = [c.lower() for c in ChickWeight.columns]

# r2py:entity:chick_m
chick_m = ChickWeight.melt(id_vars=ChickWeight.columns[1:4], var_name="variable", value_name="value").dropna()
chick_m["time"] = pd.to_numeric(chick_m["time"], errors='coerce')
chick_m["chick"] = pd.to_numeric(chick_m["chick"], errors='coerce')

# r2py:entity:dcast_1
dcast_1 = pd.pivot_table(chick_m, index="time", columns="variable", values="value", aggfunc="mean").reset_index()
clean_print(dcast_1, is_dcast=True)

# r2py:entity:dcast_2
dcast_2 = pd.pivot_table(chick_m, index="diet", columns="variable", values="value", aggfunc="mean").reset_index()
clean_print(dcast_2, is_dcast=True)

# r2py:entity:acast_5
acast_5 = pd.pivot_table(chick_m, index="diet", columns="time", values="value", aggfunc="mean")
clean_print(acast_5)

# r2py:entity:acast_6
acast_6 = pd.pivot_table(chick_m, index="time", columns="diet", values="value", aggfunc="count")
clean_print(acast_6)

# r2py:entity:acast_7
acast_7 = pd.pivot_table(chick_m, index="chick", columns="time", values="value", aggfunc="mean")
clean_print(acast_7)

# r2py:entity:acast_8
acast_8 = pd.pivot_table(chick_m[(chick_m["time"] < 10) & (chick_m["chick"] < 20)], index="chick", columns="time", values="value", aggfunc="mean")
clean_print(acast_8)

# r2py:entity:acast_9
acast_9 = pd.pivot_table(chick_m, index="time", columns="diet", values="value", aggfunc="count")
clean_print(acast_9)

# r2py:entity:dcast_3
dcast_3 = pd.pivot_table(chick_m, index=["diet", "chick"], columns="time", values="value").reset_index()
clean_print(dcast_3, is_dcast=True)

# r2py:entity:acast_10
acast_10 = pd.pivot_table(chick_m, index=["diet", "chick"], columns="time", values="value")
clean_print(acast_10)

# r2py:entity:acast_11
acast_11 = pd.pivot_table(chick_m, index="chick", columns=["time", "diet"], values="value")
clean_print(acast_11)

# r2py:entity:acast_12
acast_12 = pd.pivot_table(chick_m, index=["diet", "chick"], columns="time", values="value", aggfunc="count", margins=True)
clean_print(acast_12)

# r2py:entity:acast_13
acast_13 = pd.pivot_table(chick_m, index=["diet", "chick"], columns="time", values="value", aggfunc="count")
clean_print(acast_13)

# Tips example
# r2py:entity:dcast_4
tips_melted = tips.melt(id_vars=["sex", "smoker"], var_name="variable", value_name="value")
dcast_4 = pd.pivot_table(tips_melted[tips_melted["variable"] == "total_bill"], index="sex", columns="smoker", values="value", aggfunc="mean").reset_index()
clean_print(dcast_4, is_dcast=True)

# French Fries example
# r2py:entity:ff_d
ff_d = french_fries.melt(id_vars=french_fries.columns[0:4], var_name="variable", value_name="value").dropna()

# r2py:entity:acast_14
acast_14 = pd.pivot_table(ff_d, index="subject", columns="time", values="value", aggfunc="count")
acast_14 = acast_14.reindex(sorted(acast_14.columns, key=lambda x: int(x) if str(x).isdigit() else x), axis=1)
clean_print(acast_14)

# r2py:entity:acast_15
acast_15 = pd.pivot_table(ff_d, index="subject", columns="time", values="value", aggfunc="count").fillna(0)
acast_15 = acast_15.reindex(sorted(acast_15.columns, key=lambda x: int(x) if str(x).isdigit() else x), axis=1)
clean_print(acast_15)

# r2py:entity:dcast_5
dcast_5_pivot = pd.pivot_table(ff_d, index="treatment", columns="variable", values="value", aggfunc="mean", margins=True)
# Reorder columns to match R's original data column order
orig_cols = [c for c in french_fries.columns if c not in ["time", "treatment", "subject", "rep"]]
col_order = [c for c in orig_cols if c in dcast_5_pivot.columns]
if "All" in dcast_5_pivot.columns: col_order.append("All")
dcast_5 = dcast_5_pivot[col_order].reset_index()
clean_print(dcast_5, is_dcast=True)

# r2py:entity:dcast_6
dcast_6_pivot = pd.pivot_table(ff_d, index=["treatment", "subject"], columns="variable", values="value", aggfunc="mean", margins=True)
col_order_6 = [c for c in orig_cols if c in dcast_6_pivot.columns]
if "All" in dcast_6_pivot.columns: col_order_6.append("All")
dcast_6 = dcast_6_pivot[col_order_6].reset_index()
clean_print(dcast_6, is_dcast=True)

# r2py:entity:import_lattice
# (R library import)

# r2py:entity:xyplot
try:
    cols_for_row = [c for c in ff_d.columns if c not in ["rep", "value"]]
    cast_df = pd.pivot_table(ff_d, index=cols_for_row, columns="rep", values="value")
    cast_df = cast_df.reset_index()
    plot_data = cast_df.copy()
    plot_data['x'] = plot_data.iloc[:, 0]
    plot_data['y'] = plot_data.iloc[:, 1]
    xyplot = (ggplot(plot_data, aes(x="x", y="y")) 
              + geom_point() 
              + facet_wrap("~variable"))
except Exception:
    xyplot = None

# call the function at the top level as it would be in R
suppressPackageStartupMessages(None)