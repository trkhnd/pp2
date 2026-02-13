#--------------------------------------------
nums = [1, 2, 3, 4, 5]
even = list(filter(lambda x: x % 2 == 0, nums))
print(even)

#--------------------------------------------
nums = [10, 15, 20, 25]
big = list(filter(lambda x: x > 15, nums))
print(big)

#--------------------------------------------
words = ["cat", "elephant", "dog"]
long_words = list(filter(lambda w: len(w) > 3, words))
print(long_words)

#--------------------------------------------
nums = [-3, 4, -1, 7]
positive = list(filter(lambda x: x > 0, nums))
print(positive)

#--------------------------------------------
