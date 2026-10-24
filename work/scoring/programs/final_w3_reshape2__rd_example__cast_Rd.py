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

def r_melt(data, id_vars, value_name="value", na_rm=False):
    df = data.copy()
    if isinstance(id_vars, list) and all(isinstance(x, int) for x in id_vars):
        cols = df.columns[[i-1 for i in id_vars]]
        id_vars = list(cols)
    elif isinstance(id_vars, range):
        cols = df.columns[[i-1 for i in id_vars]]
        id_vars = list(cols)
    
    melted = df.melt(id_vars=id_vars, var_name="variable", value_name=value_name)
    if na_rm:
        melted = melted.dropna()
    return melted

def r_acast(data, index, columns, aggfunc="mean", subset=None, fill=np.nan, margins=None):
    df = data.copy()
    if subset is not None:
        df = df[subset]
    
    idx = [index] if isinstance(index, str) else index
    cols = [columns] if isinstance(columns, str) else columns
    
    pivot = df.pivot_table(index=idx, columns=cols, values="value", aggfunc=aggfunc)
    
    if margins:
        if margins is True:
            pivot.loc['(all)'] = pivot.mean(axis=0) if aggfunc != 'count' else pivot.sum(axis=0)
            pivot['(all)'] = pivot.mean(axis=1) if aggfunc != 'count' else pivot.sum(axis=1)
        elif isinstance(margins, str):
            pivot.loc['(all)'] = pivot.mean(axis=0) if aggfunc != 'count' else pivot.sum(axis=0)
            
    return pivot.fillna(fill)

def r_dcast(data, index, columns, aggfunc="mean", subset=None, margins=None):
    df = data.copy()
    if subset is not None:
        df = df[subset]
    
    idx = [index] if isinstance(index, str) else index
    cols = [columns] if isinstance(columns, str) else columns
    
    pivot = df.pivot_table(index=idx, columns=cols, values="value", aggfunc=aggfunc)
    
    if margins:
        if margins is True:
            pivot.loc['(all)'] = pivot.mean(axis=0) if aggfunc != 'count' else pivot.sum(axis=0)
            pivot['(all)'] = pivot.mean(axis=1) if aggfunc != 'count' else pivot.sum(axis=1)
        elif isinstance(margins, (list, tuple)):
            pivot.loc['(all)'] = pivot.mean(axis=0) if aggfunc != 'count' else pivot.sum(axis=0)
            pivot['(all)'] = pivot.mean(axis=1) if aggfunc != 'count' else pivot.sum(axis=1)
            
    return pivot.reset_index()

# Air quality example
# r2py:entity:names(airquality)
airquality.columns = [c.lower() for c in airquality.columns]
# r2py:entity:aqm
aqm = r_melt(airquality, id_vars=["month", "day"], na_rm=True)

# r2py:entity:acast
acast = r_acast(aqm, index="day", columns=["month", "variable"])
print(acast)
# r2py:entity:acast_1
acast_1 = r_acast(aqm, index="month", columns="variable", aggfunc="mean")
print(acast_1)
# r2py:entity:acast_2
acast_2 = r_acast(aqm, index="month", columns="variable", aggfunc="mean", margins=True)
print(acast_2)
# r2py:entity:dcast
dcast = r_dcast(aqm, index="month", columns="variable", aggfunc="mean", margins=["month", "variable"])
print(dcast)

# Subset operations
# r2py:entity:acast_3
acast_3 = r_acast(aqm, index="variable", columns="month", aggfunc="mean", subset=(aqm["variable"] == "ozone"))
print(acast_3)
# r2py:entity:acast_4
acast_4 = r_acast(aqm, index="variable", columns="month", aggfunc="mean", subset=(aqm["month"] == 5))
print(acast_4)

# Chick weight example
# r2py:entity:names(ChickWeight)
ChickWeight.columns = [c.lower() for c in ChickWeight.columns]
# r2py:entity:chick_m
chick_m = r_melt(ChickWeight, id_vars=[2, 3, 4], na_rm=True)

