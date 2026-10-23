# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: registerInputHandler.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 12

suppressPackageStartupMessages(library(shiny))
# Register an input handler which rounds a input number to the nearest integer
# In a package, this should be called from the .onLoad function.
registerInputHandler("mypackage.validint", function(x, shinysession, name) {
  if (is.null(x)) return(NA)
  round(x)
})

## On the Javascript side, the associated input binding must have a corresponding getType method:
# getType: function(el) {
#   return "mypackage.validint";
# }