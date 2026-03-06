import re

# 1. 'a' followed by zero or more 'b's
def task1(s):
    return bool(re.match(r"^ab*$", s))

# 2. 'a' followed by two to three 'b's
def task2(s):
    return bool(re.match(r"^ab{2,3}$", s))

# 3. Find lowercase sequences joined with underscore
def task3(s):
    return re.findall(r"\b[a-z]+_[a-z]+(?:_[a-z]+)*\b", s)

# 4. Find one uppercase letter followed by lowercase letters
def task4(s):
    return re.findall(r"\b[A-Z][a-z]+\b", s)

# 5. 'a' followed by anything, ending in 'b'
def task5(s):
    return bool(re.match(r"^a.*b$", s))

# 6. Replace spaces, commas, or dots with colon
def task6(s):
    return re.sub(r"[ ,.]", ":", s)

# 7. Snake case to camel case
def snake_to_camel(s):
    parts = s.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

# 8. Split string at uppercase letters
def task8(s):
    return re.findall(r"[A-Z][a-z]*", s)

# 9. Insert spaces before capital letters
def task9(s):
    return re.sub(r"(?<!^)([A-Z])", r" \1", s)

# 10. Camel case to snake case
def camel_to_snake(s):
    return re.sub(r"(?<!^)([A-Z])", r"_\1", s).lower()