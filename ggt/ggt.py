def ggt(a: int, b: int) -> int:
    while b != 0:
        h = a % b
        a = b
        b = h
    return a
