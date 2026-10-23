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
# aqm <- melt(airquality, id=c("month", "day"), na.rm=TRUE)
aqm = airquality.melt(id_vars=["month", "day"], value_vars=["ozone", "solar.r", "wind", "temp"]).dropna()

# acast(aqm, day ~ month ~ variable)
acast_res = aqm.pivot_table(index="day", columns=["month", "variable"], values="value")

# acast(aqm, month ~ variable, mean)
acast_1 = aqm.pivot_table(index="month", columns="variable", values="value", aggfunc="mean")

# acast(aqm, month ~ variable, mean, margins = TRUE)
acast_2 = aqm.pivot_table(index="month", columns="variable", values="value", aggfunc="mean")
acast_2.loc['All'] = acast_2.mean()
acast_2['All'] = acast_2.mean(axis=0)
acast_2.loc['All', 'All'] = acast_2.loc['All'].mean() # Approximation of margins=TRUE

# dcast(aqm, month ~ variable, mean, margins = c("month", "variable"))
dcast_res = aqm.pivot_table(index="month", columns="variable", values="value", aggfunc="mean")
# margins = c("month", "variable") means marginals for those dimensions
dcast_res.loc['All'] = dcast_res.mean()
dcast_res['All'] = dcast_res.mean(axis=0)

# acast(aqm, variable ~ month, mean, subset = .(variable == "ozone"))
acast_3 = aqm[aqm["variable"] == "ozone"].pivot_table(index="variable", columns="month", values="value", aggfunc="mean")

# acast(aqm, variable ~ month, mean, subset = .(month == 5))
acast_4 = aqm[aqm["month"] == 5].pivot_table(index="variable", columns="month", values="value", aggfunc="mean")

# Chick weight example
ChickWeight.columns = [c.lower() for c in ChickWeight.columns]
# id=2:4 (time, chick, diet)
chick_m = ChickWeight.melt(na.rm=True, id_vars=["time", "chick", "diet"], value_vars=["weight"])
chick_m = chick_m.rename(columns={"value": "value", "variable": "variable"})

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
acast_12 = chick_m.pivot_table(index=["diet", "chick"], columns="time", values="value", aggfunc="count")
# margins="diet" means sum across chick for each diet
diet_margins = acast_12.groupby(level='diet').sum()
acast_12 = pd.concat([acast_12, diet_margins])

# acast(chick_m, diet + chick ~ time, length, drop = FALSE)
acast_13 = chick_m.pivot_table(index=["diet", "chick"], columns="time", values="value", aggfunc="count")

# Tips example
# dcast(melt(tips), sex ~ smoker, mean, subset = .(variable == "total_bill"))
tips_m = tips.melt()
dcast_4 = tips_m[tips_m["variable"] == "total_bill"].pivot_table(index="sex", columns="smoker", values="value", aggfunc="mean")

# French Fries example
ff_d = french_fries.melt(na.rm=True, id_vars=["time", "treatment", "subject", "rep"])

# acast(ff_d, subject ~ time, length)
acast_14 = ff_d.pivot_table(index="subject", columns="time", values="value", aggfunc="count")

# acast(ff_d, subject ~ time, length, fill=0)
acast_15 = ff_d.pivot_table(index="subject", columns="time", values="value", aggfunc="count").fillna(0)

# dcast(ff_d, treatment ~ variable, mean, margins = TRUE)
dcast_5 = ff_d.pivot_table(index="treatment", columns="variable", values="value", aggfunc="mean")
dcast_5.loc['All'] = dcast_5.mean()
dcast_5['All'] = dcast_5.mean(axis=0)

# dcast(ff_d, treatment + subject ~ variable, mean, margins="treatment")
dcast_6 = ff_d.pivot_table(index=["treatment", "subject"], columns="variable", values="value", aggfunc="mean")
treat_margins = dcast_6.groupby(level='treatment').mean()
dcast_6 = pd.concat([dcast_6, treat_margins])

# lattice::xyplot approximations
# dcast(ff_d, ... ~ rep) effectively casts everything else to index, rep to column
# In R: xyplot(`1` ~ `2` | variable, ...) where `1` is the value and `2` is the index
cast_ff = ff_d.pivot_table(index=["variable", "rep"], columns="subject", values="value")
# The R plot is variable-faceted, x=subject, y=value (approximately)
plot_df = cast_ff.reset_index().melt(id_vars=["variable", "rep"])
xyplot_res = (ggplot(plot_df, aes(x="variable", y="value")) 
              + geom_point() 
              + facet_wrap("~variable"))