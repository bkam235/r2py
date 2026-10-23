# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 33

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/reshape2__rd_example__cast_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'reshape2__rd_example__cast_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['ChickWeight', 'airquality', 'french_fries', 'tips']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# Air quality example
airquality.columns = [c.lower() for c in airquality.columns]
# aqm <- melt(airquality, id=c("month", "day"), na.rm=TRUE)
aqm = airquality.melt(id_vars=["month", "day"], value_name="value").dropna()

# acast(aqm, day ~ month ~ variable)
# R's 3D acast returns an array. We simulate it with a pivot table.
acast = pd.pivot_table(aqm, index="day", columns=["month", "variable"], values="value")

# acast(aqm, month ~ variable, mean)
acast_1 = pd.pivot_table(aqm, index="month", columns="variable", values="value", aggfunc="mean")

# acast(aqm, month ~ variable, mean, margins = TRUE)
acast_2 = pd.pivot_table(aqm, index="month", columns="variable", values="value", aggfunc="mean")
acast_2.loc['All'] = acast_2.mean()
acast_2['All'] = acast_2.mean(axis=1)

# dcast(aqm, month ~ variable, mean, margins = c("month", "variable"))
dcast = pd.pivot_table(aqm, index="month", columns="variable", values="value", aggfunc="mean")
dcast.loc['All'] = dcast.mean()
dcast['All'] = dcast.mean(axis=1)

# acast(aqm, variable ~ month, mean, subset = .(variable == "ozone"))
acast_3 = pd.pivot_table(aqm[aqm["variable"] == "ozone"], index="variable", columns="month", values="value", aggfunc="mean")

# acast(aqm, variable ~ month, mean, subset = .(month == 5))
acast_4 = pd.pivot_table(aqm[aqm["month"] == 5], index="variable", columns="month", values="value", aggfunc="mean")

# Chick weight example
ChickWeight.columns = [c.lower() for c in ChickWeight.columns]
# chick_m <- melt(ChickWeight, id=2:4, na.rm=TRUE)
# In R, 2:4 are columns time, chick, diet (1-indexed)
id_cols = ChickWeight.columns[1:4].tolist()
chick_m = ChickWeight.melt(id_vars=id_cols, value_name="value").dropna()

# dcast(chick_m, time ~ variable, mean)
dcast_1 = pd.pivot_table(chick_m, index="time", columns="variable", values="value", aggfunc="mean")

# dcast(chick_m, diet ~ variable, mean)
dcast_2 = pd.pivot_table(chick_m, index="diet", columns="variable", values="value", aggfunc="mean")

# acast(chick_m, diet ~ time, mean)
acast_5 = pd.pivot_table(chick_m, index="diet", columns="time", values="value", aggfunc="mean")

# acast(chick_m, time ~ diet, length)
acast_6 = pd.pivot_table(chick_m, index="time", columns="diet", values="value", aggfunc="count")

# acast(chick_m, chick ~ time, mean)
acast_7 = pd.pivot_table(chick_m, index="chick", columns="time", values="value", aggfunc="mean")

# acast(chick_m, chick ~ time, mean, subset = .(time < 10 & chick < 20))
acast_8 = pd.pivot_table(chick_m[(chick_m["time"] < 10) & (chick_m["chick"] < 20)], index="chick", columns="time", values="value", aggfunc="mean")

# acast(chick_m, time ~ diet, length)
acast_9 = pd.pivot_table(chick_m, index="time", columns="diet", values="value", aggfunc="count")

# dcast(chick_m, diet + chick ~ time)
dcast_3 = pd.pivot_table(chick_m, index=["diet", "chick"], columns="time", values="value")

# acast(chick_m, diet + chick ~ time)
acast_10 = pd.pivot_table(chick_m, index=["diet", "chick"], columns="time", values="value")

# acast(chick_m, chick ~ time ~ diet)
acast_11 = pd.pivot_table(chick_m, index="chick", columns=["time", "diet"], values="value")

# acast(chick_m, diet + chick ~ time, length, margins="diet")
acast_12 = pd.pivot_table(chick_m, index=["diet", "chick"], columns="time", values="value", aggfunc="count")
diet_means = acast_12.groupby(level=0).sum()
acast_12 = pd.concat([acast_12, diet_means])

# acast(chick_m, diet + chick ~ time, length, drop = FALSE)
acast_13 = pd.pivot_table(chick_m, index=["diet", "chick"], columns="time", values="value", aggfunc="count")

# Tips example
tips_m = tips.melt()
dcast_4 = pd.pivot_table(tips_m[tips_m["variable"] == "total_bill"], index="sex", columns="smoker", values="value", aggfunc="mean")

# French Fries example
# ff_d <- melt(french_fries, id=1:4, na.rm=TRUE)
ff_id_cols = french_fries.columns[0:4].tolist()
ff_d = french_fries.melt(id_vars=ff_id_cols, value_name="value").dropna()

# acast(ff_d, subject ~ time, length)
acast_14 = pd.pivot_table(ff_d, index="subject", columns="time", values="value", aggfunc="count")

# acast(ff_d, subject ~ time, length, fill=0)
acast_15 = pd.pivot_table(ff_d, index="subject", columns="time", values="value", aggfunc="count").fillna(0)

# dcast(ff_d, treatment ~ variable, mean, margins = TRUE)
dcast_5 = pd.pivot_table(ff_d, index="treatment", columns="variable", values="value", aggfunc="mean")
dcast_5.loc['All'] = dcast_5.mean()
dcast_5['All'] = dcast_5.mean(axis=1)

# dcast(ff_d, treatment + subject ~ variable, mean, margins="treatment")
dcast_6 = pd.pivot_table(ff_d, index=["treatment", "subject"], columns="variable", values="value", aggfunc="mean")
treat_margins = dcast_6.groupby(level=0).mean()
dcast_6 = pd.concat([dcast_6, treat_margins])

# lattice::xyplot approximation
# dcast(ff_d, ... ~ rep)
xyplot = pd.pivot_table(ff_d, index=["variable", "subject"], columns="rep", values="value")