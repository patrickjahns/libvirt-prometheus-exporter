import time
import configargparse
from .collector import LibvirtCollector
from prometheus_client.core import REGISTRY
from prometheus_client import start_http_server


def main():
    p = configargparse.ArgParser(add_config_file_help=False,
                                 auto_env_var_prefix='LIBVIRT_EXPORTER_'
                                 )
    p.add('--uri', required=True,
          help='libvirt connection string (i.e. qemu:///system)')
    p.add('--port',
          help='port where the exporter will listen (default: 9233)',
          default=9233)
    p.add('--host',
          help='address where the exporter will listen (default: 0.0.0.0 )',
          default='0.0.0.0')
    options = p.parse_args()
    REGISTRY.register(LibvirtCollector(options.uri))
    start_http_server(int(options.port), addr=options.host)
    while (True):
        time.sleep(10000)
