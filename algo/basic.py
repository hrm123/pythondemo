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
assert(PrimeFactors(315) == [3,3,5,7])