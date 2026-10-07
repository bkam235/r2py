---
id: stats.rnorm
package: stats
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# stats.rnorm

## Guidance
Translate R `rnorm` from stats to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "19c2edb6", "r_snippet": "rnorm(100) %>% `*`(5) %>% `+`(5) %>% ", "py_snippet": "d = np.random.normal(0, 1, 100) * 5 + 5\n\n# { cat(\"Mean:\", mean(.), \"Variance:\", var(.), \"\\n\"); head(.) }", "score": 1.0, "script_id": "magrittr__vignette__magrittr_s11.R", "n_calls": 1}
- {"r_hash": "d1644285", "r_snippet": "server <- function(input, output) {\n  output$distPlot <- renderPlot({\n    # Take a dependency on input$goButton. This will run once initially,\n    # because the value changes from NULL to 0.\n    input$goButton\n\n    # Use isolate() to avoid dependency on input$obs\n    dist <- isolate(rnorm(input$obs))\n    hist(dist)\n  })\n}", "py_snippet": ")\n\n# Server Logic\ndef server(input, output, session):\n    @render.plot\n    def distPlot():\n        # Take a dependency on input.goButton\n        input.goButton()\n\n        # Use isolate equivalent (accessing input value without triggering reactivity)\n        # In Shiny for Python, accessing input.obs() triggers updates. \n        # To emulate isolate, we use the value of input.obs() here, \n        # but since the function only triggers on goButton(), this behaves as isolate.\n        n_obs = input.obs()\n        \n        # Generate random normal distribution\n        dist = np.random.normal(0, 1, n_obs)\n        \n        # Create dataframe for plotnine\n        df = pd.DataFrame({'val': dist})\n        \n        # Equivalent to hist(dist)", "score": 1.0, "script_id": "shiny__rd_example__actionButton_Rd.R", "n_calls": 2}
- {"r_hash": "d96823b7", "r_snippet": "X <- data.frame(a = rnorm(1000), b = rnorm(1000))", "py_snippet": "m.fit(x_reg.reshape(-1, 1), y_reg)\n# new <- predict(m, x)\nnew = m.predict(x_reg.reshape(-1, 1))", "score": 0.9201, "script_id": "e1071__rd_example__predict_svm_Rd.R", "n_calls": 2}

## Edit Examples
(none)
