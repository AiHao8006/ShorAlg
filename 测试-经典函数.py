from ClassicalFuncs import ClassicalFuncs
from ClassicalFuncs import Frac

x = 0.2681

c = ClassicalFuncs.continued_frac(x)
f = ClassicalFuncs.solve_con_frac(c)

print(c)
print(f)
print(ClassicalFuncs.solve_con_frac(c, return_denominator=True))

print(x)
for i in f:
    print(i[0]/i[1]-x)
