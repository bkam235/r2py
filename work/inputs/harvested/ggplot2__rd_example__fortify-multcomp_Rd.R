# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: fortify-multcomp.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 31

suppressPackageStartupMessages(library(ggplot2))
if (require("multcomp") && require("broom")) withAutoprint({ # examplesIf
amod <- aov(breaks ~ wool + tension, data = warpbreaks)
wht <- multcomp::glht(amod, linfct = multcomp::mcp(tension = "Tukey"))

tidy(wht) # recommended
fortify(wht)

ggplot(tidy(wht), aes(contrast, estimate)) + geom_point()

ci <- confint(wht)
tidy(ci) # recommended
fortify(ci)

ggplot(tidy(confint(wht)),
       aes(contrast, estimate, ymin = conf.low, ymax = conf.high)) +
   geom_pointrange()

smry <- summary(wht)
tidy(smry) # recommended
fortify(smry)

ggplot(mapping = aes(contrast, estimate)) +
   geom_linerange(aes(ymin = conf.low, ymax = conf.high), data = tidy(ci)) +
   geom_point(aes(size = adj.p.value), data = tidy(smry)) +
   scale_size(transform = "reverse")

cld <- multcomp::cld(wht)
tidy(cld) # recommended
fortify(cld)
}) # examplesIf