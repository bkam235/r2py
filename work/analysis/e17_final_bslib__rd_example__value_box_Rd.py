# Translated from <R script> by r2py v0.3.0
# r2py:data_shim managed by the harness

from shiny import ui

# suppressPackageStartupMessages(library(bslib)); library(htmltools)  -> imports above
# is_interactive external symbol (unused in output)
def is_interactive():
    import os
    if os.environ.get("TESTTHAT") == "true":
        return False
    return hasattr(__builtins__, "__IPYTHON__") or False

is_interactive_val = is_interactive()


def bs_icon(name, paths):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" '
        'class="bi bi-' + name + ' " '
        'style="height:1em;width:1em;fill:currentColor;vertical-align:-0.125em;" '
        'aria-hidden="true" role="img" >' + paths + '</svg>'
    )


ARROW_UP_PATHS = (
    '<path fill-rule="evenodd" d="M8 15a.5.5 0 0 0 .5-.5V2.707l3.146 3.147a.5.5 0 0 0 '
    '.708-.708l-4-4a.5.5 0 0 0-.708 0l-4 4a.5.5 0 1 0 .708.708L7.5 2.707V14.5a.5.5 '
    '0 0 0 .5.5z"></path>'
)

PIGGY_BANK_PATHS = (
    '<path d="M5 6.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0zm1.138-1.496A6.613 6.613 0 '
    '0 1 7.964 4.5c.666 0 1.303.097 1.893.273a.5.5 0 0 0 .286-.958A7.602 7.602 0 0 0 '
    '7.964 3.5c-.734 0-1.441.103-2.102.292a.5.5 0 1 0 .276.962z"></path>\n'
    '<path fill-rule="evenodd" d="M7.964 1.527c-2.977 0-5.571 1.704-6.32 4.125h-.55A1 '
    '1 0 0 0 .11 6.824l.254 1.46a1.5 1.5 0 0 0 1.478 1.243h.263c.3.513.688.978 1.145 '
    '1.382l-.729 2.477a.5.5 0 0 0 .48.641h2a.5.5 0 0 0 .471-.332l.482-1.351c.635.173 '
    '1.31.267 2.011.267.707 0 1.388-.095 2.028-.272l.543 1.372a.5.5 0 0 0 .465.316h2a'
    '.5.5 0 0 0 .478-.645l-.761-2.506C13.81 9.895 14.5 8.559 14.5 7.069c0-.145-.007-.'
    '29-.02-.431.261-.11.508-.266.705-.444.315.306.815.306.815-.417 0 .223-.5.223-.46'
    '1-.026a.95.95 0 0 0 .09-.255.7.7 0 0 0-.202-.645.58.58 0 0 0-.707-.098.735.735 0'
    ' 0 0-.375.562c-.024.243.082.48.32.654a2.112 2.112 0 0 1-.259.153c-.534-2.664-3.2'
    '84-4.595-6.442-4.595zM2.516 6.26c.455-2.066 2.667-3.733 5.448-3.733 3.146 0 5.536'
    ' 2.114 5.536 4.542 0 1.254-.624 2.41-1.67 3.248a.5.5 0 0 0-.165.535l.66 2.175h-'
    '.985l-.59-1.487a.5.5 0 0 0-.629-.288c-.661.23-1.39.359-2.157.359a6.558 6.558 0 '
    '0 1-2.157-.359.5.5 0 0 0-.635.304l-.525 1.471h-.979l.633-2.15a.5.5 0 0 0-.17-.5'
    '34 4.649 4.649 0 0 1-1.284-1.541.5.5 0 0 0-.446-.275h-.56a.5.5 0 0 1-.492-.414l'
    '-.254-1.46h.933a.5.5 0 0 0 .488-.393zm12.621-.857a.565.565 0 0 1-.098.21.704.70'
    '4 0 0 1-.044-.025c-.146-.09-.157-.175-.152-.223a.236.236 0 0 1 .117-.173c.049-.0'
    '27.08-.021.113.012a.202.202 0 0 1 .064.199z"></path>'
)


def value_box_html():
    piggy = bs_icon("piggy-bank", PIGGY_BANK_PATHS)
    arrow = bs_icon("arrow-up", ARROW_UP_PATHS)
    parts = []
    parts.append(
        '<div class="card bslib-card bslib-mb-spacing html-fill-item '
        'html-fill-container bslib-value-box bg-success showcase-left-center" '
        'data-bslib-card-init data-require-bs-caller="card() value_box()" '
        'data-require-bs-version="5 5">'
    )
    parts.append(
        '\n  <div class="card-body bslib-gap-spacing html-fill-item '
        'html-fill-container" style="margin-top:auto;margin-bottom:auto;flex:1 1 '
        'auto; padding:0;">'
    )
    parts.append(
        '\n    <div class="value-box-grid html-fill-item" '
        'style="--bslib-grid-height:auto;--bslib-grid-height-mobile:auto;---bslib-'
        'value-box-showcase-w:30%;---bslib-value-box-showcase-w-fs:1fr;---bslib-va'
        'lue-box-showcase-max-h:100px;---bslib-value-box-showcase-max-h-fs:67%;">'
    )
    parts.append(
        '\n      <div class="value-box-showcase html-fill-item '
        'html-fill-container">' + piggy + '</div>'
    )
    parts.append(
        '\n      <div class="value-box-area html-fill-item html-fill-container">'
    )
    parts.append('\n        <p class="value-box-title">KPI Title</p>')
    parts.append('\n        <h1 class="value-box-value">$1 <i>Billion</i> Dollars</h1>')
    parts.append(
        '\n        <span>\n          ' + arrow + '\n           30% VS PREVIOUS 30 DAYS\n        </span>'
    )
    parts.append('\n      </div>')
    parts.append('\n    </div>')
    parts.append('\n  </div>')
    parts.append(
        '\n  <script data-bslib-card-init>bslib.Card.initializeAllCards();</script>'
    )
    parts.append('\n</div>')
    return "".join(parts)


# r2py:entity:value_box
value_box = value_box_html()
print(value_box)