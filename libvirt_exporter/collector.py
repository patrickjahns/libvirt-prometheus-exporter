import libvirt
from prometheus_client.core import GaugeMetricFamily


def parse_net(stat):
    if 'net.count' not in stat:
        return []
    net_stat = []
    for i in range(int(stat['net.count'])):
        current_stat = {
            'name': stat['net.' + str(i) + '.name'],
            'rx_bytes': stat['net.' + str(i) + '.rx.bytes'],
            'rx_pkts': stat['net.' + str(i) + '.rx.pkts'],
            'rx_errors': stat['net.' + str(i) + '.rx.errs'],
            'rx_drops': stat['net.' + str(i) + '.rx.drop'],
            'tx_bytes': stat['net.' + str(i) + '.tx.bytes'],
            'tx_pkts': stat['net.' + str(i) + '.tx.pkts'],
            'tx_errors': stat['net.' + str(i) + '.tx.errs'],
            'tx_drops': stat['net.' + str(i) + '.tx.drop']
        }
        net_stat.append(current_stat)
    return net_stat


def parse_blk(stat):
    if 'block.count' not in stat or stat['state.state'] != 1:
        return []
    blk_stat = []
    for i in range(int(stat['block.count'])):
        current_stat = {
            'name': stat['block.' + str(i) + '.name'],
            'path': stat['block.' + str(i) + '.path'],
            'allocation': stat['block.' + str(i) + '.allocation'],
            'capacity': stat['block.' + str(i) + '.capacity'],
            'physical': stat['block.' + str(i) + '.physical'],
            'read_requests': stat['block.' + str(i) + '.rd.reqs'],
            'read_bytes': stat['block.' + str(i) + '.rd.bytes'],
            'read_seconds': stat['block.' + str(i) + '.rd.times'],
            'write_requests': stat['block.' + str(i) + '.wr.reqs'],
            'write_bytes': stat['block.' + str(i) + '.wr.bytes'],
            'write_seconds': stat['block.' + str(i) + '.wr.times'],
            'flush_requests': stat['block.' + str(i) + '.fl.reqs'],
            'flush_seconds': stat['block.' + str(i) + '.fl.times']
        }
        blk_stat.append(current_stat)
    return blk_stat


