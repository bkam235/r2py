# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: merge_rev.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 35

suppressPackageStartupMessages(library(bit))
merge_rev(1:9)

merge_match(1:7, 3:9)
#' merge_match(merge_rev(1:7), 3:9)
merge_match(merge_rev(1:7), 3:9, revx=TRUE)
merge_match(merge_rev(1:7), 3:9, revy=TRUE)
merge_match(merge_rev(1:7), merge_rev(3:9))

merge_in(1:7, 3:9)
merge_notin(1:7, 3:9)

merge_anyDuplicated(c(1L, 1L, 2L, 3L))
merge_duplicated(c(1L, 1L, 2L, 3L))
merge_unique(c(1L, 1L, 2L, 3L))

merge_union(c(1L, 2L, 2L, 2L), c(2L, 2L, 3L))
merge_union(c(1L, 2L, 2L, 2L), c(2L, 2L, 3L), method="exact")
merge_union(c(1L, 2L, 2L, 2L), c(2L, 2L, 3L), method="all")

merge_setdiff(c(1L, 2L, 2L, 2L), c(2L, 2L, 3L))
merge_setdiff(c(1L, 2L, 2L, 2L), c(2L, 2L, 3L), method="exact")
merge_setdiff(c(1L, 2L, 2L), c(2L, 2L, 2L, 3L), method="exact")

merge_symdiff(c(1L, 2L, 2L, 2L), c(2L, 2L, 3L))
merge_symdiff(c(1L, 2L, 2L, 2L), c(2L, 2L, 3L), method="exact")
merge_symdiff(c(1L, 2L, 2L), c(2L, 2L, 2L, 3L), method="exact")

merge_intersect(c(1L, 2L, 2L, 2L), c(2L, 2L, 3L))
merge_intersect(c(1L, 2L, 2L, 2L), c(2L, 2L, 3L), method="exact")

merge_setequal(c(1L, 2L, 2L), c(1L, 2L))
merge_setequal(c(1L, 2L, 2L), c(1L, 2L, 2L))
merge_setequal(c(1L, 2L, 2L), c(1L, 2L), method="exact")
merge_setequal(c(1L, 2L, 2L), c(1L, 2L, 2L), method="exact")