import sys
import time
import random
import math


def create_property_based_test(f, regressions=[], time_test=10):
    tstart = time.time()
    i = 0
    while (time.time() - tstart) < time_test:
        if i < len(regressions):
            seed = regressions[i]
        else:
            seed = random.randrange(0, 2**64)
        random.seed(seed)
        try:
            f()
            print("Test", f.__name__, i, "OK")
        except AssertionError as err:
            print("Test", f.__name__, "failed with seed", seed)
            print(err)
            sys.exit(1)
        i += 1


# Example
def get_dist(a, b):
    return math.sqrt(
        ((a[0] - b[0]) ** 2)
        + ((a[1] - b[1]) ** 2)
        + ((a[2] - b[2]) ** 2)
    )


def addition():
    # Exercice:    Tester les additions
    pass


def distance():
    # Exercice:     Tester la distance entre le point A et le point B
    pass


create_property_based_test(addition, time_test=3)
create_property_based_test(
    distance, regressions=[4480881574280375424], time_test=10
)
