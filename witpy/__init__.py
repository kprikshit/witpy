from WitAI import WitAI
import sys
import logging

# Set default logging for the module. Client applications can use a custom
# logging config to override defaults specified here
logging.getLogger(__name__).setLevel(logging.DEBUG)
logging.getLogger(__name__).propagate = False
formatter = logging.Formatter('%(message)s')
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logging.getLogger(__name__).addHandler(handler)
