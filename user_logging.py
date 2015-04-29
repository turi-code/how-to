# Use a logger on top of the GraphLab Create loggers. The simplest pattern for
# logging, i.e. `logging.basicConfig(...)`, then `logging.info(...)` does not
# work. It may push messages to stdout, but will not write to a file. The
# following pattern should work.

import time
import logging
import graphlab as gl

## Set up a file handler for the log
handler = logging.FileHandler('my_output.log', mode='w')

## Create the logger, add the file handler, and set the level to 'debug'.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

## Do stuff, and time it
start_time = time.time()
sa = gl.SArray(range(1000000))

## Write an info message to the log
logger.info("Elapsed time: {}".format(time.time() - start_time))