# r2py:entity:dcast_1
dcast_1 = r_dcast(chick_m, index="time", columns="variable", aggfunc="mean")
print(dcast_1)
# r2py:entity:dcast_2
dcast_2 = r_dcast(chick_m, index="diet", columns="variable", aggfunc="mean")
print(dcast_2)
# r2py:entity:acast_5
acast_5 = r_acast(chick_m, index="diet", columns="time", aggfunc="mean")
print(acast_5)

# r2py:entity:acast_6
acast_6 = r_acast(chick_m, index="time", columns="diet", aggfunc="count")
print(acast_6)
# r2py:entity:acast_7
acast_7 = r_acast(chick_m, index="chick", columns="time", aggfunc="mean")
print(acast_7)
# r2py:entity:acast_8
chick_m["time"] = pd.to_numeric(chick_m["time"])
chick_m["chick"] = pd.to_numeric(chick_m["chick"])
acast_8 = r_acast(chick_m, index="chick", columns="time", aggfunc="mean", subset=((chick_m["time"] < 10) & (chick_m["chick"] < 20)))
print(acast_8)

# r2py:entity:acast_9
acast_9 = r_acast(chick_m, index="time", columns="diet", aggfunc="count")
print(acast_9)

# r2py:entity:dcast_3
dcast_3 = r_dcast(chick_m, index=["diet", "chick"], columns="time", aggfunc="mean")
print(dcast_3)
# r2py:entity:acast_10
acast_10 = r_acast(chick_m, index=["diet", "chick"], columns="time", aggfunc="mean")
print(acast_10)
# r2py:entity:acast_11
acast_11 = r_acast(chick_m, index="chick", columns=["time", "diet"], aggfunc="mean")
print(acast_11)
# r2py:entity:acast_12
acast_12 = r_acast(chick_m, index=["diet", "chick"], columns="time", aggfunc="count", margins="diet")
print(acast_12)
# r2py:entity:acast_13
acast_13 = r_acast(chick_m, index=["diet", "chick"], columns="time", aggfunc="count", fill=np.nan)
print(acast_13)

# Tips example
# r2py:entity:dcast_4
tips_m = r_melt(tips, id_vars=["sex", "smoker"])
dcast_4 = r_dcast(tips_m, index="sex", columns="smoker", aggfunc="mean", subset=(tips_m["variable"] == "total_bill"))
print(dcast_4)

# French Fries example
# r2py:entity:ff_d
ff_d = r_melt(french_fries, id_vars=[1, 2, 3, 4], na_rm=True)
# r2py:entity:acast_14
acast_14 = r_acast(ff_d, index="subject", columns="time", aggfunc="count")
print(acast_14)
# r2py:entity:acast_15
acast_15 = r_acast(ff_d, index="subject", columns="time", aggfunc="count", fill=0)
print(acast_15)
# r2py:entity:dcast_5
dcast_5 = r_dcast(ff_d, index="treatment", columns="variable", aggfunc="mean", margins=True)
print(dcast_5)
# r2py:entity:dcast_6
dcast_6 = r_dcast(ff_d, index=["treatment", "subject"], columns="variable", aggfunc="mean", margins="treatment")
print(dcast_6)

# xyplot approximation
id_vars = [c for c in ff_d.columns if c not in ["rep", "value"]]
res_dcast = r_dcast(ff_d, index=id_vars, columns="rep", aggfunc="mean")
val_cols = [c for c in res_dcast.columns if c not in id_vars]
if len(val_cols) >= 2:
    plot_df = res_dcast[[val_cols[0], val_cols[1], "variable"]]
    plot_df.columns = ["x", "y", "variable"]
# r2py:entity:xyplot
    xyplot = (ggplot(plot_df, aes(x="x", y="y")) 
              + geom_point() 
              + facet_wrap("variable"))