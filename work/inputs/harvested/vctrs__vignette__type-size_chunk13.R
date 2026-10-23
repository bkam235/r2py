# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: type-size_chunk13
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\type-size.Rmd
# lines: 6

suppressPackageStartupMessages(library(vctrs))
fa <- factor("a")
    fb <- factor("b")
    
    levels(vec_ptype_common(fa, fb))
    levels(vec_ptype_common(fb, fa))