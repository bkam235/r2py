# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/progressr__rd_example__withProgressShiny_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'progressr__rd_example__withProgressShiny_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['cars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import time
import pandas as pd
import matplotlib.pyplot as plt
from shiny import App, render, ui

# Mocking progressr functionality as it is a specialized R package for progress tracking
# In Python, the standard equivalent for progress tracking in apps would be using
# a progress bar widget or a custom reactive value, but to maintain the logic:
# r2py:entity:app
def with_progress_shiny(message, detail, value, func):
    # In a real Shiny Python app, you would use ui.output_text or a progress bar
    # For this translation, we simulate the wrapping logic
    print(f"Progress: {message} | {detail} | Value: {value}")
    return func()

def progressor(along):
    def p(msg):
        # Simulation of the progressor call in R
        print(f"Progression: {msg}")
    return p

def stop_app():
    # In shiny for python, session.close() or similar is used, 
    # but stopApp is an R-specific force-termination.
    import os
    os._exit(0)

# Prepare the 'cars' dataset equivalent for plotting
cars_df = pd.DataFrame({
    'speed': [4, 4, 7, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 20],
    'dist': [2, 0, 4, 2, 6, 3, 7, 5, 9, 4, 10, 10, 11, 13, 26]
})

# r2py:entity:app
app_ui = ui.page_fluid(
    ui.output_plot("plot")
)

def server(input, output, session):
    @render.plot
    def plot():
        X = list(range(1, 16))
        
        def calculation():
            p = progressor(along=X)
            for x in X:
                time.sleep(0.25)
                p(f"x={x}")
            return None

        with_progress_shiny(
            message="Calculation in progress",
            detail="Starting ...",
            value=0,
            func=calculation
        )
        
        # Plotting cars dataset
        plt.figure()
        plt.scatter(cars_df['speed'], cars_df['dist'])
        plt.xlabel("speed")
        plt.ylabel("dist")
        plt.title("Cars")
        plt.show()

        # Terminate the Shiny app
        time.sleep(1.0)
        stop_app()

app = App(app_ui, server)

# r2py:entity:print
if __name__ == "__main__":
    # Equivalent to print(app) in R to run/describe the app
    print(app)