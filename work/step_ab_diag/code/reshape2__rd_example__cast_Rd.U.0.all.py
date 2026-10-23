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

# Air quality example
airquality.columns = [c.lower() for c in airquality.columns]
# aqm <- melt(airquality, id=c("month", "day"), na.rm=TRUE)
aqm = airquality.melt(id_vars=["month", "day"], value_name="value").dropna()

# acast(aqm, day ~ month ~ variable)
# This is a 3D array in R; in Python we represent as a pivot with MultiIndex columns
acast = pd.pivot_table(aqm, index="day", columns=["month", "variable"], values="value")

# acast(aqm, month ~ variable, mean)
acast_1 = pd.pivot_table(aqm, index="month", columns="variable", values="value", aggfunc="mean")

# acast(aqm, month ~ variable, mean, margins = TRUE)
acast_2 = pd.pivot_table(aqm, index="month", columns="variable", values="value", aggfunc="mean", margins=True)

# dcast(aqm, month ~ variable, mean, margins = c("month", "variable"))
dcast = pd.pivot_table(aqm, index="month", columns="variable", values="value", aggfunc="mean", margins=True)

# acast(aqm, variable ~ month, mean, subset = .(variable == "ozone"))
acast_3 = pd.pivot_table(aqm[aqm["variable"] == "ozone"], index="variable", columns="month", values="value", aggfunc="mean")

# acast(aqm, variable ~ month, mean, subset = .(month == 5))
acast_4 = pd.pivot_table(aqm[aqm["month"] == 5], index="variable", columns="month", values="value", aggfunc="mean")

# Chick weight example
ChickWeight.columns = [c.lower() for c in ChickWeight.columns]
# id=2:4 in R (1-indexed) corresponds to indices 1, 2, 3 in Python (time, chick, diet)
chick_m = ChickWeight.melt(id_vars=ChickWeight.columns[1:4], value_name="value").dropna()

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
acast_12 = pd.pivot_table(chick_m, index=["diet", "chick"], columns="time", values="value", aggfunc="count", margins=True)

# acast(chick_m, diet + chick ~ time, length, drop = FALSE)
acast_13 = pd.pivot_table(chick_m, index=["diet", "chick"], columns="time", values="value", aggfunc="count")

# Tips example
# dcast(melt(tips), sex ~ smoker, mean, subset = .(variable == "total_bill"))
tips_m = tips.melt()
dcast_4 = pd.pivot_table(tips_m[tips_m["variable"] == "total_bill"], index="sex", columns="smoker", values="value", aggfunc="mean")

# French Fries example
# ff_d <- melt(french_fries, id=1:4, na.rm=TRUE)
ff_d = french_fries.melt(id_vars=french_fries.columns[0:4], value_name="value").dropna()

# acast(ff_d, subject ~ time, length)
acast_14 = pd.pivot_table(ff_d, index="subject", columns="time", values="value", aggfunc="count")

# acast(ff_d, subject ~ time, length, fill=0)
acast_15 = pd.pivot_table(ff_d, index="subject", columns="time", values="value", aggfunc="count").fillna(0)

# dcast(ff_d, treatment ~ variable, mean, margins = TRUE)
dcast_5 = pd.pivot_table(ff_d, index="treatment", columns="variable", values="value", aggfunc="mean", margins=True)

# dcast(ff_d, treatment + subject ~ variable, mean, margins="treatment")
dcast_6 = pd.pivot_table(ff_d, index=["treatment", "subject"], columns="variable", values="value", aggfunc="mean", margins=True)

# lattice::xyplot(`1` ~ `2` | variable, dcast(ff_d, ... ~ rep), aspect="iso")
# The R formula `1` ~ `2` in dcast(ff_d, ... ~ rep) refers to the resulting columns of the cast.
# dcast(ff_d, ... ~ rep) means indices are everything else, columns are 'rep'.
# In Python, we pivot to get 'rep' as columns.
cast_for_plot = pd.pivot_table(ff_d, index=["variable", "subject", "time", "treatment"], columns="rep", values="value")
plot_df = cast_for_plot.reset_index()

# Plotting `1` ~ `2` (first two columns of the resulting cast) grouped by `variable`
xyplot = (ggplot(plot_df, aes(x=plot_df.columns[4], y=plot_df.columns[5])) # Simplified proxy for `1` ~ `2`
          + geom_point() 
          + facet_wrap("variable"))