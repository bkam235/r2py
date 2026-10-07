---
id: base.summary
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.summary

## Guidance
Translate R `summary` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "55b8d38b", "r_snippet": "x <- summary(fit4,times=10,newdata=expand.grid(age=c(60,40,50),sex=c(\"male\",\"female\")))", "py_snippet": "print(fit3_summary.round(3))\n\n# stratified Beran estimator\n# -----------------------------------------------------------------------------------------\nfit4_results = []\nnewdata4 = pd.DataFrame({'age': [20, 50, 70], 'sex': ['female', 'male', 'male']})\nfor _, row in newdata4.iterrows():\n    subset = d[(d['sex'] == row['sex']) & (d['age'] >= row['age'] - 5) & (d['age'] <= row['age'] + 5)]\n    if len(subset) == 0: subset = d[d['sex'] == row['sex']]\n    st = prodlim_summary_table(subset, [1, 5, 10], percent=True)", "score": 1.0, "script_id": "prodlim__rd_example__summary_prodlim_Rd.R", "n_calls": 2}
- {"r_hash": "a45705c2", "r_snippet": "shinyApp(\n  ui = basicPage(\n    actionButton(\"show\", \"Show modal dialog\"),\n    verbatimTextOutput(\"dataInfo\")\n  ),\n\n  server = function(input, output) {\n    # reactiveValues object for storing current data set.\n    vals <- reactiveValues(data = NULL)\n\n    # Return the UI for a modal dialog with data selection input. If 'failed' is\n    # TRUE, then display a message that the previous value was invalid.\n    dataModal <- function(failed = FALSE) {\n      modalDialog(\n        textInput(\"dataset\", \"Choose data set\",\n          placeholder = 'Try \"mtcars\" or \"abc\"'\n        ),\n        span('(Try the name of a valid data object like \"mtcars\", ',\n             'then a name of a non-existent object like \"abc\")'),\n        if (failed)\n          div(tags$b(\"Invalid name of data object\", style = \"color: red;\")),\n\n        footer = tagList(\n          modalButton(\"Cancel\"),\n          actionButton(\"ok\", \"OK\")\n        )\n      )\n    }\n\n    # Show modal when button is clicked.\n    observeEvent(input$show, {\n ", "py_snippet": "mtcars = pd.DataFrame({\"mpg\": [21.0, 21.0], \"cyl\": [6, 6]})\n\ndef server3(input, output, session):\n    vals = reactive.Value(None)\n\n    def data_modal(failed=False):\n        return ui.modal_dialog(\n            ui.input_text(\"dataset\", \"Choose data set\", placeholder='Try \"mtcars\" or \"abc\"'),\n            ui.span('(Try the name of a valid data object like \"mtcars\", then a name of a non-existent object like \"abc\")'),\n            ui.div(ui.tags.b(\"Invalid name of data object\", style=\"color: red;\")) if failed else None,\n            footer=ui.tag_list(\n                ui.modal_button(\"Cancel\"),\n                ui.input_action_button(\"ok\", \"OK\")\n            )\n        )\n\n    @reactive.effect\n    def _():\n        if input.show():\n            ui.show_modal(data_modal())\n\n    @reactive.effect\n    def _():\n        if input.ok():\n            dataset_name = input.dataset()\n            # Approximation of R's exists() and get() using globals()\n            if dataset_name and dataset_name in globals() and isinstance(globals()[dataset_name], pd.DataFrame):\n                vals.set(globals()[dataset_name])\n                ui.remove_modal()\n            else:\n                ui.show_modal(data_modal(failed=True))\n\n    @render.text\n    def dataInfo():\n        d = vals.get()\n        if d is None:\n            return \"No data selected\"\n        else:\n            return str(d.describe())\n\napp3 = App(\n    ui=ui.page_bootstrap(\n        ui.input_action_button(\"show\", \"Show modal dialog\"),\n        ui.output_text_verbatim(\"dataInfo\")", "score": 1.0, "script_id": "shiny__rd_example__modalDialog_Rd.R", "n_calls": 6}

## Edit Examples
(none)
