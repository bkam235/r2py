# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: join_by.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 84

suppressPackageStartupMessages(library(dplyr))
sales <- tibble(
  id = c(1L, 1L, 1L, 2L, 2L),
  sale_date = as.Date(c("2018-12-31", "2019-01-02", "2019-01-05", "2019-01-04", "2019-01-01"))
)
sales

promos <- tibble(
  id = c(1L, 1L, 2L),
  promo_date = as.Date(c("2019-01-01", "2019-01-05", "2019-01-02"))
)
promos

# Match `id` to `id`, and `sale_date` to `promo_date`
by <- join_by(id, sale_date == promo_date)
left_join(sales, promos, by)

# For each `sale_date` within a particular `id`,
# find all `promo_date`s that occurred before that particular sale
by <- join_by(id, sale_date >= promo_date)
left_join(sales, promos, by)

# For each `sale_date` within a particular `id`,
# find only the closest `promo_date` that occurred before that sale
by <- join_by(id, closest(sale_date >= promo_date))
left_join(sales, promos, by)

# If you want to disallow exact matching in rolling joins, use `>` rather
# than `>=`. Note that the promo on `2019-01-05` is no longer considered the
# closest match for the sale on the same date.
by <- join_by(id, closest(sale_date > promo_date))
left_join(sales, promos, by)

# Same as before, but also require that the promo had to occur at most 1
# day before the sale was made. We'll use a full join to see that id 2's
# promo on `2019-01-02` is no longer matched to the sale on `2019-01-04`.
sales <- mutate(sales, sale_date_lower = sale_date - 1)
by <- join_by(id, closest(sale_date >= promo_date), sale_date_lower <= promo_date)
full_join(sales, promos, by)

# ---------------------------------------------------------------------------

segments <- tibble(
  segment_id = 1:4,
  chromosome = c("chr1", "chr2", "chr2", "chr1"),
  start = c(140, 210, 380, 230),
  end = c(150, 240, 415, 280)
)
segments

reference <- tibble(
  reference_id = 1:4,
  chromosome = c("chr1", "chr1", "chr2", "chr2"),
  start = c(100, 200, 300, 415),
  end = c(150, 250, 399, 450)
)
reference

# Find every time a segment `start` falls between the reference
# `[start, end]` range.
by <- join_by(chromosome, between(start, start, end))
full_join(segments, reference, by)

# If you wanted the reference columns first, supply `reference` as `x`
# and `segments` as `y`, then explicitly refer to their columns using `x$`
# and `y$`.
by <- join_by(chromosome, between(y$start, x$start, x$end))
full_join(reference, segments, by)

# Find every time a segment falls completely within a reference.
# Sometimes using `x$` and `y$` makes your intentions clearer, even if they
# match the default behavior.
by <- join_by(chromosome, within(x$start, x$end, y$start, y$end))
inner_join(segments, reference, by)

# Find every time a segment overlaps a reference in any way.
by <- join_by(chromosome, overlaps(x$start, x$end, y$start, y$end))
full_join(segments, reference, by)

# It is common to have right-open ranges with bounds like `[)`, which would
# mean an end value of `415` would no longer overlap a start value of `415`.
# Setting `bounds` allows you to compute overlaps with those kinds of ranges.
by <- join_by(chromosome, overlaps(x$start, x$end, y$start, y$end, bounds = "[)"))
full_join(segments, reference, by)