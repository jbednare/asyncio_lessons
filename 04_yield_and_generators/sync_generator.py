#!/usr/bin/env python3

# Plain `yield`: defines a generator function. Calling the function does
# NOT run any code -- it returns a generator object. The body advances
# one chunk at a time, only when the caller asks for the next value via
# `next()` or by iterating with `for`. Generators are LAZY.

import sys


def counter(n: int):
    print(f"  [body] counter({n}) entered, about to loop")
    for i in range(n):
        print(f"  [body] about to yield {i}")
        yield i
        print(f"  [body] resumed after yielding {i}")
    print(f"  [body] counter({n}) returning, raises StopIteration")


def main() -> int:
    print("--- create the generator (nothing runs yet) ---")
    gen = counter(3)
    print(f"  gen = {gen!r}")

    print("\n--- pull values one at a time with next() ---")
    print(f"  next(gen) -> {next(gen)}")
    print(f"  next(gen) -> {next(gen)}")
    print(f"  next(gen) -> {next(gen)}")
    try:
        next(gen)
    except StopIteration:
        print("  next(gen) -> StopIteration")

    print("\n--- or drive it with a for loop ---")
    for value in counter(3):
        print(f"  for got {value}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
