from shiny import ui

# r2py:entity:value_box
# In R, bslib::value_box is returned and auto-printed. 
# In Python, we must explicitly print it to match the R output.
value_box_result = ui.value_box(
    "KPI Title",
    ui.h1(ui.HTML("$1 <i>Billion</i> Dollars")),
    ui.span(
        ui.HTML('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" class="bi bi-arrow-up" style="height:1em; width:1em;"><path fill="currentColor" d="M8 15a.5.5 0 0 0 .5-.5V2.707l2.146 2.147a.5.5 0 0 0 .708 0l-2.147-2.146a.5.5 0 0 0-.708 0L8 2.707V14.5A.5.5 0 0 0 8 15z"/></svg>'),
        " 30% VS PREVIOUS 30 DAYS"
    ),
    showcase=ui.HTML('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" class="bi bi-piggy-bank" style="height:1em; width:1em;"><path fill="currentColor" d="M7 2.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 .5.5v1h-2a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h2v1a1 1 0 0 1-1 1h-5a1 1 0 0 1-1-1v-1a1 1 0 0 0-1-1v-2a1 1 0 0 0 1-1h2V3.5a.5.5 0 0 1 .5-.5zM3 6a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6zm1 1V6a.5.5 0 0 1 .5-.5h6a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-.5.5H4a.5.5 0 0 1-.5-.5z"/></svg>'),
    theme="success"
)
print(value_box_result)