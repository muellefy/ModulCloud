# ModulCloud

This repository contains configuration files for Prometheus, Grafana, and related services.

## Running Tests

Install dependencies:

```bash
pip install pytest pyyaml
```

Run the tests with:

```bash
pytest
```


## Docker Update Web Interface

A simple Flask application is provided in `docker_update_webapp.py`. It lists running Docker containers, checks whether their images are up to date and, if not, allows updating them.

Install additional dependencies:

```bash
pip install flask docker
```

Run the web interface with:

```bash
python docker_update_webapp.py
```

The application will start on port 5000.
