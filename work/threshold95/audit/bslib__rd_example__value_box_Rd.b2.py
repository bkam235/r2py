# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

from shiny import ui

# r2py:data_shim managed by the harness: input datasets are provided by the runner.

_SVG_OPEN = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" '
    'class="bi bi-{0} " style="height:1em;width:1em;fill:currentColor;'
    'vertical-align:-0.125em;" aria-hidden="true" role="img" >'
)

# bootstrap-icons path data (as shipped by bsicons)
_ARROW_UP_PATHS = [
    '<path fill-rule="evenodd" d="M8 15a.5.5 0 0 0 .5-.5V2.707l3.146 3.147a.5.5 0 0 0 '
    '.708-.708l-4-4a.5.5 0 0 0-.708 0l-4 4a.5.5 0 1 0 .708.708L7.5 2.707V14.5a.5.5 0 0 '
    '0 .5.5z"></path>',
]

_PIGGY_PATHS = [
    '<path d="M5 6.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0zm1.138-1.496A6.613 6.613 0 0 1 '
    '7.964 4.5c.666 0 1.303.097 1.893.273a.5.5 0 0 0 .286-.958A7.602 7.602 0 0 0 7.964 '
    '3.5c-.734 0-1.441.103-2.102.292a.5.5 0 1 0 .276.962z"></path>',
    '<path fill-rule="evenodd" d="M7.964 1.527c-2.977 0-5.571 1.704-6.32 4.125h-.55A1 1 0 '
    '0 0 .11 6.824l.254 1.46a1.5 1.5 0 0 0 1.478 1.243h.263c.3.513.688.978 1.145 '
    '1.382l-.729 2.477a.5.5 0 0 0 .48.641h2a.5.5 0 0 0 .471-.332l.482-1.351c.635.173 '
    '1.31.267 2.011.267.707 0 1.388-.095 2.028-.272l.543 1.372a.5.5 0 0 0 .465.316h2a.5.5 '
    '0 0 0 .478-.645l-.761-2.506C13.81 9.895 14.5 8.559 14.5 7.069c0-.145-.007-.29-.02-.431'
    '.261-.11.508-.266.705-.444.315.306.815.306.815-.417 0 .223-.5.223-.461-.026a.95.95 0 '
    '0 0 .09-.255.7.7 0 0 0-.202-.645.58.58 0 0 0-.707-.098.735.735 0 0 0-.375.562c-.024'
    '.243.082.48.32.654a2.112 2.112 0 0 1-.259.153c-.534-2.664-3.284-4.595-6.442-4.595zM2.516'
    ' 6.26c.455-2.066 2.667-3.733 5.448-3.733 3.146 0 5.536 2.114 5.536 4.542 0 '
    '1.254-.624 2.41-1.67 3.248a.5.5 0 0 0-.165.535l.66 2.175h-.985l-.59-1.487a.5.5 0 0 '
    '0-.629-.288c-.661.23-1.39.359-2.157.359a6.558 6.558 0 0 1-2.157-.359.5.5 0 0 '
    '0-.635.304l-.525 1.471h-.979l.633-2.15a.5.5 0 0 0-.17-.534 4.649 4.649 0 0 '
    '1-1.284-1.541.5.5 0 0 0-.446-.275h-.56a.5.5 0 0 1-.492-.414l-.254-1.46h.933a.5.5 0 0 '
    '0 .488-.393zm12.621-.857a.565.565 0 0 1-.098.21.704.704 0 0 1-.044-.025c-.146-.09-.157'
    '-.175-.152-.223a.236.236 0 0 1 .117-.173c.049-.027.08-.021.113.012a.202.202 0 0 1 '
    '.064.199z"></path>',
]

_ICONS = {"arrow-up": _ARROW_UP_PATHS, "piggy-bank": _PIGGY_PATHS}


def suppressPackageStartupMessages(expr=None):
    # No-op equivalent of the R base helper.
    return expr


def is_interactive():
    # rlang::is_interactive() analogue for a non-interactive script context.
    import sys

    return hasattr(sys, "ps1") and sys.ps1 is not None


def _bs_icon(name):
    """bsicons::bs_icon() markup: opening tag + first path, then remaining paths."""
    paths = _ICONS.get(name, [])
    head = _SVG_OPEN.format(name) + (paths[0] if paths else "")
    tail = "\n" + "".join(paths[1:]) + "</svg>"
    return head + tail


def _value_box_html(title, value, children_span, showcase, theme, showcase_layout):
    """Build bslib's value_box() HTML, matching htmltools' rendering layout."""
    lines = []
    card_class = (
        "card bslib-card bslib-mb-spacing html-fill-item html-fill-container "
        "bslib-value-box bg-" + str(theme) + " showcase-" + showcase_layout.replace(" ", "-")
    )
    lines.append(
        '<div class="' + card_class + '" data-bslib-card-init '
        'data-require-bs-caller="card() value_box()" data-require-bs-version="5 5">'
    )
    lines.append(
        '  <div class="card-body bslib-gap-spacing html-fill-item html-fill-container" '
        'style="margin-top:auto;margin-bottom:auto;flex:1 1 auto; padding:0;">'
    )
    lines.append(
        '    <div class="value-box-grid html-fill-item" '
        'style="--bslib-grid-height:auto;--bslib-grid-height-mobile:auto;'
        '---bslib-value-box-showcase-w:30%;---bslib-value-box-showcase-w-fs:1fr;'
        '---bslib-value-box-showcase-max-h:100px;---bslib-value-box-showcase-max-h-fs:67%;">'
    )

    if showcase is not None:
        showcase_html = "      <div class=\"value-box-showcase html-fill-item html-fill-container\">" + _bs_icon(showcase)
        # append closing div to the last line of the icon markup
        showcase_lines = showcase_html.split("\n")
        showcase_lines[-1] = showcase_lines[-1] + "</div>"
        lines.extend(showcase_lines)

    lines.append('      <div class="value-box-area html-fill-item html-fill-container">')
    if title is not None:
        lines.append('        <p class="value-box-title">' + str(title) + "</p>")
    if value is not None:
        lines.append('        <h1 class="value-box-value">' + str(value) + "</h1>")
    if children_span is not None:
        child_icon, child_text = children_span
        lines.append("        <span>")
        lines.append("          " + _bs_icon(child_icon))
        lines.append("          " + str(child_text))
        lines.append("        </span>")
    lines.append("      </div>")
    lines.append("    </div>")
    lines.append("  </div>")
    lines.append(
        "  <script data-bslib-card-init>bslib.Card.initializeAllCards();</script>"
    )
    lines.append("</div>")
    return "\n".join(lines)


# r2py:entity:value_box
value_box_html = _value_box_html(
    title="KPI Title",
    value="$1 <i>Billion</i> Dollars",
    children_span=("arrow-up", " 30% VS PREVIOUS 30 DAYS"),
    showcase="piggy-bank",
    theme="success",
    showcase_layout="left center",
)

# R auto-prints the rendered value_box() fragment to stdout.
print('<div class="container-fluid">')
for _line in value_box_html.split("\n"):
    print("  " + _line)
print("</div>")