# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: pillar_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\pillar.R
# lines: 34

suppressPackageStartupMessages(library(vctrs))
#' @export
latlon <- function(lat, lon) {
  new_rcrd(list(lat = lat, lon = lon), class = "earth_latlon")
}

#' @export
format.earth_latlon <- function(x, ..., formatter = deg_min) {
  x_valid <- which(!is.na(x))

  lat <- field(x, "lat")[x_valid]
  lon <- field(x, "lon")[x_valid]

  ret <- rep(NA_character_, vec_size(x))
  ret[x_valid] <- paste0(formatter(lat, "lat"), " ", formatter(lon, "lon"))
  # It's important to keep NA in the vector!
  ret
}

deg_min <- function(x, direction) {
  pm <- if (direction == "lat") c("N", "S") else c("E", "W")

  sign <- sign(x)
  x <- abs(x)
  deg <- trunc(x)
  x <- x - deg
  min <- round(x * 60)

  # Ensure the columns are always the same width so they line up nicely
  ret <- sprintf("%d°%.2d'%s", deg, min, ifelse(sign >= 0, pm[[1]], pm[[2]]))
  format(ret, justify = "right")
}

latlon(c(32.71, 2.95), c(-117.17, 1.67))