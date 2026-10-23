# r2py crawler metadata
# package: caret
# source_type: rd_example
# topic: maxDissim.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\caret\help
# lines: 49

suppressPackageStartupMessages(library(caret))
example <- function(pct = 1, obj = minDiss, ...)
{
  tmp <- matrix(rnorm(200 * 2), nrow = 200)

  ## start with 15 data points
  start <- sample(1:dim(tmp)[1], 15)
  base <- tmp[start,]
  pool <- tmp[-start,]
  
  ## select 9 for addition
  newSamp <- maxDissim(
                       base, pool, 
                       n = 9, 
                       randomFrac = pct, obj = obj, ...)
  
  allSamp <- c(start, newSamp)
  
  plot(
       tmp[-newSamp,], 
       xlim = extendrange(tmp[,1]), ylim = extendrange(tmp[,2]), 
       col = "darkgrey", 
       xlab = "variable 1", ylab = "variable 2")
  points(base, pch = 16, cex = .7)
  
  for(i in seq(along.with = newSamp))
    points(
           pool[newSamp[i],1], 
           pool[newSamp[i],2], 
           pch = paste(i), col = "darkred") 
}

par(mfrow=c(2,2))

set.seed(414)
example(1, minDiss)
title("No Random Sampling, Min Score")

set.seed(414)
example(.1, minDiss)
title("10 Pct Random Sampling, Min Score")

set.seed(414)
example(1, sumDiss)
title("No Random Sampling, Sum Score")

set.seed(414)
example(.1, sumDiss)
title("10 Pct Random Sampling, Sum Score")