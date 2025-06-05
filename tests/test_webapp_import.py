import importlib

def test_webapp_imports():
    assert importlib.import_module('docker_update_webapp') is not None
