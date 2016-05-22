"""
star_history

Use github api to get repo's star history information from stargazors data
and return data in json format.
"""


__version__ = '0.0.1'


from .star_history import get_star_history
from .exceptions import (NoEnoughStargazorsError,ReachLimitError,ConnectionError)
