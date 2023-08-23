from prometheus_client import start_http_server, Summary, Gauge
import os
from transmission_rpc import Client
import time

try:
    transmission_host = os.environ['TRANSMISSION_HOST']
except:
    print('TRANSMISSION_HOST env variable not set')
    exit

try:
    transmission_port = os.environ['TRANSMISSION_PORT']
except:
    print('TRANSMISSION_PORT env variable not set')
    exit

transmission_user = None
transmission_pass = None

try:
    transmission_user = os.environ['TRANSMISSION_USERNAME']
    transmission_pass = os.environ['TRANSMISSION_PASSWORD']
except:
    print('TRANSMISSION_USERNAME and/or TRANSMISSION_PASSWORD env variable not set defaulting to no authentication')

if transmission_user and transmission_pass:
    c = Client(host=transmission_host, port=transmission_port, username=transmission_user, password=transmission_pass)
else:
    c = Client(host=transmission_host, port=transmission_port)

transmission_torrent_countg = Gauge('transmission_torrent_count', 'Total number of torrents')
transmission_active_torrent_countg = Gauge('transmission_active_torrent_count', 'Total number of active torrents')
transmission_paused_torrent_countg = Gauge('transmission_paused_torrent_count', 'Total number of paused torrents')
transmission_download_speedg = Gauge('transmission_download_speed', 'Current total download speed')
transmission_upload_speedg = Gauge('transmission_upload_speed', 'Current total upload speed')
transmission_server_versiong = Gauge('transmission_server_version', 'Version of transmission server', ["version"])
transmission_rpc_versiong = Gauge('transmission_rpc_version', 'Version of transmission RPC API', ["version"])
#transmission_free_spaceg = Gauge('transmission_free_space', 'Free space on default download location')

download_rate_gauge = Gauge("transmission_torrent_download_rate", "Current download rate of a torrent", ["torrent"])
upload_rate_gauge = Gauge("transmission_torrent_upload_rate", "Current upload rate of a torrent", ["torrent"])
file_count_gauge = Gauge("transmission_torrent_file_count", "Number of files in a torrent", ["torrent"])
peers_getting_from_us_gauge = Gauge("transmission_torrent_peers_getting_from_us", "Number of peers that we're sending data to", ["torrent"])
peers_sending_to_us_gauge = Gauge("transmission_torrent_peers_sending_to_us", "Number of peers that are sending data to us.", ["torrent"])
ratio_gauge = Gauge("transmission_torrent_ratio", "Upload/Download ratio", ["torrent"])
available_gauge = Gauge("transmission_torrent_available", "Availability", ["torrent"])

def metrics():
    #Create gauges with session values
    stats = c.session_stats()
    torrents = c.get_torrents()

    transmission_torrent_countg.set(stats.torrent_count)
    transmission_active_torrent_countg.set(stats.active_torrent_count)
    transmission_paused_torrent_countg.set(stats.paused_torrent_count)
    transmission_download_speedg.set(stats.download_speed)
    transmission_upload_speedg.set(stats.upload_speed)
    #transmission_free_spaceg.set(c.free_space())
    transmission_server_versiong.labels(c.server_version).set(1)
    transmission_rpc_versiong.labels(c.rpc_version).set(1)

    #Create gauges per torrent
    for torrent in torrents:
        download_rate_gauge.labels(torrent.name).set(torrent.rate_download)
        upload_rate_gauge.labels(torrent.name).set(torrent.rate_upload)
        file_count_gauge.labels(torrent.name).set(torrent.file_count)
        peers_getting_from_us_gauge.labels(torrent.name).set(torrent.peers_getting_from_us)
        peers_sending_to_us_gauge.labels(torrent.name).set(torrent.peers_sending_to_us)
        ratio_gauge.labels(torrent.name).set(torrent.ratio)
        available_gauge.labels(torrent.name).set(torrent.available)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(5000)
    while True:
        time.sleep(0.1)
        metrics()