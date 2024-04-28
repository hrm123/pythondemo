from typing import List
import math

'''
Leetcode (912) accepted - runtime beats 10% python3 users. memory beats 90% python3 users
'''
class MergeSortSolution:
    def sortArray(self, nums: List[int]) -> List[int]:
        self.nums = nums
        self.merge_sort(0, len(self.nums)-1)
        return self.nums
    
    def get_mid(self, start, end):
        if (end-start)%2!=0:
            response = start + math.floor((end-start)/2);
        else:
            response = start + ((end-start)/2);
        return int(response)  

    def merge_arrays(self,start: int, mid: int, end: int):
        itr=start
        left_itr = start
        right_itr = mid+1
        response = []
        while(itr!=end  and left_itr<=mid and right_itr<=end):
            if self.nums[left_itr]<self.nums[right_itr]:
                response.append(self.nums[left_itr])
                left_itr = left_itr + 1
            else:
                response.append(self.nums[right_itr])
                right_itr = right_itr + 1
            itr = itr + 1
        while(left_itr<=mid):
            response.append(self.nums[left_itr])
            left_itr += 1
        while(right_itr<=end):
            response.append(self.nums[right_itr])
            right_itr += 1
        itr = start
        iter = 0
        while(itr<=end):
            self.nums[itr] = response[iter]
            iter = iter + 1
            itr = itr + 1
        
    def merge_sort(self,start, end):
        '''
        numbers - array of integer
        start >= 0 based start of current array
        start < n
        '''
        if end==start:
            return
        else :
            mid = self.get_mid(start, end)
            self.merge_sort( start, mid)
            self.merge_sort( mid + 1, end)
            self.merge_arrays(start, mid, end)
            return
        
merge_sort_solution :MergeSortSolution = MergeSortSolution()

print (merge_sort_solution.sortArray([5,2,3,1]))
print (merge_sort_solution.sortArray([5,1,1,2,0,0]))