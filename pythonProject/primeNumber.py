import math
import random


# prime number checker

def is_prime_number(num):
    for temp in range(2, math.ceil(math.sqrt(num))):
        if num % temp == 0:
            return False
    return True


print(is_prime_number(11))
print(is_prime_number(12))
