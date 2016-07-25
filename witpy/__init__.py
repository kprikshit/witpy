from witpy import WitPy
import sys
import logging

# Default Logger for the module
logging.getLogger(__name__).setLevel(logging.DEBUG)
logging.getLogger(__name__).propagate = False
formatter = logging.Formatter('%(message)s')
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logging.getLogger(__name__).addHandler(handler)
