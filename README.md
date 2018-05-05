Early version of implementation of [Hypothesis] strategy for
Context Free Grammars.

```python
from hypothesis import given
from hypothesis_cfg import ContextFreeGrammarStrategy

# Production rules
GRAMMAR = {
    'P': (('P', 'P'), ('A', 'R')),
    'A': (('L', 'P'), ('(',)),
    'L': (('(',),),
    'R': ((')',),),
}

@given(ContextFreeGrammarStrategy(GRAMMAR, max_length=20, start='P'))
def test_foo(foo):
    assert len(foo) <= 20
```

Currently no guarantees on the distribution.
TODO: cite relevant works.

[Hypothesis]: http://hypothesis.works/
