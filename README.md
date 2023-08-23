Exports metrics from transmission torrent client to be scraped by prometheus.

## Docker
```bash
git clone https://github.com/t3hl34d34/python-transmission-exporter.git
docker build -t python-transmission-exporter .
docker run --rm -p 5000:5000 -e TRANSMISSION_HOST=<your transmission host> -e TRANSMISSION_PORT=<your transmission port (eg. 9091)> --name=python-transmission-exporter python-transmission-exporter
```

## Prometheus config
```
- job_name: python-transmission
  metrics_path: /metrics
  static_configs:
  - targets:
    - python-transmission-exporter:5000
```

