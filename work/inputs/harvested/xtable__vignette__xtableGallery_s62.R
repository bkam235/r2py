# r2py crawler metadata
# package: xtable
# source_type: vignette
# topic: xtableGallery_s62
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\doc\xtableGallery.R
# lines: 6

suppressPackageStartupMessages(library(xtable))
df.width <- data.frame(One = c("item 1", "A"), Two = c("item 2", "B"),
                       Three = c("item 3", "C"), Four = c("item 4", "D"))
x.width <- xtable(df.width)
align(x.width) <- "|l|X|l|l|l|"
print(x.width, tabular.environment = "tabularx", width = "\\textwidth")