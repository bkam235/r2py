# r2py crawler metadata
# package: whisker
# source_type: rd_example
# topic: whisker-package.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\whisker\help
# lines: 30

suppressPackageStartupMessages(library(whisker))
template <- 
'Hello {{name}}
You have just won ${{value}}!
{{#in_ca}}
Well, ${{taxed_value}}, after taxes.
{{/in_ca}}'

data <- list( name = "Chris"
            , value = 10000
            , taxed_value = 10000 - (10000 * 0.4)
            , in_ca = TRUE
            )

whisker.render(template, data)




base <-
'<h2>Names</h2>
{{#names}}
  {{> user}}
{{/names}}'

user <- '<strong>{{name}}</strong>'

names <- list(list(name="Alice"), list(name="Bob"))

whisker.render(base, partials=list(user=user))