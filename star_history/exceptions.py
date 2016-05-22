"""
star_history's exceptions
"""


class StarHistoryError(Exception):
    pass


class NoEnoughStargazorsError(StarHistoryError):
    """
    Throw this error when repo's stargazor is less than 30
    """
    pass


class ReachLimitError(StarHistoryError):
    """
    Throw this error when reach github api's connect limit
    """
    pass


class ConnectionError(StarHistoryError):
    """
    Throw this error when meet net connect problem
    """
    pass
