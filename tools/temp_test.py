import math

temp =  math.log10(math.sqrt(2))
res = 2 * temp ** 2 + temp * math.log10(5) + math.sqrt(temp ** 2 - math.log10(2) + 1)
print(res)


