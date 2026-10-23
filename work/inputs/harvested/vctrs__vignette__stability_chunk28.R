# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: stability_chunk28
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\stability.Rmd
# lines: 22

suppressPackageStartupMessages(library(vctrs))
vec_c <- function(...) {
  args <- compact(list2(...))

  ptype <- vec_ptype_common(!!!args)
  if (is.null(ptype))
    return(NULL)

  ns <- map_int(args, vec_size)
  out <- vec_init(ptype, sum(ns))

  pos <- 1
  for (i in seq_along(ns)) {
    n <- ns[[i]]
    
    x <- vec_cast(args[[i]], to = ptype)
    vec_slice(out, pos:(pos + n - 1)) <- x
    pos <- pos + n
  }

  out
}