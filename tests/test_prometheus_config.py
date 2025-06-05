import yaml
import os


def test_prometheus_yaml_loads():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prometheus.yml')
    with open(config_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    assert data is not None

