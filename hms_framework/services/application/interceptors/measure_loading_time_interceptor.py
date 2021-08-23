from functools import wraps

from hms_framework.utils import TimeDiff


def measure_loading_time_interceptor(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        time_diff = TimeDiff()
        result = func(*args, **kwargs)
        time_diff.stop()
        return result

    return wrapper
