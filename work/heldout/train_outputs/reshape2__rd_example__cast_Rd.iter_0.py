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
from plotnine import ggplot, aes, geom_point, facet_wrap

# Load datasets (Assuming standard datasets are available or mocked for functionality)
# airquality, ChickWeight, tips, french_fries are standard R datasets
from statsmodels.datasets import get_rdataset

# airquality section
# r2py:entity:names(airquality)
airquality.columns = [c.lower() for c in airquality.columns]
# r2py:entity:aqm
aqm = airquality.melt(id_vars=["month", "day"], value_name="value")
aqm.columns = ["month", "day", "variable", "value"]
aqm = aqm.dropna()

# acast(aqm, day ~ month ~ variable) -> Multi-index / Pivot
# r2py:entity:acast
pd.pivot_table(aqm, index="day", columns=["month", "variable"], values="value")
# acast(aqm, month ~ variable, mean)
# r2py:entity:acast_1
pd.pivot_table(aqm, index="month", columns="variable", values="value", aggfunc="mean")
# acast(aqm, month ~ variable, mean, margins = TRUE)
# r2py:entity:acast_2
pd.pivot_table(aqm, index="month", columns="variable", values="value", aggfunc="mean", margins=True)
# dcast(aqm, month ~ variable, mean, margins = c("month", "variable"))
# r2py:entity:dcast
pd.pivot_table(aqm, index="month", columns="variable", values="value", aggfunc="mean", margins=True)

# Subset operations
# acast(aqm, variable ~ month, mean, subset = .(variable == "ozone"))
# r2py:entity:acast_3
pd.pivot_table(aqm[aqm["variable"] == "ozone"], index="variable", columns="month", values="value", aggfunc="mean")
# acast(aqm, variable ~ month, mean, subset = .(month == 5))
# r2py:entity:acast_4
pd.pivot_table(aqm[aqm["month"] == 5], index="variable", columns="month", values="value", aggfunc="mean")

# ChickWeight section
# r2py:entity:names(ChickWeight)
ChickWeight.columns = [c.lower() for c in ChickWeight.columns]
# id=2:4 refers to weight, time, chick in original R ChickWeight
# r2py:entity:chick_m
chick_m = ChickWeight.melt(id_vars=ChickWeight.columns[1:4], value_name="value")
chick_m.columns = ["var1", "var2", "var3", "variable", "value"] # Adjusted to match melt logic

# mapping back for clarity: time, chick, diet
chick_m = ChickWeight.melt(id_vars=["time", "chick", "diet"], value_name="value")

# dcast(chick_m, time ~ variable, mean)
# r2py:entity:dcast_1
pd.pivot_table(chick_m, index="time", columns="variable", values="value", aggfunc="mean")
# dcast(chick_m, diet ~ variable, mean)
# r2py:entity:dcast_2
pd.pivot_table(chick_m, index="diet", columns="variable", values="value", aggfunc="mean")
# acast(chick_m, diet ~ time, mean)
# r2py:entity:acast_5
pd.pivot_table(chick_m, index="diet", columns="time", values="value", aggfunc="mean")

# acast(chick_m, time ~ diet, length)
# r2py:entity:acast_6
pd.pivot_table(chick_m, index="time", columns="diet", values="value", aggfunc="count")
# acast(chick_m, chick ~ time, mean)
# r2py:entity:acast_7
pd.pivot_table(chick_m, index="chick", columns="time", values="value", aggfunc="mean")
# acast(chick_m, chick ~ time, mean, subset = .(time < 10 & chick < 20))
# r2py:entity:acast_8
pd.pivot_table(chick_m[(chick_m["time"] < 10) & (chick_m["chick"] < 20)], index="chick", columns="time", values="value", aggfunc="mean")

# acast(chick_m, time ~ diet, length)
# r2py:entity:acast_9
pd.pivot_table(chick_m, index="time", columns="diet", values="value", aggfunc="count")

# dcast(chick_m, diet + chick ~ time)
# r2py:entity:dcast_3
chick_m.pivot_table(index=["diet", "chick"], columns="time", values="value")
# acast(chick_m, diet + chick ~ time)
# r2py:entity:acast_10
chick_m.pivot_table(index=["diet", "chick"], columns="time", values="value")
# acast(chick_m, chick ~ time ~ diet) -> 3D cast approximated by multi-index columns
# r2py:entity:acast_11
chick_m.pivot_table(index="chick", columns=["time", "diet"], values="value")
# acast(chick_m, diet + chick ~ time, length, margins="diet")
# r2py:entity:acast_12
pd.pivot_table(chick_m, index=["diet", "chick"], columns="time", values="value", aggfunc="count", margins=True)
# acast(chick_m, diet + chick ~ time, length, drop = FALSE)
# r2py:entity:acast_13
pd.pivot_table(chick_m, index=["diet", "chick"], columns="time", values="value", aggfunc="count")

# Tips section
# r2py:entity:dcast_4
tips_m = tips.melt()
pd.pivot_table(tips_m[tips_m["variable"] == "total_bill"], index="sex", columns="smoker", values="value", aggfunc="mean")

# French Fries section
# r2py:entity:ff_d
ff_d = french_fries.melt(id_vars=french_fries.columns[0:4], value_name="value")
ff_d.columns = ["subject", "time", "treatment", "rep", "variable", "value"] # Adjusted to match structure

# acast(ff_d, subject ~ time, length)
# r2py:entity:acast_14
pd.pivot_table(ff_d, index="subject", columns="time", values="value", aggfunc="count")
# acast(ff_d, subject ~ time, length, fill=0)
# r2py:entity:acast_15
pd.pivot_table(ff_d, index="subject", columns="time", values="value", aggfunc="count").fillna(0)
# dcast(ff_d, treatment ~ variable, mean, margins = TRUE)
# r2py:entity:dcast_5
pd.pivot_table(ff_d, index="treatment", columns="variable", values="value", aggfunc="mean", margins=True)
# dcast(ff_d, treatment + subject ~ variable, mean, margins="treatment")
# r2py:entity:dcast_6
pd.pivot_table(ff_d, index=["treatment", "subject"], columns="variable", values="value", aggfunc="mean", margins=True)

# lattice::xyplot approximation using plotnine
# r2py:entity:xyplot
plot_data = ff_d.pivot_table(index=["variable", "rep"], columns="subject", values="value").reset_index()
# We need to melt it back to long format for ggplot (plotnine) to mimic xyplot `1` ~ `2`
plot_long = plot_data.melt(id_vars=["variable", "rep"])
(ggplot(plot_long, aes(x="variable", y="value")) 
 + geom_point() 
 + facet_wrap("~variable")
)