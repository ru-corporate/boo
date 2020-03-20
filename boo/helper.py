def as_mb(n_bytes: int) -> int:
    m = n_bytes / (1024 ** 2)
    return int(round(m, 0))
