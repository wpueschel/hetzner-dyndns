class StaleCacheError(Exception):
    # Exception to be raised, when the cache is stale
    pass

class GetExternalIPError(Exception):
    # Exception to be raised, when external IP could not be determined
    pass
