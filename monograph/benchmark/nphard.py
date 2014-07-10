#!/usr/bin/env python
import re

clauses = [[1,2,-3], [1,-2,3], [-1,-2,3], [-1,-2,-3]]
#(x1 or not x2 or x3) and (x1 or not x2 or x3) and 
#(not x1 or not x2 or x3) and (not x1 or not x2 or not x3)

v = reduce(lambda a, b: max(a, *b), clauses, 0)
s = v * 'x' + ';' + len(clauses) * 'x,'
e = '^' + v * '(x?)' + '.*;' + ''.join(
    '(?:' + '|'.join(
        '\\' + (str(-x) + 'x' if x < 0 else str(x)) 
        for x in clause) + '),' 
    for clause in clauses)

print re.match(e, s).groups()


