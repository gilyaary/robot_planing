import numpy as np

def bubble_zeros(arr):
    last_j = 0
    for i in range(0, len(arr)):
        if arr[i] == 0:
            right_start = max(i + 1, last_j + 1)
            #right_start = i + 1
            for j in range (right_start, len(arr)):
                if arr[j] != 0:
                    #this optimization is so that if we already looked for NON-ZERO at the right side then we should not look again at these places. 
                    # We continue to the right So our complexity is N.
                    # If we just increment to i+1 we may get worst case of N^2 (A string of zeros will be searched over and over ....) 
                    last_j = j
                    n = arr[j]
                    arr[j] = arr[i]
                    arr[i] = n
                    break

#arr = [1,2,3,4,0,0,0,5,0,6,7,8,9,10,11,0,0,12,13]
arr = np.random.randint(2,size=10000)
bubble_zeros(arr)
print(arr)