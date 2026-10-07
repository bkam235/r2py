---
id: base.paste
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.paste

## Guidance
Translate R `paste` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "9c7c27e0", "r_snippet": "markup <- paste(sep = \"\\n\",\n  \"This is *emphasized* text in markdown.\",\n  htmlPreserve(\"<script>alert(10*2*3);</script>\"),\n  \"Here is some more *emphasized text*.\"\n)", "py_snippet": "def html_preserve(x, inline=\"auto\"):\n    if isinstance(x, list):\n        x = \"\\n\".join(map(str, x))\n    if not x:\n        return x\n    \n    # getOption(\"htmltools.preserve.raw\", FALSE) is FALSE by default\n    return f\"<!--html_preserve-->{x}<!--/html_preserve-->\"\n\ndef htmlPreserve(x):\n    return html_preserve(x, inline=\"auto\")\n# --- Main Script Execution ---\n\nmarkup = \"\\n\".join([\n    \"This is *emphasized* text in markdown.\",", "score": 1.0, "script_id": "htmltools__rd_example__htmlPreserve_Rd.R", "n_calls": 1}
- {"r_hash": "42082a54", "r_snippet": "server <- function(input, output, session) {\n  observe({\n    x <- input$inRadioButtons\n\n    # Can also set the label and select items\n    updateRadioButtons(session, \"inRadioButtons2\",\n      label = paste(\"radioButtons label\", x),\n      choices = x,\n      selected = x\n    )\n  })\n}", "py_snippet": "def server(input, output, session):\n    @reactive.effect\n    def _():\n        x = input.inRadioButtons()\n        \n        # Can also set the label and select items\n        ui.update_radio_buttons(\n            session,\n            \"inRadioButtons2\",\n            label=f\"radioButtons label {x}\",\n            choices=[x],\n            selected=x\n        )", "score": 1.0, "script_id": "shiny__rd_example__updateRadioButtons_Rd.R", "n_calls": 1}

## Edit Examples
(none)
