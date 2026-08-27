# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 4

import logging

# r2py:entity:myfun
def myfun():
    # Python's logging module serves as the equivalent to otel/lgr
    logger = logging.getLogger("otel")
    logger.info("Log message")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
# r2py:entity:myfun_1
    myfun()