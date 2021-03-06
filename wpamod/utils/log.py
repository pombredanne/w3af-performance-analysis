from __future__ import print_function

import logging

from fabric.colors import red, yellow, green


def configure_logging(debug):
    console = ColorLog()
    console.setLevel(logging.DEBUG if debug else logging.INFO)
    logging.getLogger('').addHandler(console)
    logging.getLogger('').setLevel(logging.DEBUG)


class ColorLog(logging.Handler):
    """
    A class to print colored messages to stdout
    """

    COLORS = {
                logging.CRITICAL: red,
                logging.ERROR: red,
                logging.WARNING: yellow,
                logging.INFO: green,
                logging.DEBUG: lambda x: x,
              }
    
    def __init__(self):
        logging.Handler.__init__(self)

    def usesTime(self):
        return False

    def emit(self, record):
        color = self.COLORS.get(record.levelno, lambda x: x)
        print(color(record.msg))
