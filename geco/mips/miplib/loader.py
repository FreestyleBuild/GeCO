import tempfile
import requests
import pyscipopt as scip
import os
import pandas as pd

INSTANCES_DIR = tempfile.gettempdir() + "/geco/miplib/instances/"
MIPLIB_INSTANCE_URL = "https://miplib.zib.de/WebData/instances/"


def load_instances(filters={}, instances_csv=None):
    if instances_csv:
        df = pd.read_csv(instances_csv, header=0)
    else:
        raise NotImplemented("Dynamic loading of instances csv is not implemented yet.")

    for key, value in filters.items():
        df = df[df[key] == value]

    for instance in df["Instance  Ins."]:
        full_instance_name = instance + ".mps.gz"
        yield load_instance(full_instance_name)


def load_instance(instance_name):
    if not _instance_cached(instance_name):
        _download_instance(instance_name)
    problem_path = INSTANCES_DIR + instance_name
    model = scip.Model()
    model.readProblem(problem_path)
    return model


def _download_instance(instance_name):
    if not os.path.exists(INSTANCES_DIR):
        os.makedirs(INSTANCES_DIR)
    path = _instance_path(instance_name)
    content = requests.get(MIPLIB_INSTANCE_URL + instance_name).content
    with open(path, "wb") as f:
        f.write(content)


def _instance_cached(instance_name):
    return os.path.exists(_instance_path(instance_name))


def _instance_path(instance_name):
    return INSTANCES_DIR + instance_name


def easy_instances(instances_csv):
    return load_instances(filters={"Status  Sta.": "easy"}, instances_csv=instances_csv)


def hard_instances(instances_csv):
    return load_instances(filters={"Status  Sta.": "hard"}, instances_csv=instances_csv)


def open_instances(instances_csv):
    return load_instances(filters={"Status  Sta.": "open"}, instances_csv=instances_csv)
