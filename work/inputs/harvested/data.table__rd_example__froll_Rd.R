# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: froll.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 78

suppressPackageStartupMessages(library(data.table))
# single vector and single window
frollmean(1:6, 3)

d = as.data.table(list(1:6/2, 3:8/4))
# rollmean of single vector and single window
frollmean(d[, V1], 3)
# multiple columns at once
frollmean(d, 3)
# multiple windows at once
frollmean(d[, .(V1)], c(3, 4))
# multiple columns and multiple windows at once
frollmean(d, c(3, 4))
## three calls above will use multiple cores when available

# other functions
frollsum(d, 3:4)
frollmax(d, 3:4)
frollmin(d, 3:4)
frollprod(d, 3:4)
frollmedian(d, 3:4)
frollvar(d, 3:4)
frollsd(d, 3:4)

# partial=TRUE
x = 1:6/2
n = 3
ans1 = frollmean(x, n, partial=TRUE)
# same using adaptive=TRUE
an = function(n, len) c(seq.int(n), rep.int(n, len-n))
ans2 = frollmean(x, an(n, length(x)), adaptive=TRUE)
all.equal(ans1, ans2)
# speed up by using partial only for incomplete observations
ans3 = frollmean(x, n)
ans3[seq.int(n-1L)] = frollmean(x[seq.int(n-1L)], n, partial=TRUE)
all.equal(ans1, ans3)

# give.names
frollsum(list(x=1:5, y=5:1), c(tiny=2, big=4), give.names=TRUE)

# has.nf=FALSE should be used with care
frollmax(c(1,2,NA,4,5), 2)
frollmax(c(1,2,NA,4,5), 2, has.nf=FALSE)

# use verbose=TRUE for extra insight
.op = options(datatable.verbose = TRUE)
frollsd(c(1:5,NA,7:8), 4)
options(.op)

# performance vs exactness
set.seed(108)
x = sample(c(rnorm(1e3, 1e6, 5e5), 5e9, 5e-9))
n = 15
ma = function(x, n, na.rm=FALSE) {
  ans = rep(NA_real_, nx<-length(x))
  for (i in n:nx) ans[i] = mean(x[(i-n+1):i], na.rm=na.rm)
  ans
}
fastma = function(x, n, na.rm) {
  if (!missing(na.rm)) stop("NAs are unsupported, wrongly propagated by cumsum")
  cs = cumsum(x)
  scs = shift(cs, n)
  scs[n] = 0
  as.double((cs-scs)/n)
}
system.time(ans1<-ma(x, n))
system.time(ans2<-fastma(x, n))
system.time(ans3<-frollmean(x, n))
system.time(ans4<-frollmean(x, n, algo="exact"))
system.time(ans5<-frollapply(x, n, mean))
anserr = list(
  fastma = ans2-ans1,
  froll_fast = ans3-ans1,
  froll_exact = ans4-ans1,
  frollapply = ans5-ans1
)
errs = sapply(lapply(anserr, abs), sum, na.rm=TRUE)
sapply(errs, format, scientific=FALSE) # roundoff