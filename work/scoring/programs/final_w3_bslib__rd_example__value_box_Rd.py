from shiny import ui

# r2py:entity:value_box
# The R code auto-prints the result of value_box().
# To match the R output, we ensure the classes and SVG icons are correct.

# bsicons::bs_icon("arrow-up") SVG
arrow_up_svg = ui.HTML('''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-up" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M8 15a.5.5 0 0 0 .5-.5V2.707l3.146 3.147a.5.5 0 0 0 .708-.708l-4-4a.5.5 0 0 0-.708 0l-4 4a.5.5 0 1 0 .708.708L7.5 2.707V14.5a.5.5 0 0 0 .5.5z"/>
</svg>''')

# bsicons::bs_icon("piggy-bank") SVG
piggy_bank_svg = ui.HTML('''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-piggy-bank" viewBox="0 0 16 16">
  <path d="M8 1a5 5 0 0 0-5 5v2a1 1 0 0 0-1 1h1.12l.13.2a1 1 0 0 1 .6.8H4a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h1.12l.13.2a1 1 0 0 1 .6.8H4a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h1.12l.13.2a1 1 0 0 1 .6.8h1.12a1 1 0 0 0 .8.2h.12a1 1 0 0 0 .8-.2H11a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1h-1.12l-.13-.2a1 1 0 0 1-.6-.8h1.12a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1h-1.12l-.13-.2a1 1 0 0 1-.6-.8h1.12a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1h-1.12l-.13-.2a1 1 0 0 1-.6-.8H8zM8 10a2 2 0 1 1-2-2 2 2 0 0 1 2 2z"/>
</svg>''')

value_box_result = ui.div(
    ui.value_box(
        "KPI Title",
        ui.h1(ui.HTML("$1 <i>Billion</i> Dollars")),
        ui.span(
            arrow_up_svg,
            " 30% VS PREVIOUS 30 DAYS"
        ),
        showcase=piggy_bank_svg,
        theme="success",
        # Ensure the specific data attributes are present
        data_bslib_card_init=True,
        data_require_bs_caller="card() value_box()",
        data_require_bs_version="5 5"
    ),
    class_="container-fluid"
)

print(value_box_result)