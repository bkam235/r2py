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

# Air quality example
airquality.columns = [c.lower() for c in airquality.columns]
# melt(airquality, id=c("month", "day"), na.rm=TRUE)
aqm = airquality.melt(id_vars=["month", "day"], value_vars=["ozone", "solar.r", "wind", "temp"], var_name="variable", value_name="value").dropna()

# acast(aqm, day ~ month ~ variable)
# This creates a 3D array in R. In Python, we use a pivot with MultiIndex as an equivalent representation.
acast_0 = aqm.pivot_table(index="day", columns=["month", "variable"], values="value")

# acast(aqm, month ~ variable, mean)
acast_1 = aqm.pivot_table(index="month", columns="variable", values="value", aggfunc="mean")

# acast(aqm, month ~ variable, mean, margins = TRUE)
acast_2 = aqm.pivot_table(index="month", columns="variable", values="value", aggfunc="mean", margins=True)

# dcast(aqm, month ~ variable, mean, margins = c("month", "variable"))
# R's dcast margins=c("month", "variable") means totals for both index and columns. pandas margins=True does this.
dcast_0 = aqm.pivot_table(index="month", columns="variable", values="value", aggfunc="mean", margins=True)

# acast(aqm, variable ~ month, mean, subset = .(variable == "ozone"))
acast_3 = aqm[aqm["variable"] == "ozone"].pivot_table(index="variable", columns="month", values="value", aggfunc="mean")

# acast(aqm, variable ~ month, mean, subset = .(month == 5))
acast_4 = aqm[aqm["month"] == 5].pivot_table(index="variable", columns="month", values="value", aggfunc="mean")

# Chick weight example
ChickWeight.columns = [c.lower() for c in ChickWeight.columns]
# melt(ChickWeight, id=2:4, na.rm=TRUE) -> id is time, chick, diet
chick_m = ChickWeight.melt(id_vars=["time", "chick", "diet"], value_vars=["weight"], var_name="variable", value_name="value").dropna()

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
# margins="diet" in R means marginal sums for diet. Pandas margins=True gives all.
acast_12 = chick_m.pivot_table(index=["diet", "chick"], columns="time", values="value", aggfunc="count", margins=True)

# acast(chick_m, diet + chick ~ time, length, drop = FALSE)
acast_13 = chick_m.pivot_table(index=["diet", "chick"], columns="time", values="value", aggfunc="count")

# Tips example
# dcast(melt(tips), sex ~ smoker, mean, subset = .(variable == "total_bill"))
tips_melted = tips.melt(var_name="variable", value_name="value")
dcast_4 = tips_melted[tips_melted["variable"] == "total_bill"].pivot_table(index="sex", columns="smoker", values="value", aggfunc="mean")

# French Fries example
# melt(french_fries, id=1:4, na.rm=TRUE)
ff_d = french_fries.melt(id_vars=french_fries.columns[0:4], var_name="variable", value_name="value").dropna()

# acast(ff_d, subject ~ time, length)
acast_14 = ff_d.pivot_table(index="subject", columns="time", values="value", aggfunc="count")

# acast(ff_d, subject ~ time, length, fill=0)
acast_15 = ff_d.pivot_table(index="subject", columns="time", values="value", aggfunc="count").fillna(0)

# dcast(ff_d, treatment ~ variable, mean, margins = TRUE)
dcast_5 = ff_d.pivot_table(index="treatment", columns="variable", values="value", aggfunc="mean", margins=True)

# dcast(ff_d, treatment + subject ~ variable, mean, margins="treatment")
dcast_6 = ff_d.pivot_table(index=["treatment", "subject"], columns="variable", values="value", aggfunc="mean", margins=True)

# lattice::xyplot(`1` ~ `2` | variable, dcast(ff_d, ... ~ rep))
# The R code `... ~ rep` in dcast(ff_d, ... ~ rep) casts all remaining variables as index and rep as column.
ff_rep = ff_d.pivot_table(index=["treatment", "subject", "time", "variable"], columns="rep", values="value")
ff_rep = ff_rep.reset_index()
# In R: `1` ~ `2` | variable implies column 1 as y, column 2 as x, facet by variable.
# Since dcast output has reps as columns, the values are in the rep columns.
# We melt the rep columns to create a long format for plotnine.
plot_df = ff_rep.melt(id_vars=["treatment", "subject", "time", "variable"], value_vars=[str(i) for i in range(1, len(ff_rep.columns)-4) if str(i) in ff_rep.columns or i in ff_rep.columns])
# Note: rep indices in french_fries might be 1, 2, etc.
rep_cols = [c for c in ff_rep.columns if c not in ["treatment", "subject", "time", "variable"]]
plot_df = ff_rep.melt(id_vars=["treatment", "subject", "time", "variable"], value_vars=rep_cols, var_name="rep_val", value_name="obs_val")

xyplot_plot = (ggplot(plot_df, aes(x="rep_val", y="obs_val")) 
               + geom_point() 
               + facet_wrap("~variable")
)