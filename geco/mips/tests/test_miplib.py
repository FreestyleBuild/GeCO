import pyscipopt as scip
from geco.mips.miplib.loader import *
import pytest


def test_load_instance():
    instance = load_instance("30n20b8.mps.gz")
    assert isinstance(instance, scip.Model)


@pytest.mark.skip(reason="Resolving this requires loading the csv dynamically")
def test_load_instances():
    instances = [i for i in load_instances({"Status  Sta.": "hard"})]
    assert len(instances) == 142
    for i in instances:
        assert isinstance(i, scip.Model)
