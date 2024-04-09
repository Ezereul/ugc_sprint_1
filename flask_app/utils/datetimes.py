from datetime import datetime


def datetime_now() -> datetime:
    """Get current datetime WITHOUT MICROSECONDS."""

    return datetime.now().replace(microsecond=0)
