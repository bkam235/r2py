# r2py crawler metadata
# package: htmltools
# source_type: rd_example
# topic: tagAddRenderHook.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\htmltools\help
# lines: 48

suppressPackageStartupMessages(library(htmltools))
# Have a place holder div and return a span instead
obj <- div("example", .renderHook = function(x) {
  x$name <- "span"
  x
})
obj$name # "div"
print(obj) # Prints as a `span`

# Add a class to the tag
# Should print a `span` with class `"extra"`
spanExtra <- tagAddRenderHook(obj, function(x) {
  tagAppendAttributes(x, class = "extra")
})
spanExtra

# Replace the previous render method
# Should print a `div` with class `"extra"`
divExtra <- tagAddRenderHook(obj, replace = TRUE, function(x) {
  tagAppendAttributes(x, class = "extra")
})
divExtra

# Add more child tags
spanExtended <- tagAddRenderHook(obj, function(x) {
  tagAppendChildren(x, " ", tags$strong("bold text"))
})
spanExtended

# Add a new html dependency
newDep <- tagAddRenderHook(obj, function(x) {
  fa <- htmlDependency(
    "font-awesome", "4.5.0", c(href="shared/font-awesome"),
    stylesheet = "css/font-awesome.min.css")
  attachDependencies(x, fa, append = TRUE)
})
# Also add a jqueryui html dependency
htmlDependencies(newDep) <- htmlDependency(
  "jqueryui", "1.11.4", c(href="shared/jqueryui"),
  script = "jquery-ui.min.js")
# At render time, both dependencies will be found
renderTags(newDep)$dependencies

# Ignore the original tag and return something completely new.
newObj <- tagAddRenderHook(obj, function(x) {
  tags$p("Something else")
})
newObj