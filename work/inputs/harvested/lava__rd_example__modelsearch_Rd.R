# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: modelsearch.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 9

suppressPackageStartupMessages(library(lava))
m <- lvm();
regression(m) <- c(y1,y2,y3) ~ eta; latent(m) <- ~eta
regression(m) <- eta ~ x
m0 <- m; regression(m0) <- y2 ~ x
dd <- sim(m0,100)[,manifest(m0)]
e <- estimate(m,dd);
modelsearch(e,messages=0)
modelsearch(e,messages=0,type="cor")