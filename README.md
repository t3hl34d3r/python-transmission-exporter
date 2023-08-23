Exports metrics from transmission torrent client to be scraped by prometheus.

## Docker
Clone the repository:
```bash
git clone https://github.com/t3hl34d34/python-transmission-exporter.git
```
Build the image:
```bash
docker build -t python-transmission-exporter .
```
Run the image:
```bash
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

