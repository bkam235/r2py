# r2py crawler metadata
# package: foreach
# source_type: rd_example
# topic: getDoSeqWorkers.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\foreach\help
# lines: 8

suppressPackageStartupMessages(library(foreach))
cat(sprintf('%s backend is registered\n',
            if(getDoSeqRegistered()) 'A' else 'No'))
cat(sprintf('Running with %d worker(s)\n', getDoSeqWorkers()))
(name <- getDoSeqName())
(ver <- getDoSeqVersion())
if (getDoSeqRegistered())
  cat(sprintf('Currently using %s [%s]\n', name, ver))