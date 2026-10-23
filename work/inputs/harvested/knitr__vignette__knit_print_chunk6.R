# r2py crawler metadata
# package: knitr
# source_type: vignette
# topic: knit_print_chunk6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\doc\knit_print.Rmd
# lines: 21

suppressPackageStartupMessages(library(knitr))
knit_print.classA = function(x, ...) {
  # ignore options and inline
}
knit_print.classB = function(x, options, ...) {
  # use the chunk option out.height
  asis_output(paste0(
    '<iframe src="https://yihui.org" height="', options$out.height, '"></iframe>',
  ))
}
knit_print.classC = function(x, inline = FALSE, ...) {
  # different output according to inline=TRUE/FALSE
  if (inline) {
    'inline output for classC'
  } else {
    'chunk output for classC'
  }
}
knit_print.classD = function(x, options, inline = FALSE, ...) {
  # use both options and inline
}