#--------------------------------------------
nums = [5, 1, 3, 2]
sorted_nums = sorted(nums, key=lambda x: x)
print(sorted_nums)

#--------------------------------------------
words = ["apple", "kiwi", "banana"]
sorted_words = sorted(words, key=lambda w: len(w))
print(sorted_words)

#--------------------------------------------
pairs = [(1, 3), (2, 1), (4, 2)]
sorted_pairs = sorted(pairs, key=lambda x: x[1])
print(sorted_pairs)

#--------------------------------------------
names = ["Ali", "dani", "Bob"]
sorted_names = sorted(names, key=lambda x: x.lower())
print(sorted_names)

#--------------------------------------------
