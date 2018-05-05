import funcy as fn
from typing import Mapping, Sequence, Hashable

from hypothesis.searchstrategy.strategies import SearchStrategy
from hypothesis.strategies import integers

CFG = Mapping[Hashable, Sequence[Hashable]]

class ContextFreeGrammarStrategy(SearchStrategy):
    def __init__(self, cfg: CFG, start: Hashable, max_length: int):
        super(ContextFreeGrammarStrategy, self).__init__()
        self.cfg = cfg
        self.start = start
        self.n = max_length
        self.terminals = set.union(*(
            set.union(*map(set, rhs)) for rhs in cfg.values())) - set(cfg.keys())

    def count(self, n):
        return sum(self.f(self.start, n))

    @fn.memoize
    def f(self, variable, n):
        return [sum(self.fPrime(word, 1, n)) for word in self.cfg[variable]]

    @fn.memoize
    def fPrime(self, word, k, n):
        if n == 0:
            return []

        t, symbol = len(word), word[k-1]
        if symbol in self.terminals:
            if k == t:
                result = ([1] if n == 1 else [0])
            else:
                result = [sum(self.fPrime(word, k+1, n-1))]
        else:
            if k == t:
                result = [sum(self.f(symbol, n))]
            else:
                result = [sum(self.f(symbol, l)) * sum(
                    self.fPrime(word, k+1, n-l)) for l in range(1, n-t+k+1)]
        return result

    def do_draw(self, data):
        def chooseIndex(l):
            total = sum(l)
            if total <= 0:
                return None

            r = data.draw(integers(1, total))
            for (index, num) in enumerate(l):
                if r <= num:
                    return index
                else:
                    r -= num
            return None

        def g(variable, n):
            index = chooseIndex(self.f(variable, n))
            if index is None:
                return None
            return gPrime(self.cfg[variable][index], 1, n)

        def gPrime(word, k, n):
            t, symbol = len(word), word[k-1]
            if symbol in self.terminals:
                if k == t:
                    return [symbol]
                else:
                    return [symbol] + gPrime(word, k+1, n-1)
            else:
                if k == t:
                    return g(symbol, n)
                else:
                    l = chooseIndex(self.fPrime(word, k, n)) + 1
                    return g(symbol, l) + gPrime(word, k+1, n-l)

        # Pick length of element weighted by #elements per length
        l = chooseIndex([self.count(i) for i in range(self.n + 1)])
        return g(self.start, l)
