def get_mid(start, end):
    if end-start%2!=0:
        response = ((end-start)/2)+1;
    else:
        response = ((end-start)/2);
    return response

def merge_arrays(left, right):
    itr=0
    left_itr = 0
    right_itr = 0
    response = []
    right_num = left[itr]
    len_right = len(right)
    len_left = len(left)
    while(itr!=(len_right+len_left)  and left_itr<len_right and right_itr<len_right):
        if left[left_itr]<right[right_itr]:
            response.append(left[left_itr])
            left_itr = left_itr + 1
        else:
            response.append(right[right_itr])
            right_itr = right_itr + 1
        itr = itr + 1
    while(left_itr<len_left):
        response.append(left[left_itr])
    while(right_itr<len_right):
        response.append(right[right_itr])

def merge_sort(numbers, start, end):
    '''
    numbers - array of integer
    start >= 0 based start of current array
    start < n
    '''
    if end==start:
        return numbers
    else :
        mid = get_mid(start, end)
        left_numbers = merge_sort(numbers, start, mid)
        right_numbers = merge_sort(numbers, mid + 1, end)
        merged = merge_arrays(left_numbers, right_numbers)
        return merged
    
