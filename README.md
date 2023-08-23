Exports metrics from transmission torrent client to be scraped by prometheus.

![Grafana dashboard preview](https://i.imgur.com/iQt0pzv.png)
## Docker
Clone the repository:
```bash
git clone https://github.com/t3hl34d3r/python-transmission-exporter.git && cd python-transmission-exporter
```
Build the image:
```bash
docker build -t python-transmission-exporter .
```
Run the image:
```bash
docker run --rm \
-p 5000:5000 \
-e TRANSMISSION_HOST=<your transmission host> \
-e TRANSMISSION_PORT=<your transmission port (eg. 9091)> \
-e TRANSMISSION_USERNAME=<your transmission username, optional> \
-e TRANSMISSION_PASSWORD=<your transmission password, optional> \
--name=python-transmission-exporter \
python-transmission-exporter
```

Metrics should now be available on http://localhost:5000/metrics
## Prometheus config
Add this example config to your prometheus.yml to scrape metrics with prometheus:
```yaml
- job_name: python-transmission
  metrics_path: /metrics
  static_configs:
  - targets:
    - python-transmission-exporter:5000
```

## Metrics
Currently the following metrics are exported
### Global metrics

| Metric | Description |
| ----------- | ----------- |
| transmission_torrent_count | Total number of torrents |
|transmission_active_torrent_count|Total number of active torrents|
|transmission_paused_torrent_count|Total number of paused torrents|
|transmission_download_speed|Current total download speed|
|transmission_upload_speed|Current total upload speed|
|transmission_server_version|Version of transmission server|
|transmission_rpc_version|Version of transmission RPC API|

### Per torrent metrics

| Metric | Description |
| ----------- | ----------- |
|transmission_torrent_download_rate|Current download rate of a torrent|
|transmission_torrent_upload_rate|Current upload rate of a torrent|
|transmission_torrent_file_count|Number of files in a torrent|
|transmission_torrent_peers_getting_from_us|Number of peers that we're sending data to|
|transmission_torrent_peers_sending_to_us|Number of peers that are sending data to us|
|transmission_torrent_ratio|Upload/Download ratio|
|transmission_torrent_available|Availability|

## Grafana
You can use the the included dashboard.json to import an example grafana dashboard. This dashboard has a constant variable "job" defaulting to "python-transmission". Change this variable if you added this exporter with a different name in prometheus. 