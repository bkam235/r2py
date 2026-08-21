# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/ggplot2__rd_example__Guide_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__Guide_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mpg']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *
from plotnine.data import mpg

# Note: plotnine (the Python port of ggplot2) does not support custom 
# ggproto Guide definitions as R's ggplot2 does. 
# To achieve the visual effect of a descriptive legend label 
# formatted as a sentence, we manipulate the data labels.

# r2py:entity:GuideDescribe
def format_labels_as_sentence(labels):
    labels = list(labels)
    if not labels:
        return ""
    if len(labels) == 1:
        sentence = labels[0]
    else:
        sentence = ", ".join(labels[:-1]) + ", and " + labels[-1]
    return f"A guide showing {sentence} categories"

# Process the data to create a single combined label for the legend
df = mpg.copy()
unique_classes = df['class'].unique().tolist()
sentence_label = format_labels_as_sentence(unique_classes)

# To mimic the custom guide, we create a dummy column for the legend 
# that contains the full sentence, while keeping the colors mapped to the original classes.
# However, plotnine's legend is driven by the scale. 
# The closest approximation in plotnine is to override the legend title or use a custom scale.

# r2py:entity:ggplot
plot = (
    ggplot(df, aes(x='displ', y='hwy', color='class'))
# r2py:entity:geom_point
    + geom_point()
# r2py:entity:guide_describe
    + labs(color=sentence_label) # Using the label as the legend title
    + theme(
        legend_position='bottom',
        legend_title=element_text(size=10),
        legend_text=element_blank() # Hide individual category labels to mimic the R code
    )
)

print(plot)