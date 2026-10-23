# r2py crawler metadata
# package: broom
# source_type: vignette
# topic: broom_s11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\doc\broom.R
# lines: 6

suppressPackageStartupMessages(library(broom))
chit <- chisq.test(xtabs(Freq ~ Sex + Class,
  data = as.data.frame(Titanic)
))
tidy(chit)
augment(chit)