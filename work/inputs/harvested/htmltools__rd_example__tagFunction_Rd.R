# r2py crawler metadata
# package: htmltools
# source_type: rd_example
# topic: tagFunction.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\htmltools\help
# lines: 12

suppressPackageStartupMessages(library(htmltools))
myDivDep <- tagFunction(function() {
  if (isTRUE(getOption("useDep", TRUE))) {
    htmlDependency(
      name = "lazy-dependency",
      version = "1.0", src = ""
    )
  }
})
myDiv <- attachDependencies(div(), myDivDep)
renderTags(myDiv)
withr::with_options(list(useDep = FALSE), renderTags(myDiv))