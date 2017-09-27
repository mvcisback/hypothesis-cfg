from typing import Mapping, Sequence
import random
import funcy as fn

CFG = Mapping[str, Sequence[str]]

def sample(cfg: CFG, start: str, n: int) -> str:
    """Uniformly sample from derivation trees of strings of length n.

    - cfg : Mapping from non-terminal to possible expansions, e.g., A ::= AA | b.
            Also known as the production rules.
    - start : First rule to apply.
    - n : Length of sample producted.
    """
    variables = set(cfg.keys())
    terminals = set.union(*(set(rhs) for rhs in cfg.values())) - variables

    @fn.memoize
    def f(variable, n):
        return [sum(fPrime(word, 1, n)) for word in cfg[variable]]

    def chooseIndex(l):
        total = sum(l)
        if total <= 0:
            return None
        r = random.randint(1, total)
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
        return gPrime(cfg[variable][index], 1, n)

    @fn.memoize
    def fPrime(word, k, n):
        if n == 0:
            return []

        t, symbol = len(word), word[k-1]
        if symbol in terminals:
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
        if symbol in terminals:
            l, prefix = None, [symbol]
        elif k == t:
            l, prefix = 1, g(symbol, n)
        else:
            l = chooseIndex(fPrime(word, k, n)) + 1
            prefix = g(symbol, l)
        return prefix + ([] if k == t else gPrime(word, k+1, n-l))

    return ''.join(g(start, n))


def main():
    cfg = {
        'P': ('PP', 'AR'),
        'A': ('LP', '('),
        'L': ('(',),
        'R': (')',),        
    }
    # sample a word of length n=20
    print(sample(cfg, n=20, start='P'))


if __name__ == '__main__':
    main()
