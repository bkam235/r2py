# r2py crawler metadata
# package: whisker
# source_type: rd_example
# topic: iteratelist.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\whisker\help
# lines: 29

suppressPackageStartupMessages(library(whisker))
# create an iteration list from a named vector
x <- c(a=1, b=2)
iteratelist(x)

# iterate over the members of a list
x <- list(name="John", age="30", gender="male")
iteratelist(x, name="variable") 

# iterate over an unnamed vector
values <- c(1,2,3,4)

template <- 
'{{#values}}
* Value: {{.}}
{{/values}}'

whisker.render(template)

#or 

values <- iteratelist(values, value="count")

template <- 
'{{#values}}
* Value: {{count}}
{{/values}}'

whisker.render(template)