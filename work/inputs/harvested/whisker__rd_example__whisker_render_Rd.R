# r2py crawler metadata
# package: whisker
# source_type: rd_example
# topic: whisker.render.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\whisker\help
# lines: 15

suppressPackageStartupMessages(library(whisker))
template <- "Hello {{place}}!"
place <- "World"

whisker.render(template)

# to prevent html escaping use triple {{{}}}
template <- 
  "I'm escaped: {{name}}
And I'm not: {{{name}}}"

data <- list( name = '<My Name="Nescio&">')
whisker.render(template, data)
# I'm escaped: &lt;My Name=&quot;Nescio&amp;&quot;&gt;
# And I'm not: <My Name="Nescio&">