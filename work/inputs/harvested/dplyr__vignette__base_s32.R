# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: base_s32
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\base.R
# lines: 5

suppressPackageStartupMessages(library(dplyr))
mtcars_by <- by(mtcars, mtcars$cyl, function(df) {
  with(df, data.frame(cyl = cyl[[1]], mean = mean(disp), n = nrow(df)))
})
do.call(rbind, mtcars_by)