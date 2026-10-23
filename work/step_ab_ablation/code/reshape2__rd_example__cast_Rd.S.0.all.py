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
# names(airquality) <- tolower(names(airquality))
airquality_low = airquality.copy()
airquality_low.columns = [c.lower() for c in airquality_low.columns]

# aqm <- melt(airquality, id=c("month", "day"), na.rm=TRUE)
aqm = airquality_low.melt(id_vars=["month", "day"], value_name="value").dropna()

# acast(aqm, day ~ month ~ variable)
acast_0 = aqm.pivot_table(index="day", columns=["month", "variable"], values="value")

# acast(aqm, month ~ variable, mean)
acast_1 = aqm.pivot_table(index="month", columns="variable", values="value", aggfunc="mean")

# acast(aqm, month ~ variable, mean, margins = TRUE)
acast_2 = aqm.pivot_table(index="month", columns="variable", values="value", aggfunc="mean", margins=True)

# dcast(aqm, month ~ variable, mean, margins = c("month", "variable"))
dcast_0 = aqm.pivot_table(index="month", columns="variable", values="value", aggfunc="mean", margins=True)

# acast(aqm, variable ~ month, mean, subset = .(variable == "ozone"))
acast_3 = aqm[aqm["variable"] == "ozone"].pivot_table(index="variable", columns="month", values="value", aggfunc="mean")

# acast(aqm, variable ~ month, mean, subset = .(month == 5))
acast_4 = aqm[aqm["month"] == 5].pivot_table(index="variable", columns="month", values="value", aggfunc="mean")

# Chick weight example
# names(ChickWeight) <- tolower(names(ChickWeight))
chickweight_low = ChickWeight.copy()
chickweight_low.columns = [c.lower() for c in chickweight_low.columns]

# chick_m <- melt(ChickWeight, id=2:4, na.rm=TRUE)
# R's id=2:4 refers to columns 2, 3, 4: time, chick, diet
chick_m = chickweight_low.melt(id_vars=["time", "chick", "diet"], value_name="value").dropna()

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
# margins="diet" means marginal totals for the diet level
acast_12 = chick_m.pivot_table(index=["diet", "chick"], columns="time", values="value", aggfunc="count", margins=True)

# acast(chick_m, diet + chick ~ time, length, drop = FALSE)
acast_13 = chick_m.pivot_table(index=["diet", "chick"], columns="time", values="value", aggfunc="count")

# Tips example
# dcast(melt(tips), sex ~ smoker, mean, subset = .(variable == "total_bill"))
tips_melted = tips.melt()
dcast_4 = tips_melted[tips_melted["variable"] == "total_bill"].pivot_table(index="sex", columns="smoker", values="value", aggfunc="mean")

# French fries example
# ff_d <- melt(french_fries, id=1:4, na.rm=TRUE)
ff_d = french_fries.melt(id_vars=french_fries.columns[0:4], value_name="value").dropna()

# acast(ff_d, subject ~ time, length)
acast_14 = ff_d.pivot_table(index="subject", columns="time", values="value", aggfunc="count")

# acast(ff_d, subject ~ time, length, fill=0)
acast_15 = ff_d.pivot_table(index="subject", columns="time", values="value", aggfunc="count").fillna(0)

# dcast(ff_d, treatment ~ variable, mean, margins = TRUE)
dcast_5 = ff_d.pivot_table(index="treatment", columns="variable", values="value", aggfunc="mean", margins=True)

# dcast(ff_d, treatment + subject ~ variable, mean, margins="treatment")
dcast_6 = ff_d.pivot_table(index=["treatment", "subject"], columns="variable", values="value", aggfunc="mean", margins=True)

# lattice::xyplot(`1` ~ `2` | variable, dcast(ff_d, ... ~ rep), aspect="iso")
# dcast(ff_d, ... ~ rep) means keep all id vars and cast 'rep' to columns
ff_cast = ff_d.pivot_table(index=["time", "treatment", "subject", "variable"], columns="rep", values="value")
ff_cast = ff_cast.reset_index()
# xyplot(`1` ~ `2` | variable) maps columns 1 and 2 of the dcast result to x and y, faceted by variable
# In R's dcast(ff_d, ... ~ rep), columns `1` and `2` are the first two numeric columns (the reps)
# We will use the first two rep columns as x and y
rep_cols = [c for c in ff_cast.columns if isinstance(c, (int, float)) or (isinstance(c, str) and c.isdigit())]
if len(rep_cols) >= 2:
    xyplot_df = ff_cast[["variable", rep_cols[0], rep_cols[1]]]
    xyplot_df.columns = ["variable", "x", "y"]
    xyplot = (ggplot(xyplot_df, aes(x="x", y="y")) 
              + geom_point() 
              + facet_wrap("~variable"))