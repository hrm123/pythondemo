# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 06:30:18 2025

@author: hramm
"""
import math

def NumberOfDigits(n):
    t = 0
    n1=n
    while n1>0:
        t += 1
        n1 = math.floor(n1/10)

    # digits after decimal
    if isinstance(n, float):
        n2 = n - math.floor(n)
        while n2>0 and t<15:  # limit to avoid infinite loop on repeating decimals
            t += 1
            n2 = math.floor(n2/10)

    return t

# assert NumberOfDigits(1) == 1, "NumberOfDigits(1) failed"
# assert NumberOfDigits(10) == 2, "NumberOfDigits(10) failed"
# assert NumberOfDigits(101) == 3, "NumberOfDigits(101) failed"
# assert NumberOfDigits(101.1) != 3, "NumberOfDigits(101.1)!=3 failed"
# assert NumberOfDigits(101.1) == 4, "NumberOfDigits(101.1)==4 failed"

def ReverseNumber(n):
    rev = 0
    n1=n
    ending_zeros = 0
    while n1>0:
        last_digit = n1%10
        if last_digit == 0 and rev==0:
            ending_zeros += 1
        else:
            rev = rev*10 + last_digit
        n1 = math.floor(n1/10) #last digit removed
    return (rev, ending_zeros)

# assert ReverseNumber(1)[0] == 1, "ReverseNumber(1)[0] == 1 failed"
# assert ReverseNumber(123)[0] == 321, "ReverseNumber(123)[0] == 321 failed"
# assert ReverseNumber(100)[0] == 1 and ReverseNumber(100)[1] == 2 , "ReverseNumber(100)[0] == 1 and ReverseNumber(100)[1] == 2 failed"


def IsPalindromeNumber(n):
    n1 = n
    n_rev, ending_zeros = ReverseNumber(n1)
    # print(f"{n_rev}, {ending_zeros}")
    n1 = math.floor(n / 10 ** ending_zeros)
    iter = 0
    trunc_n = math.floor(n1 / 10**ending_zeros)
    return trunc_n == n_rev

def IsPalindromeNumberHacked(n):
    str_n = str(n)
    l = len(str_n)
    if l==1:
        return True
    iter = 0
    while iter < l/2:
        if str_n[iter] != str_n[l-1-iter]:
            return False
        iter += 1
    return True

#assert IsPalindromeNumber(1), "IsPalindromeNumber(1) failed"
#assert IsPalindromeNumber(10) == False, "IsPalindromeNumber(10) == False failed"
#assert IsPalindromeNumber(101), "IsPalindromeNumber(101) failed"
#assert IsPalindromeNumber(26362), "IsPalindromeNumber(26362) failed"

#assert IsPalindromeNumberHacked(1) == IsPalindromeNumber(1), "IsPalindromeNumberHacked(1) == IsPalindromeNumber(1) failed"
#assert IsPalindromeNumberHacked(10)  == IsPalindromeNumber(10), "IsPalindromeNumberHacked(10)  == IsPalindromeNumber(10) failed"
#assert IsPalindromeNumberHacked(101)  == IsPalindromeNumber(101), "IsPalindromeNumberHacked(101)  == IsPalindromeNumber(101) failed"
#assert IsPalindromeNumberHacked(26362) == IsPalindromeNumber(26362), "IsPalindromeNumberHacked(26362) == IsPalindromeNumber(26362) failed"


# O(n) time complexity, O(1) space complexity
def FactorialWhile(n):
    assert n>=0, "n must be non-negative"
    if n==0 or n==1: 
        return 1
    outn = 1 
    n1 = n
    while n1>1:
        outn *= n1
        n1 -= 1
    return outn

# O(n) time complexity, O(1) space complexity
def Factorial(n):
    assert n>=0, "n must be non-negative"
    if n==0 or n==1: 
        return 1
    outn = 1 
    for iter in range(2, n+1):
        outn *= iter
    return outn

# assert Factorial(0) == 1, "Factorial(0) == 1 failed"
# assert Factorial(1) == 1, "Factorial(1) == 1 failed"
# assert Factorial(5) == 120, "Factorial(5) == 120 failed"

# T(n)= T(n-1) + O(1) 
# //  O(1) is for constnat extra work in each level of recursion which is n recursions => O(n), O(n) space complexity due to recursion stack which has n+1 calls at some point of time
def FactorialRecursive(n):
    assert n>=0, "n must be non-negative"
    if n==0: 
        return 1
    return n*FactorialRecursive(n-1)

# assert FactorialRecursive(0) == 1, "FactorialRecursive(0) == 1 failed"
# assert FactorialRecursive(1) == 1, "FactorialRecursive(1) == 1 failed"
# assert FactorialRecursive(5) == 120, "FactorialRecursive(5) == 120 failed"

# O(n log n) time complexity, O(1) space complexity
def NumberOfFivesInFactorizedNumber(n):
    # we can find number of 5's in factorized number by dividing number by 5 until it is no longer divisible by 5
    # it can be optimized further by dividing by higher powers of 5 though
    count = 0
    temp = n
    while temp%5 == 0: # number is multiple of 5
        count += 1
        temp = temp//5
    return count

    

# O(n log n) time complexity (every iteration n will 1/5 ths itself), O(1) space complexity
def TrailingZerosInFactorial(n):
    assert n>=0, "n must be non-negative"
    # we have to find out how many (5,2) pairs are there when all factors of all the numbers from 1 to n are considered
    # we can see that 2's are always more than 5's (since anything that ends in zero also will have 5 and 2), so we just need to count number of 5's
    # depending on how many 5's are there in factorized number and how many 2's are there in the factorized number
    # each (5,2) pair will add one 0. For example 125= 5 * 5 * 5, has three 5's only and hence no zeros
    # 120 = 5 * 2 * 2 * 2 * 3, has one (5,2) pair and hence one zero
    count = 0
    # we need to total the number of 5's in each of the numbers from 1 to n. We already know that 5s will be present in a 
    # number only if the number leaves reminder 0 when divided by 5. So we can skip other numbers
    for iter in range(5, n+1, 5):
        if iter%5 == 0:
                count += NumberOfFivesInFactorizedNumber(iter)
    return count 

# assert TrailingZerosInFactorial(5) == 1, "TrailingZerosInFactorial(5) == 1 failed"
# assert TrailingZerosInFactorial(10) == 2, "TrailingZerosInFactorial(10) == 2 failed"
# assert TrailingZerosInFactorial(100) == 24, "TrailingZerosInFactorial(100) == 24 failed"

# this problem can be solved using Euclidean algorithm - GCD(a,b) = GCD(a-b, b)
# O(log min(x,y)) time complexity, O(1) space complexity
# similar probllems - find the largest square tile that can fill a rectangle of size x by y
# naive approach - start with minimum of these 2 numbers x & y and try all the numbers if any number dividces both x & y until we reach 1 O(min(x,y))
def GCDRecursive(x,y):
    # largest number that divides both x and y
    x1 = x
    if x<y: #swap them so x is always the bigger number
        x = y
        y = x1
    if x%y == 0:
        return y
    return GCDRecursive(x-y, y)

def GCDIterative(x,y): # basic euclidean algorithm to calculate GCD / HCF
    # largest number that divides both x and y
    while x != y:
        if x>y:
            x = x - y
        else:
            y = y - x
    return x

def GCDrecursive(x,y): # optimized euclidean algorithm
    # largest number that divides both x and y 
    # assert(x>y), "x must be greater than y"
    if y==0:
        return x
    else:
        return GCDrecursive(y, x%y) # this also functions to recursive call after swaps the numbers if x<y
    
# assert(GCDIterative(100,200) == 100), "GCD(100,200) == 100 failed"
# assert(GCDIterative(17,13) == 1), "GCD(17,13) == 1 failed"
# assert(GCDIterative(20,30) == 10), "GCD(20,30) == 10 failed"
 
# assert(GCDrecursive(100,200) == 100), "GCD(100,200) == 100 failed"
# assert(GCDrecursive(17,13) == 1), "GCD(17,13) == 1 failed"
# assert(GCDrecursive(20,30) == 10), "GCD(20,30) == 10 failed"


def LCM(x,y): #Least Common Multiple = smalles number that is divisible by both x,y
    # smallest number that is multiple of both x and y
    # LCM of 2 numbers which dont have any common factors is x*y
    #LCM of two numbers which have common factors is (x*y)/GCD(x,y)
    #LCM of 2 numbers the smaller of which divides bigegr number is bugger number
    # naive approach is to iterate numbers starting from max(x,y) to x*y and see which first number is divided by both x,y - O(x*y)
    # LCM(x,y) * GCD(x,y) = x * y => O(log(min(x,y)))
    gcd_xy = GCDrecursive(x,y)
    return (x*y)//gcd_xy


def IsPrime(n):
    # check from 2 to sqrt(n) if any number divides n then n is not prime
    # 2 is the 'only even prime number'. 1 is neither prime nor composite
    # all divisors occur in pairs. Ex for 30 (1,30), (2,15), (3,10),(5,6) => if (x,y) is pair then, let x be smaller number,  x*y =n => x*x <= n => x <= sqrt(n)
    # => if there is divisor which is > sqrt(n) then it will have a pair divisor that is <= sqrt(n). Henc ewe only need to traverse till sqrt(n)
    for iter in range(2,math.ceil(math.sqrt(n))):
        if n%iter ==0:
            return (False,iter)
    return (True,0)

assert(IsPrime(65)[0] == False and IsPrime(65)[1] == 5)
assert(IsPrime(37)[0] == True and IsPrime(37)[1] == 0)


def IsPrime(n):
    # check from 2 to sqrt(n) if any number divides n then n is not prime - O(sqrt(n))
    # 2 is the 'only even prime number'. 1 is neither prime nor composite
    # all divisors occur in pairs. Ex for 30 (1,30), (2,15), (3,10),(5,6) => if (x,y) is pair then, let x be smaller number,  x*y =n => x*x <= n => x <= sqrt(n)
    # => if there is divisor which is > sqrt(n) then it will have a pair divisor that is <= sqrt(n). Henc ewe only need to traverse till sqrt(n)
    for iter in range(2,math.ceil(math.sqrt(n))):
        if n%iter ==0:
            return (False,iter)
    return (True,0)

# assert(IsPrime(65)[0] == False and IsPrime(65)[1] == 5)
# assert(IsPrime(37)[0] == True and IsPrime(37)[1] == 0)

def IsPrimeThriceFaster(n):
    # more efficient method
    # check for 2 and 3 separately and then check for all numbers of form 6k +/- 1 till sqrt(n)
    # if 2 is not divisor then no even number can be divisor (reduces numbers by half)
    # if 3 is not divisor then no number of form 3k can be divisor (reduces numbers by 1/3)
    # Even though we are incrementing by 6, it is still not 6 times faster since we are doing 2 operations in each iteration
    if n == 1:
        return False
    if n==2 or n==3:
        return True
    if n%2 == 0 or n%3==0 :
        return False
    for iter in range(5, math.ceil(math.sqrt(n)),6):
        if n%iter ==0 or n%(iter+2) ==0:
            return False    
    return True

# assert(IsPrimeThriceFaster(65) == False)
# assert(IsPrimeThriceFaster(37) == True)   
# assert(IsPrimeThriceFaster(1031) == True)   # we check iter=5,11,17,23,29 only 5 iterations needed instead of 32 iterations in basic method

def PrimeFactors(n): # prime factors are divisors of n that are prime O(sqrt(n) log(n)) - Naive method
    # we can find prime factors by dividing n by all prime numbers till sqrt(n)
    # any number can be written as product of powers of prime factors
    prime_factors = []
    n1 = n
    # check for 2 separately
    while n1%2 ==0:
        prime_factors.append(2)
        n1 = n1//2
    # check for odd numbers from 3 to sqrt(n)
    for iter in range(3, math.ceil(math.sqrt(n1))+1,2): 
        #O(sqrt(n)) within which O(log(n)) work is done on each iteration due to division of number in while
        # we only check odd numbers since no even number other than 2 is prime
        if IsPrimeThriceFaster(iter):
            while n1%iter ==0:
                prime_factors.append(iter)
                n1 = n1//iter
    # if n1 is still >2 then it is a prime number
    if n1>2:
        prime_factors.append(n1)
    return prime_factors  

# print(PrimeFactorsNaive(315))  # 3,3,5,7
# assert(PrimeFactors(315) == [3,3,5,7])

def FetchDivisors(n):
    # we can find divisors by checking numbers from 1 to sqrt(n)
    # any divisor greater than sqrt(n) will have a pair divisor less than sqrt(n)
    divisors = []
    for iter in range(1, math.ceil(math.sqrt(n))+1):
        if n%iter ==0:
            divisors.append(iter)
            if iter != n//iter: # to avoid adding square root twice
                divisors.append(n//iter) # add the pair divirsor
    divisors.sort() # this will cause O(n log(n))) time complexity though. To avoid this see FetchDivisorsV2 which is O(n)
    return divisors

def FetchDivisorsV2(n):
    # we can find divisors by checking numbers from 1 to sqrt(n)
    # any divisor greater than sqrt(n) will have a pair divisor less than sqrt(n)
    divisors_low = []
    divisors_high = []
    for iter in range(1, math.ceil(math.sqrt(n))+1):
        if n%iter ==0:
            divisors_low.append(iter)
            if iter != n//iter: # to avoid adding square root twice
                divisors_high.append(n//iter) # add the pair divirsor
    divisors_high.reverse() # reverse the high divisors to get them in ascending order
    return divisors_low + divisors_high  # concatenation of two lists


# print(FetchDivisors(36))  # 1,2,3,4,6,9,12,18,36
# assert(FetchDivisors(36) == [1,2,3,4,6,9,12,18,36])
# print(FetchDivisorsV2(36))  # 1,2,3,4,6,9,12,18,36
# assert(FetchDivisorsV2(36) == [1,2,3,4,6,9,12,18,36])

def SieveOfEratosthenes(n): # O(n log log n) time complexity, O(n) space complexity. which is much better than  naive method is O(n sqrt(n)) = O(n power (3/2))
    # find all prime numbers till n
    # create a boolean array of size n+1 and initialize all entries as true. 
    # Since we have marked all numbers (location of that number) that have multiples as false,
    # a value in is_prime[i] will be false if i is Not a prime, else true
    is_prime = [True for iter in range(n+1)]
    is_prime[0] = False
    is_prime[1] = False
    for iter in range(2, math.ceil(math.sqrt(n))+1):
        if is_prime[iter]:
            for multiple in range(2*iter, n+1, iter): # mark all multiples of iter as non-prime 
                is_prime[multiple] = False
    primes = []
    for iter in range(n+1):
        if is_prime[iter]:
            primes.append(iter)
    return primes




def Power(x,n): # time complexity O(log n), space complexity O(1) 
    # log(n) iterations if we use previous product to calculate next product
    # odd number power is special case since it can be always made even power times same number. so it has same complexity
    if n==0:
        return 1
    result = 1
    x1 = x
    n1 = n
    while n1>0: # we go in halving steps -  n,n/2,n/4... to 0 => O(log n)
        if n1%2 == 1: # odd power
            result = result * x1
            n1 -= 1
        else: # even power
            x1 = x1 * x1
            n1 = n1 // 2
    return result

# assert(Power(2,0) == 1), "Power(2,0) == 1 failed"
# assert(Power(2,5) == 32), "Power(2,5) == 32 failed"
# assert(Power(3,4) == 81), "Power(3,4) == 81 failed"
# assert(Power(3,10) == 59049), "PowerByBinaryExponentiation(2,5) == 32 failed"


def PowerWithoutWhile(x,n): # time complexity O(log n), space complexity O(1) - my solution
    # log(n) iterations if we use previous product to calculate next product
    # x, x*x = x2, x2*x2 = x4, x4*x4=x16, x16*x16=x32... => O(log n) time complexity, O(1) space complexity
    # odd number power is special case since it can be always made even power times same number. so it has same complexity
    if n==0:
        return 1
    if n==1:
        return x
    result = 1
    n1 = n
       
    if n%2 == 1: # odd power
        n1 -= 1
    result = x
    for iter in range(math.log2(n1)):
            result *= result
    if n%2 == 1: # odd power
        result = result * x
    return result
        


# assert(PowerWithoutWhile(2,0) == 1), "Power(2,0) == 1 failed"
# assert(PowerWithoutWhile(2,5) == 32), "Power(2,5) == 32 failed"
# assert(PowerWithoutWhile(3,4) == 81), "Power(3,4) == 81 failed"
# assert(PowerWithoutWhile(3,10) == 59049), "PowerByBinaryExponentiation(2,5) == 32 failed"


# assert(Power(2,0) == 1), "Power(2,0) == 1 failed"
# assert(Power(2,5) == 32), "Power(2,5) == 32 failed"
# assert(Power(3,4) == 81), "Power(3,4) == 81 failed"
# assert(Power(3,10) == 59049), "PowerByBinaryExponentiation(2,5) == 32 failed"

def PowerRecursive(x,n): # time complexity O(log n), space complexity O(1)
    # log(n) iterations if we use previous product to calculate next product
    # x, x*x = x2, x2*x2 = x4, x4*x4=x16, x16*x16=x32... => O(log n) time complexity, O(1) space complexity
    # odd number power is special case since it can be always made even power times same number. so it has same complexity
    if n==0:
        return 1
    if n%2 == 1: # odd power
        return x * PowerRecursive(x, n-1)
    else: # even power
        return PowerRecursive(x, n//2) * PowerRecursive(x, n//2)

# assert(PowerRecursive(2,0) == 1), "PowerRecursive(2,0) == 1 failed"
# assert(PowerRecursive(2,5) == 32), "PowerRecursive(2,5) == 32 failed"
# assert(PowerRecursive(3,4) == 81), "PowerRecursive(3,4) == 81 failed"


def GetBits(n): # TODO Understand the mod and div approach.  optimize this function to directly return list of bits without using mod and div operators
    # get bits of n in LSB to MSB order
    bits = []
    n1 = n
    while n1>0: # O(log(n))
        bits.append(n1%2) # if current number is even then LSB is 0 else 1
        n1 = n1//2 # each iteration you half the number - this operator does floor division
    return bits

#assert(GetBits(10) == [0,1,0,1]), "GetBits(10) == [0,1,0,1] failed"


def PowerByBinaryExponentiation(x,n): # time complexity O(log n), space complexity O(1) - same as previous 'power' method.. but more explained
    # any number can be written as multiplication of powers of 2 - 
    # basically binary representation of a number, ex: binary representation of 10 is 1010
    # since binary representation has log n bits, we can find power in log n time - eah iteration we multiple by power of 2
    # x^n = x^(b0*2^0 + b1*2^1 + b2*2^2 + ... + bk*2^k) where bi is 0 or 1
    # = x^(b0*2^0) * x^(b1*2^1) * x^(b2*2^2) * ... * x^(bk*2^k)
    # where bi is 0 or 1
    # for example to find x^13
    # ex: 13 = 8 + 4 + 1 = 2^3 + 2^2 + 2^0 => x^13 = x^(2^3) * x^(2^2) * x^(2^0)
    # we can find powers of 2 by squaring the previous power
    if n ==0:
        return 1
    if n ==1:
        return x
    
    bits = GetBits(n) # get bits of n in LSB to MSB order
    print(f"bits of {n} are {bits}")
    #iterate over bits and multiply corresponding powers of 2
    result = 1
    tmp = x # x^(2^0)
    for indx,bit in enumerate(bits):
        if bit == 1:
            print(f"bit at index {indx} is 1, including (x ** 'power_of_2_at_current_bit') to result")
            result *= tmp # we are just adding to result if bit at current place is 1
        tmp = tmp * tmp # square the previous power to get next power of 2
    return result

# assert(PowerByBinaryExponentiation(2,0) == 1), "PowerByBinaryExponentiation(2,0) == 1 failed"
# assert(PowerByBinaryExponentiation(3,10) == 59049), "PowerByBinaryExponentiation(2,5) == 32 failed"
# assert(PowerByBinaryExponentiation(3,4) == 81), "PowerByBinaryExponentiation(3,4) == 81 failed"