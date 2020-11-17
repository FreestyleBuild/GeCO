import itertools

import pytest

from geco.mips.set_packing import *


def test_yang():
    m = 100
    model = yang_instance(m)
    assert model.getNVars() == 5 * m
    assert model.getNConss() == m
    assert model.getObjectiveSense() == "maximize"


@pytest.mark.parametrize(
    "m,seed1,seed2",
    itertools.product([10, 100, 1000], [0, 1, 1337, 53115], [0, 1, 1337, 53115]),
)
def test_yang_seeding(m, seed1, seed2):
    params1 = yang_parameters(m, seed=seed1)
    params2 = yang_parameters(m, seed=seed2)
    same_seeds_produce_same_params = seed1 == seed2 and params1 == params2
    different_seeds_produce_different_params = seed1 != seed2 and params1 != params2
    assert same_seeds_produce_same_params or different_seeds_produce_different_params
