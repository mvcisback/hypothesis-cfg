from typing import Mapping, Sequence, Hashable
import random
import funcy as fn
from hypothesis.searchstrategy.strategies import SearchStrategy
from hypothesis.strategies import integers

CFG = Mapping[Hashable, Sequence[Hashable]]

class ContextFreeGrammarStrategy(SearchStrategy):
    def __init__(self, cfg: CFG, start: Hashable, length: int):
        super(ContextFreeGrammarStrategy, self).__init__()
        self.cfg = cfg
        self.start = start
        self.n = length
        self.terminals = set.union(*(
            set.union(*map(set, rhs)) for rhs in cfg.values())) - set(cfg.keys())


    def do_draw(self, data):
        cfg, n = self.cfg, self.n
        @fn.memoize
        def f(variable, n):
            return [sum(fPrime(word, 1, n)) for word in self.cfg[variable]]

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
            index = chooseIndex(f(variable, n))
            if index is None:
                return None
            return gPrime(self.cfg[variable][index], 1, n)

        @fn.memoize
        def fPrime(word, k, n):
            if n == 0:
                return []

            t, symbol = len(word), word[k-1]
            if symbol in self.terminals:
                if k == t:
                    result = ([1] if n == 1 else [0])
                else:
                    result = [sum(fPrime(word, k+1, n-1))]
            else:
                if k == t:
                    result = [sum(f(symbol, n))]
                else:
                    result = [sum(f(symbol, l)) * sum(fPrime(word, k+1, n-l)) for l in range(1, n-t+k+1)]
            return result

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
                    l = chooseIndex(fPrime(word, k, n)) + 1
                    return g(symbol, l) + gPrime(word, k+1, n-l)

        # Check the initial production is the Grammar
        for i in reversed(range(n)):
            result = g(self.start, i)
            if result is not None:
                return result
