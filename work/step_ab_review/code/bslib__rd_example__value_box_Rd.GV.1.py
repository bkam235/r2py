from shiny import ui

# r2py:entity:value_box
# We use ui.value_box and then print its representation to match R's auto-printing behavior.
# Note: bslib's value_box in R is mirrored by shiny.ui.value_box in Python.
# For icons, we use HTML tags consistent with Bootstrap Icons as used by bsicons.
v_box = ui.value_box(
    "KPI Title",
    ui.h1(ui.HTML("$1 <i>Billion</i> Dollars")),
    ui.span(
        ui.HTML('<i class="bi bi-arrow-up"></i>'),
        " 30% VS PREVIOUS 30 DAYS"
    ),
    showcase=ui.HTML('<i class="bi bi-piggy-bank"></i>'),
    theme="success"
)

print(v_box)