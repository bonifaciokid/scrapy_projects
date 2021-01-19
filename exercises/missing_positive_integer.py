"""
Hi, here's your problem today. This problem was recently asked by Facebook:

	You are given an array of integers. Return the smallest positive integer that is not present in the array. The array may contain duplicate entries.

	For example, the input [3, 4, -1, 1] should return 2 because it is the smallest positive integer that doesn't exist in the array.

	Your solution should run in linear time and use constant space.
"""

from datetime import datetime
import random

def first_missing_positive(nums):
	"""
		Add 1 from the smallest number in array add return if it doesn't exists
	"""
	max_num = max(nums)
	min_num = min(nums)
	lowest = 0
	for n in nums:
		if n > 1:
			current_lowest = n-1
			if lowest == 0:
				lowest = current_lowest
			else:
				if current_lowest < max_num and current_lowest > min_num and current_lowest not in nums:
					if current_lowest < lowest:
						lowest = current_lowest
	return lowest

nums = [3, 4, -1, 1]
start = datetime.now()
missing = first_missing_positive(nums)
end = datetime.now()
run_time = end - start
print ('smallest missing positive integer is ', missing)
print ('run time =', run_time)



# Still learning how linear time and constant space works, but this is for now. 