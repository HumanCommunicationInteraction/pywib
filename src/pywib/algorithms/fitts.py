

def fitts(a : int = 0, b: int = 0, D : float = 1.0, W: float = 1.0, ID: float = 0.0) -> float:
    """
    Fitts' Law predicts the time required to move to a target area based on the distance to the target and the size of the target.

    Parameters:
    a (int): The intercept constant in milliseconds. Default is 0.
    b (int): The slope constant in milliseconds per bit. Default is 0.
    D (float): The distance to the target in arbitrary units. Default is 1.0.
    W (float): The width of the target in arbitrary units. Default is 1.0.

    Returns:
    float: The predicted movement time in milliseconds.
    """
    import math

    if a <= 0 or b <= 0:
        raise ValueError("Constants a and b must be greater than 0.")
    
    if ID <= 0:
        if W <= 0:
            raise ValueError("Target width W must be greater than 0.")
        if D <= 0:
            raise ValueError("Distance to target D must be greater than 0.")
        ID = math.log2(D / W + 1)

    MT = a + b * ID
    return MT
