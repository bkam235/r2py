# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/shiny__rd_example__withProgress_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shiny__rd_example__withProgress_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['cars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from shiny import App, ui, render, reactive

# r2py:entity:ui
ui = ui.page_fluid(
    ui.output_plot("plot")
)

# r2py:entity:server
def server(input, output, session):
    @output
    @render.plot
    def plot():
        with ui.with_progress(
            message='Calculation in progress',
            detail='This may take a while...', 
            value=0
        ) as progress:
            for i in range(1, 16):
                progress.inc(1/15)
                time.sleep(0.25)
        
        # Using a sample dataset similar to R's 'cars'
        # cars dataset in R: speed vs dist
        cars_data = pd.DataFrame({
            'speed': [4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18, 19, 19, 19, 20, 20, 20],
            'dist': [160, 160, 160, 190, 190, 190, 200, 200, 200, 220, 220, 220, 240, 240, 240, 260, 260, 260, 280, 280, 280, 300, 300, 300, 320, 320, 320, 340, 340, 340, 360, 360, 360, 380, 380, 380, 400, 400, 400, 420, 420, 420, 440, 440, 440, 460, 460, 460, 480, 480, 480]
        })
        plt.scatter(cars_data['speed'], cars_data['dist'])
        plt.xlabel('speed')
        plt.ylabel('dist')
        return plt.gcf()

# r2py:entity:shinyApp
app = App(ui, server)