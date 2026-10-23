# r2py crawler metadata
# package: foreach
# source_type: rd_example
# topic: getDoParWorkers.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\foreach\help
# lines: 8

suppressPackageStartupMessages(library(foreach))
cat(sprintf('%s backend is registered\n',
            if(getDoParRegistered()) 'A' else 'No'))
cat(sprintf('Running with %d worker(s)\n', getDoParWorkers()))
(name <- getDoParName())
(ver <- getDoParVersion())
if (getDoParRegistered())
  cat(sprintf('Currently using %s [%s]\n', name, ver))