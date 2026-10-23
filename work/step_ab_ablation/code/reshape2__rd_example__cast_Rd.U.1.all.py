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
aqm = airquality.melt(id_vars=["month", "day"], value_vars=["ozone", "solar.r", "wind", "temp"], var_name="variable", value_name="value").dropna()

# acast(aqm, day ~ month ~ variable)
# In R, this is a 3D array. In Pandas, we use a MultiIndex.
acast_res = aqm.pivot_table(index="day", columns=["month", "variable"], values="value")

# acast(aqm, month ~ variable, mean)
acast_1 = aqm.pivot_table(index="month", columns="variable", values="value", aggfunc="mean")

# acast(aqm, month ~ variable, mean, margins = TRUE)
acast_2 = aqm.pivot_table(index="month", columns="variable", values="value", aggfunc="mean", margins=True)

# dcast(aqm, month ~ variable, mean, margins = c("month", "variable"))
dcast_res = aqm.pivot_table(index="month", columns="variable", values="value", aggfunc="mean", margins=True)

# acast(aqm, variable ~ month, mean, subset = .(variable == "ozone"))
acast_3 = aqm[aqm["variable"] == "ozone"].pivot_table(index="variable", columns="month", values="value", aggfunc="mean")

# acast(aqm, variable ~ month, mean, subset = .(month == 5))
acast_4 = aqm[aqm["month"] == 5].pivot_table(index="variable", columns="month", values="value", aggfunc="mean")

# Chick weight example
ChickWeight.columns = [c.lower() for c in ChickWeight.columns]
# melt(ChickWeight, id=2:4) -> columns at indices 1, 2, 3 (time, chick, diet) are IDs
chick_ids = ChickWeight.columns[1:4].tolist()
chick_m = ChickWeight.melt(id_vars=chick_ids, var_name="variable", value_name="value").dropna()

# dcast(chick_m, time ~ variable, mean)
dcast_1 = chick_m.pivot_table(index="time", columns="variable", values="value", aggfunc="mean")

# dcast(chick_m, diet ~ variable, mean)
dcast_2 = chick_m.pivot_table(index="diet", columns="variable", values="value", aggfunc="mean")

# acast(chick_m, diet ~ time, mean)
acast_5 = chick_m.pivot_table(index="diet", columns="time", values="value", aggfunc="mean")

# acast(chick_m, time ~ diet, length)
acast_6 = chick_m.pivot_table(index="time", columns="diet", values="value", aggfunc="count")

# acast(chick_m, chick ~ time, mean)
acast_7 = chick_m.pivot_table(index="chick", columns="time", values="value", aggfunc="mean")

# acast(chick_m, chick ~ time, mean, subset = .(time < 10 & chick < 20))
acast_8 = chick_m[(chick_m["time"] < 10) & (chick_m["chick"] < 20)].pivot_table(index="chick", columns="time", values="value", aggfunc="mean")

# acast(chick_m, time ~ diet, length)
acast_9 = chick_m.pivot_table(index="time", columns="diet", values="value", aggfunc="count")

# dcast(chick_m, diet + chick ~ time)
dcast_3 = chick_m.pivot_table(index=["diet", "chick"], columns="time", values="value")

# acast(chick_m, diet + chick ~ time)
acast_10 = chick_m.pivot_table(index=["diet", "chick"], columns="time", values="value")

# acast(chick_m, chick ~ time ~ diet)
acast_11 = chick_m.pivot_table(index="chick", columns=["time", "diet"], values="value")

# acast(chick_m, diet + chick ~ time, length, margins="diet")
# R's margins="diet" adds a marginal total for the 'diet' level of the index.
# In pandas, we use margins=True then filter or just compute the mean/count.
acast_12 = chick_m.pivot_table(index=["diet", "chick"], columns="time", values="value", aggfunc="count", margins=True)

# acast(chick_m, diet + chick ~ time, length, drop = FALSE)
acast_13 = chick_m.pivot_table(index=["diet", "chick"], columns="time", values="value", aggfunc="count")

# Tips example
tips_melted = tips.melt()
dcast_4 = tips_melted[tips_melted["variable"] == "total_bill"].pivot_table(index="sex", columns="smoker", values="value", aggfunc="mean")

# French Fries example
# melt(french_fries, id=1:4)
ff_ids = french_fries.columns[0:4].tolist()
ff_d = french_fries.melt(id_vars=ff_ids, var_name="variable", value_name="value").dropna()

# acast(ff_d, subject ~ time, length)
acast_14 = ff_d.pivot_table(index="subject", columns="time", values="value", aggfunc="count")

# acast(ff_d, subject ~ time, length, fill=0)
acast_15 = ff_d.pivot_table(index="subject", columns="time", values="value", aggfunc="count").fillna(0)

# dcast(ff_d, treatment ~ variable, mean, margins = TRUE)
dcast_5 = ff_d.pivot_table(index="treatment", columns="variable", values="value", aggfunc="mean", margins=True)

# dcast(ff_d, treatment + subject ~ variable, mean, margins="treatment")
dcast_6 = ff_d.pivot_table(index=["treatment", "subject"], columns="variable", values="value", aggfunc="mean", margins=True)

# lattice::xyplot(`1` ~ `2` | variable, dcast(ff_d, ... ~ rep))
# R's `...` in dcast usually means all remaining variables.
# dcast(ff_d, ... ~ rep) means indices are all except rep, columns are rep.
cast_ff = ff_d.pivot_table(index=["treatment", "subject", "variable"], columns="rep", values="value")
cast_ff_reset = cast_ff.reset_index()
# xyplot(1 ~ 2 | variable) -> 1 is the first column (treatment), 2 is the second (subject)
# However, the columns of the cast result are the 'rep' values.
# We'll treat the first two columns of the resulting df as x and y for the plot.
plot_df = cast_ff_reset.copy()
# The formula `1` ~ `2` usually refers to the first and second columns of the data provided to xyplot.
# Column 0: treatment, Column 1: subject.
xyplot_res = (ggplot(plot_df, aes(x=plot_df.columns[0], y=plot_df.columns[1])) 
              + geom_point() 
              + facet_wrap("variable"))