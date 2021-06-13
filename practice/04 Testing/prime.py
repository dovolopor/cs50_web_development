import math

def isPrime(x):
    if x < 2:
        return False
    elif x == 2:
        return True

    for i in range(3, math.ceil(math.sqrt(x) + 1)):
        if( x % i == 0): return False

    return True
