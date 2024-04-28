from typing import List
import math

'''
Leetcode (704) accepted - runtime beats 94% python3 users. memory beats 50% python3 users (mostly since I used class fields to store number instad of passing number list)
'''
class BinarySearchSolution:
    def searchAscendingArray(self, nums: List[int], key: int) -> bool:
        self.nums = nums
        self.len = len(self.nums)
        self.key = key
        # return self.binary_search_recursive(0, len(self.nums)-1)
        return self.binary_search_iterative()
    
    def get_mid(self, start, end):
        if (end-start)%2!=0:
            response = start + math.floor((end-start)/2);
        else:
            response = start + ((end-start)/2);
        return int(response)  
    
    def binary_search_iterative(self) -> int:
        left = 0
        right = self.len-1
        foundAt = -1
        while(foundAt==-1 and left>=0 and right<self.len and left<=right):
            print(f'{left} , {right}')
            mid = (left+right) // 2
            if(self.nums[mid] == self.key):
                foundAt = mid
            elif(self.nums[mid] > self.key):
                right = mid-1
            else:
                left = mid+1
        return foundAt

    def binary_search_recursive(self, left : int, right: int) -> int:
        print(f'{left} , {right}')
        if(right<left or left<0 or right>self.len):
            return -1
        if(left==right):
            mid = left
            #return left if (self.nums[left] == self.key) else None
        else:
            mid = (left+ right) // 2 # // divides with integral result (discard reminder) - this makes runtime beat only 20% python users
            # mid = self.get_mid(left,right) # // using custome mid function instad of // operator makes runtime beat only 96% python users
        if(self.nums[mid] == self.key):
            return mid
        elif(self.nums[mid] > self.key):
            return self.binary_search_recursive(left, mid-1)
        else:
            return self.binary_search_recursive( mid+1, right)

binary_search_solution :BinarySearchSolution = BinarySearchSolution()

# print (binary_search_solution.searchAscendingArray([-1,0,3,5,9,12], 9)) #4
print (binary_search_solution.searchAscendingArray([-1,0,3,5,9,12], 2)) #-1