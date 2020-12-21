
# Question : Given two strings A and B of lowercase letters, return True if and only if we can swap two letters in A so that the result equals B.

def buddy_strings(a_string, b_string):
	"""
		return True if reversed a_string is equals to b_string
		else return False
	"""
	for i in range(len(list(a_string))-1):
		split_a = list(a_string) # list string so we can assign swapped values
		first_string = split_a[i] # swap value to next index string
		second_string = split_a[i+1] # swap value to previous string
		split_a[i] = second_string # assign the current value to next index
		split_a[i+1] = first_string # assign next index value to previous value
		join_a = ''.join(split_a) # join list swapped values
		if join_a == b_string:
			return True
	return False

print (buddy_strings(a, b))
