from libvirt_exporter.collector import parse_net, parse_blk


class TestLibvirtCollector:

    def test_net_parser_will_return_empty_array(self):
        data = {}
        assert len(parse_net(data)) == 0, "a empty data set should not result in a set"

    def test_net_parser_will_return_single_array(self):
        data = {
            'net.count': 1,
            'net.0.name': 'test',
            'net.0.rx.bytes': 1,
            'net.0.rx.pkts': 2,
            'net.0.rx.errs': 3,
            'net.0.rx.drop': 4,
            'net.0.tx.bytes': 5,
            'net.0.tx.errs': 6,
            'net.0.tx.pkts': 7,
            'net.0.tx.drop': 8,
        }
        parsed_data = parse_net(data)
        assert len(parsed_data) == 1, "net parser should return a single result"
        result = parsed_data.pop()
        assert result['name'] == 'test'
        assert result['rx_bytes'] == 1
        assert result['rx_pkts'] == 2
        assert result['rx_errors'] == 3
        assert result['rx_drops'] == 4
        assert result['tx_bytes'] == 5
        assert result['tx_pkts'] == 7
        assert result['tx_errors'] == 6
        assert result['tx_drops'] == 8

    def test_net_parser_will_return_more_than_one_array(self):
        data = {
            'net.count': 2,
            'net.0.name': 'test',
            'net.0.rx.bytes': 1,
            'net.0.rx.pkts': 2,
            'net.0.rx.errs': 3,
            'net.0.rx.drop': 4,
            'net.0.tx.bytes': 5,
            'net.0.tx.errs': 6,
            'net.0.tx.pkts': 7,
            'net.0.tx.drop': 8,
            'net.1.name': 'test2',
            'net.1.rx.bytes': 11,
            'net.1.rx.pkts': 12,
            'net.1.rx.errs': 13,
            'net.1.rx.drop': 14,
            'net.1.tx.bytes': 15,
            'net.1.tx.errs': 16,
            'net.1.tx.pkts': 17,
            'net.1.tx.drop': 18,
        }

        parsed_data = parse_net(data)
        assert len(parsed_data) == 2, "net parser should return two objects"
        result = parsed_data.pop()
        assert result['name'] == 'test2'
        assert result['rx_bytes'] == 11
        assert result['rx_pkts'] == 12
        assert result['rx_errors'] == 13
        assert result['rx_drops'] == 14
        assert result['tx_bytes'] == 15
        assert result['tx_pkts'] == 17
        assert result['tx_errors'] == 16
        assert result['tx_drops'] == 18

        result = parsed_data.pop()
        assert result['name'] == 'test'
        assert result['rx_bytes'] == 1
        assert result['rx_pkts'] == 2
        assert result['rx_errors'] == 3
        assert result['rx_drops'] == 4
        assert result['tx_bytes'] == 5
        assert result['tx_pkts'] == 7
        assert result['tx_errors'] == 6
        assert result['tx_drops'] == 8

    def test_blk_parser_will_return_emby_array(self):
        data = {}
        assert len(parse_blk(data)) == 0
        data = {'state.state': '5'}
        assert len(parse_blk(data)) == 0

    def test_blk_parser_will_return_single_array(self):
        data = {
            'state.state': 1,
            'block.count': '1',
            'block.0.name': 'test',
            'block.0.path': 'testpath',
            'block.0.allocation': 0,
            'block.0.capacity': 1,
            'block.0.physical': 2,
            'block.0.rd.reqs': 3,
            'block.0.rd.bytes': 4,
            'block.0.rd.times': 5,
            'block.0.wr.reqs': 6,
            'block.0.wr.bytes': 7,
            'block.0.wr.times': 8,
            'block.0.fl.reqs': 9,
            'block.0.fl.times': 10,
        }
        parsed = parse_blk(data)
        assert len(parsed) == 1
        result = parsed.pop()
        assert result['name'] == 'test'
        assert result['path'] == 'testpath'
        assert result['allocation'] == 0
        assert result['capacity'] == 1
        assert result['physical'] == 2
        assert result['read_requests'] == 3
        assert result['read_bytes'] == 4
        assert result['read_seconds'] == 5
        assert result['write_requests'] == 6
        assert result['write_bytes'] == 7
        assert result['write_seconds'] == 8
        assert result['flush_requests'] == 9
        assert result['flush_seconds'] == 10

    def test_blk_parser_will_return_more_than_one_array(self):
        data = {
            'state.state': 1,
            'block.count': '2',
            'block.0.name': 'test',
            'block.0.path': 'testpath',
            'block.0.allocation': 0,
            'block.0.capacity': 1,
            'block.0.physical': 2,
            'block.0.rd.reqs': 3,
            'block.0.rd.bytes': 4,
            'block.0.rd.times': 5,
            'block.0.wr.reqs': 6,
            'block.0.wr.bytes': 7,
            'block.0.wr.times': 8,
            'block.0.fl.reqs': 9,
            'block.0.fl.times': 10,
            'block.1.name': 'test2',
            'block.1.path': 'testpath2',
            'block.1.allocation': 0,
            'block.1.capacity': 1,
            'block.1.physical': 2,
            'block.1.rd.reqs': 3,
            'block.1.rd.bytes': 4,
            'block.1.rd.times': 5,
            'block.1.wr.reqs': 6,
            'block.1.wr.bytes': 7,
            'block.1.wr.times': 8,
            'block.1.fl.reqs': 9,
            'block.1.fl.times': 10,
        }
        parsed = parse_blk(data)
        assert len(parsed) == 2
        result = parsed.pop()
        assert result['name'] == 'test2'
        assert result['path'] == 'testpath2'
        assert result['allocation'] == 0
        assert result['capacity'] == 1
        assert result['physical'] == 2
        assert result['read_requests'] == 3
        assert result['read_bytes'] == 4
        assert result['read_seconds'] == 5
        assert result['write_requests'] == 6
        assert result['write_bytes'] == 7
        assert result['write_seconds'] == 8
        assert result['flush_requests'] == 9
        assert result['flush_seconds'] == 10

        result = parsed.pop()
        assert result['name'] == 'test'
        assert result['path'] == 'testpath'
        assert result['allocation'] == 0
        assert result['capacity'] == 1
        assert result['physical'] == 2
        assert result['read_requests'] == 3
        assert result['read_bytes'] == 4
        assert result['read_seconds'] == 5
        assert result['write_requests'] == 6
        assert result['write_bytes'] == 7
        assert result['write_seconds'] == 8
        assert result['flush_requests'] == 9
        assert result['flush_seconds'] == 10
