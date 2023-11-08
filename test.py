import re
pattern = "<([?*])>"
s = "<操作><条件>"
results = re.finditer(pattern,s)
for r in re.finditer(pattern,s):
    print(r)
print(r)