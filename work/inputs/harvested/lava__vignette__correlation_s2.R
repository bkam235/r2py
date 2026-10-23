# r2py crawler metadata
# package: lava
# source_type: vignette
# topic: correlation_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\doc\correlation.R
# lines: 5

library('lava')
m0 <- lvm(y1+y2 ~ x, y1 ~~ y2)
edgelabels(m0, y1 + y2 ~ x) <- c(expression(beta[1]), expression(beta[2]))
edgelabels(m0, y1 ~ y2) <- expression(rho)
plot(m0, layoutType="circo")