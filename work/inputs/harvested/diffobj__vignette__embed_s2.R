# r2py crawler metadata
# package: diffobj
# source_type: vignette
# topic: embed_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diffobj\doc\embed.R
# lines: 8

suppressPackageStartupMessages(library(diffobj))
cat(
  as.character(
    diffPrint(
      1:5, 2:6,
      format="html",
      style=list(html.output="diff.w.style")
) ) )