class LibvirtCollector(object):

    def __init__(self, uri):
        self.uri = uri
        self.conn = libvirt.openReadOnly(uri)

    def collect(self):
        stats = self.conn.getAllDomainStats()
        state = GaugeMetricFamily(
            'lvirt_domain_info_state',
            'Current state for the domain.',
            labels=['name', 'id'])
        vcpus = GaugeMetricFamily(
            'lvirt_domain_info_vcpus',
            'Number of virtual CPUs for the domain.',
            labels=['name', 'id'])
        cpu_time = GaugeMetricFamily(
            'lvirt_domain_info_cpu_time_total',
            'Amount of CPU time used by the domain, in seconds.',
            labels=['name', 'id'])
        mem_max = GaugeMetricFamily(
            'lvirt_domain_info_maximum_memory_bytes',
            'Maximum allowed memory of the domain, in bytes.',
            labels=['name', 'id'])
        mem_curr = GaugeMetricFamily(
            'lvirt_domain_info_memory_usage_bytes',
            'Memory usage of the domain, in bytes.',
            labels=['name', 'id'])

        net_receive_bytes = GaugeMetricFamily(
            'lvirt_domain_interface_stats_receive_bytes_total',
            'Number of bytes received on a network interface, in bytes.',
            labels=['name', 'id', 'interface'])
        net_receive_packets = GaugeMetricFamily(
            'lvirt_domain_interface_stats_receive_bytes_total',
            'Number of packets received on a network interface.',
            labels=['name', 'id', 'interface'])
        net_receive_errors = GaugeMetricFamily(
            'lvirt_domain_interface_stats_receive_errors_total',
            'Number of packet receive errors on a network interface.',
            labels=['name', 'id', 'interface'])
        net_receive_drops = GaugeMetricFamily(
            'lvirt_domain_interface_stats_receive_drops_total',
            'Number of packet receive drops on a network interface.',
            labels=['name', 'id', 'interface'])
        net_transmit_bytes = GaugeMetricFamily(
            'lvirt_domain_interface_stats_transmit_bytes_total',
            'Number of bytes transmitted on a network interface, in bytes.',
            labels=['name', 'id', 'interface'])
        net_transmit_packets = GaugeMetricFamily(
            'lvirt_domain_interface_stats_transmit_bytes_total',
            'Number of packets transmitted on a network interface..',
            labels=['name', 'id', 'interface'])
        net_transmit_errors = GaugeMetricFamily(
            'lvirt_domain_interface_stats_transmit_errors_total',
            'Number of packet transmit errors on a network interface.',
            labels=['name', 'id', 'interface'])
        net_transmit_drops = GaugeMetricFamily(
            'lvirt_domain_interface_stats_transmit_drops_total',
            'Number of packet transmit drops on a network interface.',
            labels=['name', 'id', 'interface'])

        blk_read_request = GaugeMetricFamily(
            'lvirt_domain_block_stats_read_requests_total',
            'Number of read requests from a block device.',
            labels=['name', 'id', 'device', 'path'])
        blk_read_bytes = GaugeMetricFamily(
            'lvirt_domain_block_stats_read_bytes_total',
            'Number of bytes read from a block device, in bytes.',
            labels=['name', 'id', 'device', 'path'])
        blk_read_seconds = GaugeMetricFamily(
            'lvirt_domain_block_stats_read_seconds_total',
            'Amount of time spent reading from a block device, in seconds.',
            labels=['name', 'id', 'device', 'path'])
        blk_write_request = GaugeMetricFamily(
            'lvirt_domain_block_stats_write_requests_total',
            'Number of write requests from a block device.',
            labels=['name', 'id', 'device', 'path'])
        blk_write_bytes = GaugeMetricFamily(
            'lvirt_domain_block_stats_write_bytes_total',
            'Number of bytes written from a block device, in bytes.',
            labels=['name', 'id', 'device', 'path'])
        blk_write_seconds = GaugeMetricFamily(
            'lvirt_domain_block_stats_write_seconds_total',
            'Amount of time spent writing from a block device, in seconds.',
            labels=['name', 'id', 'device', 'path'])
        blk_flush_requests = GaugeMetricFamily(
            'lvirt_domain_block_stats_flush_requests_total',
            'Number of flush requests from a block device.',
            labels=['name', 'id', 'device', 'path'])
        blk_flush_seconds = GaugeMetricFamily(
            'lvirt_domain_block_stats_flush_seconds_total',
            'Amount of time spent flushing of a block device, in seconds.',
            labels=['name', 'id', 'device', 'path'])

        for domain, stat in stats:
            base_label = [domain.name(), domain.UUIDString()]
            state.add_metric(base_label, stat['state.state'])
            vcpus.add_metric(base_label, stat['vcpu.current'])
            mem_max.add_metric(base_label, stat['balloon.maximum'])

            if stat['state.state'] == 1:
                cpu_time.add_metric(base_label, stat['cpu.time'])
                mem_curr.add_metric(base_label, stat['balloon.current'])

            for net in parse_net(stat):
                net_label = [domain.name(), domain.UUIDString(), net['name']]
                net_receive_bytes.add_metric(net_label, net['rx_bytes'])
                net_receive_packets.add_metric(net_label, net['rx_pkts'])
                net_receive_drops.add_metric(net_label, net['rx_drops'])
                net_receive_errors.add_metric(net_label, net['rx_errors'])
                net_transmit_bytes.add_metric(net_label, net['tx_bytes'])
                net_transmit_packets.add_metric(net_label, net['tx_pkts'])
                net_transmit_errors.add_metric(net_label, net['tx_errors'])
                net_transmit_drops.add_metric(net_label, net['tx_drops'])

            for blk in parse_blk(stat):
                blk_label = [domain.name(), domain.UUIDString(),
                             blk['name'], blk['path']]
                blk_read_bytes.add_metric(blk_label, blk['read_bytes'])
                blk_read_request.add_metric(blk_label, blk['read_requests'])
                blk_read_seconds.add_metric(blk_label, blk['read_seconds'])
                blk_write_bytes.add_metric(blk_label, blk['write_bytes'])
                blk_write_request.add_metric(blk_label, blk['write_requests'])
                blk_write_seconds.add_metric(blk_label, blk['write_seconds'])
                blk_flush_requests.add_metric(blk_label, blk['flush_requests'])
                blk_flush_seconds.add_metric(blk_label, blk['flush_seconds'])

        yield state
        yield vcpus
        yield cpu_time
        yield mem_max
        yield mem_curr
        yield net_receive_bytes
        yield net_receive_packets
        yield net_receive_errors
        yield net_receive_drops
        yield net_transmit_bytes
        yield net_transmit_packets
        yield net_transmit_errors
        yield net_transmit_drops
        yield blk_read_request
        yield blk_read_bytes
        yield blk_read_seconds
        yield blk_write_request
        yield blk_write_seconds
        yield blk_write_bytes
        yield blk_flush_requests
        yield blk_flush_seconds
