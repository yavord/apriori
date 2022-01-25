from tokenize import String


count = 0

for i in range(100,999+1):
    as_str = str(i)
    if as_str[0] < as_str[1] and as_str[1] < as_str[2]:
        count += 1

print(count)