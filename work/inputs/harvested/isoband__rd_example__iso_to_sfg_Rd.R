# r2py crawler metadata
# package: isoband
# source_type: rd_example
# topic: iso_to_sfg.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\isoband\help
# lines: 61

suppressPackageStartupMessages(library(isoband))
if (requireNamespace("sf", quietly = TRUE)) {
library(sf)
library(ggplot2)

# Example 1: simple 5x5 matrix
m <- matrix(c(0, 2, 2, 2, 0,
              0, 1, 0, 1, 0,
              0, 1, 0, 0, 0,
              0, 1, 0, 1, 0,
              0, 0, 0, 0, 0), 5, 5, byrow = TRUE)

z <- isolines(1:ncol(m), nrow(m):1, m, c(0.5, 1.5))
lines <- iso_to_sfg(z)
x <- st_sf(level = names(lines), geometry = st_sfc(lines))
ggplot(x) + geom_sf(aes(color = level))

# Example 2: volcano dataset
m <- volcano
b <- isobands((1:ncol(m))/(ncol(m)+1), (nrow(m):1)/(nrow(m)+1), m,
              10*9:19, 10*10:20)
bands <- iso_to_sfg(b)
x <- st_sf(level = as.numeric(sub(":.*", "", names(bands))), geometry = st_sfc(bands))
ggplot(x) + geom_sf(aes(color = level, fill = level))

# Example 3: invalid simple features
m <- matrix(c(1.5, 1.5, 1.5, 1.5, 0.6,
              0.5, 1.5, 1.5,   0,   0,
                0,   1,   0,   1,   1,
                0,   1,   0, 0.7,   0,
              0.9, 1.3, 1.8, 1.4, 0.4), 5, 5, byrow = TRUE)

raw <- isobands(1:5, 5:1, m, levels_low = 0:1, levels_high = 1:2)
bands <- iso_to_sfg(raw)

iso <- st_sf(
  id = factor(1:length(bands)),
  geometry = st_sfc(bands)
)

# the geometries are not valid
st_is_valid(iso, reason = TRUE)
# this doesn't prevent us from plotting them
ggplot(iso, aes(fill = id)) + geom_sf()

# make all geometries valid, requires GEOS >= 3.8.0
if (sf_extSoftVersion()["GEOS"] >= "3.8.0") {
  iso2 <- st_make_valid(iso)
  st_is_valid(iso2, reason=TRUE)
  # the plot should be unchanged
  ggplot(iso2, aes(fill = id)) + geom_sf()
}

# alternatively, if we shift all data values by a tiny
# amount (here, 1e-10) so they don't coincide with the band
# limits, no invalid geometries are generated.
raw <- isobands(1:5, 5:1, m + 1e-10, levels_low = 0:1, levels_high = 1:2)
bands <- iso_to_sfg(raw)
iso <- st_sf(id = factor(1:length(bands)), geometry = st_sfc(bands))
st_is_valid(iso, reason = TRUE)
}