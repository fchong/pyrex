# -*- coding: utf-8 -*-
from collections import deque
from functools import reduce

def rex(pattern):
    tokens = deque(pattern)

    def walk(chars):
        while tokens and tokens[0] in chars:
            yield tokens.popleft()

    def option():
        e = sequence()
        for token in walk('|'):
            e2 = sequence()
            e = [(1, len(e)+2)] + e + [(len(e2)+1,)] + e2
        return e        

    def sequence():
        e = []
        while tokens and tokens[0] not in '|)':
            e += repetition()
        return e
        
    def repetition():
        e = primary()
        for token in walk('?*+'):
            if token in '+*': e = e + [(1, -len(e))]
            if token in '?*': e = [(1, len(e)+1)] + e
        return e
        
    def primary():
        token = tokens.popleft()
        if token == '.': return [None]
        if token == '(': return [option(), tokens.popleft()][0]
        if token not in '?*+)|': return [token]
        raise Exception('Not expected: "{}"'.format(token))

    e = option()
    if tokens: 
        raise Exception('Not expected: "{}"'.format(''.join(tokens)))

    return Machine(e)
                
class Machine(object):
    def __init__(self, states):
        self.states = states
        self.n = len(states)
        
    def matcher(self, string):
        A, B, V = list(), list(), [-1]*len(self.states)
            
        def addnext(start, i, j):
            if j==self.n: return 1
            if V[j] == i: return 0
            V[j] = i

            if isinstance(self.states[j], tuple):
                return sum(addnext(start, i, j+k) for k in self.states[j])

            B.append((start, j))
            return 0
        
        def key(a): return (a[1]-a[0], -a[0]) if a else (0, 0)
        
        answer = None
        for i, c in enumerate(string):
            addnext(i, i, 0)
            yield answer, B
            
            A, B = B, A
            del B[:]

            for start, j in A:
                if self.states[j] in (None, c) and addnext(start, i+1, j+1):
                    answer = max(answer, (start, i+1), key=key)
            
        yield answer, B
        
    def match(self, string):
        return reduce(lambda answer, s: s[0], self.matcher(string), None)
     
    def source(self):
        for s in self.states:
            yield ('JUMP ' if isinstance(s, tuple) else 'CONSUME ') + str(s)
        yield 'MATCH!'
       
    def __repr__(self):
        return '\n'.join('{:04d}: {}'.format(i, s) for i, s in enumerate(self.source()))
