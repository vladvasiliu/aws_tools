try:
    from .prod import *
except ModuleNotFoundError:
    from .dev import *
