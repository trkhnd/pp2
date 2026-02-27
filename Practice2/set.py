#-------------------------------------------------
thisset = {"red", "green", "blue"}
print(thisset)

#-------------------------------------------------
thisset = {"red", "green", "blue"}

for x in thisset:
  print(x)

#-------------------------------------------------
thisset = {"red", "green", "blue"}

thisset.add("yellow")

print(thisset)

#-------------------------------------------------
set1 = {"x", "y", "z"}
set2 = {7, 8, 9}

set3 = set1.union(set2)
print(set3)

#-------------------------------------------------
x = frozenset({"red", "green", "blue"})
print(x)        # prints the frozen set (unordered, cannot be changed)
print(type(x))  # <class, "frozenset">

#-------------------------------------------------

