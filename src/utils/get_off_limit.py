def get_off_limit(page: int, size: int) -> tuple[int, int]:
    """Get offset and limit for pagination."""
    return (page - 1) * size, size