import pandas as pd
import numpy as np

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/reshape2__rd_example__cast_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'reshape2__rd_example__cast_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['ChickWeight', 'airquality', 'french_fries', 'tips']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# Air quality example
# r2py:entity:names(airquality)
airquality.columns = [c.lower() for c in airquality.columns]
# r2py:entity:aqm
aqm = airquality.melt(id_vars=["month", "day"], value_vars=["ozone", "solar.r", "wind", "temp"], var_name="variable", value_name="value").dropna()

# acast(aqm, day ~ month ~ variable)
# r2py:entity:acast
acast_res = aqm.pivot_table(index="day", columns=["month", "variable"], values="value")
# acast(aqm, month ~ variable, mean)
# r2py:entity:acast_1
acast_1 = aqm.pivot_table(index="month", columns="variable", values="value", aggfunc="mean")
# acast(aqm, month ~ variable, mean, margins = TRUE)
# r2py:entity:acast_2
acast_2 = aqm.pivot_table(index="month", columns="variable", values="value", aggfunc="mean", margins=True)
# dcast(aqm, month ~ variable, mean, margins = c("month", "variable"))
# r2py:entity:dcast
dcast_res = aqm.pivot_table(index="month", columns="variable", values="value", aggfunc="mean", margins=True)

# Subset operations
# acast(aqm, variable ~ month, mean, subset = .(variable == "ozone"))
# r2py:entity:acast_3
acast_3 = aqm[aqm["variable"] == "ozone"].pivot_table(index="variable", columns="month", values="value", aggfunc="mean")
# acast(aqm, variable ~ month, mean, subset = .(month == 5))
# r2py:entity:acast_4
acast_4 = aqm[aqm["month"] == 5].pivot_table(index="variable", columns="month", values="value", aggfunc="mean")

# Chick weight example
# r2py:entity:names(ChickWeight)
ChickWeight.columns = [c.lower() for c in ChickWeight.columns]
# id=2:4 in ChickWeight refers to time, chick, diet (assuming columns are weight, time, chick, diet)
# r2py:entity:chick_m
chick_m = ChickWeight.melt(id_vars=["time", "chick", "diet"], value_vars=["weight"], var_name="variable", value_name="value")

# dcast(chick_m, time ~ variable, mean)
# r2py:entity:dcast_1
dcast_1 = chick_m.pivot_table(index="time", columns="variable", values="value", aggfunc="mean")
# dcast(chick_m, diet ~ variable, mean)
# r2py:entity:dcast_2
dcast_2 = chick_m.pivot_table(index="diet", columns="variable", values="value", aggfunc="mean")
# acast(chick_m, diet ~ time, mean)
# r2py:entity:acast_5
acast_5 = chick_m.pivot_table(index="diet", columns="time", values="value", aggfunc="mean")

# acast(chick_m, time ~ diet, length)
# r2py:entity:acast_6
acast_6 = chick_m.pivot_table(index="time", columns="diet", values="value", aggfunc="count")
# acast(chick_m, chick ~ time, mean)
# r2py:entity:acast_7
acast_7 = chick_m.pivot_table(index="chick", columns="time", values="value", aggfunc="mean")
# acast(chick_m, chick ~ time, mean, subset = .(time < 10 & chick < 20))
# r2py:entity:acast_8
acast_8 = chick_m[(chick_m["time"] < 10) & (chick_m["chick"] < 20)].pivot_table(index="chick", columns="time", values="value", aggfunc="mean")

# acast(chick_m, time ~ diet, length)
# r2py:entity:acast_9
acast_9 = chick_m.pivot_table(index="time", columns="diet", values="value", aggfunc="count")

# dcast(chick_m, diet + chick ~ time)
# r2py:entity:dcast_3
dcast_3 = chick_m.pivot_table(index=["diet", "chick"], columns="time", values="value")
# acast(chick_m, diet + chick ~ time)
# r2py:entity:acast_10
acast_10 = chick_m.pivot_table(index=["diet", "chick"], columns="time", values="value")
# acast(chick_m, chick ~ time ~ diet)
# r2py:entity:acast_11
acast_11 = chick_m.pivot_table(index="chick", columns=["time", "diet"], values="value")
# acast(chick_m, diet + chick ~ time, length, margins="diet")
# r2py:entity:acast_12
acast_12 = chick_m.pivot_table(index=["diet", "chick"], columns="time", values="value", aggfunc="count", margins=True)
# acast(chick_m, diet + chick ~ time, length, drop = FALSE)
# r2py:entity:acast_13
acast_13 = chick_m.pivot_table(index=["diet", "chick"], columns="time", values="value", aggfunc="count")

# Tips example
# dcast(melt(tips), sex ~ smoker, mean, subset = .(variable == "total_bill"))
# r2py:entity:dcast_4
tips_m = tips.melt(var_name="variable", value_name="value")
dcast_4 = tips_m[tips_m["variable"] == "total_bill"].pivot_table(index="sex", columns="smoker", values="value", aggfunc="mean")

# French Fries example
# ff_d <- melt(french_fries, id=1:4, na.rm=TRUE)
# r2py:entity:ff_d
ff_d = french_fries.melt(id_vars=french_fries.columns[0:4], var_name="variable", value_name="value").dropna()

# acast(ff_d, subject ~ time, length)
# r2py:entity:acast_14
acast_14 = ff_d.pivot_table(index="subject", columns="time", values="value", aggfunc="count")
# acast(ff_d, subject ~ time, length, fill=0)
# r2py:entity:acast_15
acast_15 = ff_d.pivot_table(index="subject", columns="time", values="value", aggfunc="count").fillna(0)
# dcast(ff_d, treatment ~ variable, mean, margins = TRUE)
# r2py:entity:dcast_5
dcast_5 = ff_d.pivot_table(index="treatment", columns="variable", values="value", aggfunc="mean", margins=True)
# dcast(ff_d, treatment + subject ~ variable, mean, margins="treatment")
# r2py:entity:dcast_6
dcast_6 = ff_d.pivot_table(index=["treatment", "subject"], columns="variable", values="value", aggfunc="mean", margins=True)

# lattice::xyplotapproximation
# r2py:entity:xyplot
# dcast(ff_d, ... ~ rep) -> this corresponds to taking everything not specified as index as columns
# In R, ... matches all variables. Here it implies all except 'rep'.
xyplot_data = ff_d.pivot_table(index=["variable", "rep"], columns="subject", values="value")