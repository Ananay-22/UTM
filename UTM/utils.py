def getBlockSize(window_dim, n, multiplier):
        return int(window_dim/ (n * multiplier))

def blockPositiontoGridIndex(x, y, scale_factor):
    i, j = ( int(x * scale_factor), int(y * scale_factor))
    return (i, j)
    
def polToCart(vector):
    (angle,z) = vector
    (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
    return (dx, dy)

def has(x1, y1, x, y, l, b):
    return (
        0 <= x1 -x and x1 - x < l
    ) and (
        0 <= y1 - y and y1 - y < b
    )

from uuid import uuid4

uid = lambda: str(uuid4())