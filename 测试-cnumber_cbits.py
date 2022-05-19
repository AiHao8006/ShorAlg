from CompoundGates import CompoundGates

CompoundGates = CompoundGates(n=6)

a = [12, 17, 20, 8, 24, 45]
cbits = []
cnumbers = []

for i in a:
    cbits.append(CompoundGates.cnumber_to_cbits(i))

print(cbits)

for i in cbits:
    cnumbers.append(CompoundGates.cbits_to_cnumber(i))

print(cnumbers)

invert = []
for i in a:
    invert.append(CompoundGates.invert(i, 49))
print(invert)

gcd = []
for i in a:
    gcd.append(CompoundGates.gcd(i, 36))
print(gcd)

n = []
for i in a:
    n.append(CompoundGates.find_n(i))
print(n)
print(CompoundGates.find_n(8))