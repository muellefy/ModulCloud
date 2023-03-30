#!/bin/bash
docker run -d -p 3000:3000 --mount source=modul-cloud,target=/grafana --name grafana-container -e "GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource" grafana/grafana-enterprise
docker run -d -p 9090:9090 -v modul-cloud:/prometheus -v /home/walt/prometheus.yml:/etc/prometheus/prometheus.yml --name prometheus-waltmueller prom/prometheus
