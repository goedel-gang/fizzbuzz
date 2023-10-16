#s!/usr/bin/env python3

"""
FizzBuzz program - for some set of words and integers, replace a number with
that word if the index it appears at is a multiple of that integer.

Written in such a way that there is some constant amount of calculation
involving string concatenation and multiplication and the like at the start, and
from that point on you just have a working (infinite, lazy) iterable.

This probably introduces more overhead than it saves but I think it's a nice
idea.
"""

from argparse import _AppendAction, ArgumentParser
from itertools import islice, count, combinations, chain
from functools import reduce
from math import gcd

class FizzBuzzAction(_AppendAction):
    """
    Argparse action to accumulate (int, str) tuples
    """
    def __call__(self, parser, args_, values, option_string=None):
        n, word = values
        super().__call__(parser, args_, (int(n), word), option_string)

def get_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-n', type=int, default=100,
                        help="number of things to print")
    parser.add_argument('--fb', nargs=2, action=FizzBuzzAction, default=[],
                        help='Integer followed by word',
                        metavar=('N', 'WORD'))
    return parser.parse_args()

def replace_every(seq, replacement, n):
    """
    Lazily replace every `n`th item in `seq` with `replacement`
    """
    while True:
        yield from islice(seq, n - 1)
        yield replacement
        next(seq)

def intersect(term_a, term_b):
    """
    Find how two fizzbuzz terms combine -eg
    (3, "Fizz") combines with (5, "Buzz") to make (15, "FizzBuzz")
    """
    # split each into their `n` and `word` components
    a_n, a_w = term_a
    b_n, b_w = term_b
    return a_n * b_n // gcd(a_n, b_n), "{}{}".format(a_w, b_w)

def fizzbuzz(terms):
    """
    Generate a lazy FizzBuzz style iterable. `terms` is a list of (int, str)
    tuples representing FizzBuzz rules, eg [(3, "Fizz"), (5, "Buzz")].
    """
    seq = map(str, count(1))
    for subset in chain.from_iterable(combinations(terms, i)
                                      for i in range(1, len(terms) + 1)):
        product, word = reduce(intersect, subset, (1, ""))
        seq = replace_every(seq, word, product)
    return seq

if __name__ == "__main__":
    args = get_args()
    fb_seq = fizzbuzz(args.fb)
    for line in islice(fb_seq, 0, args.n):
        print(line)
