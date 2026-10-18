"""Offline classic-PCAP analyzer: Ethernet II / unfragmented IPv4."""
import argparse
import collections
import json
import socket
import struct
import sys

import dpkt


def read_packets(path):
    with open(path, 'rb') as stream:
        header = stream.read(24)
        formats = {b'\xd4\xc3\xb2\xa1': ('<', 1e6),
                   b'\xa1\xb2\xc3\xd4': ('>', 1e6),
                   b'\x4d\x3c\xb2\xa1': ('<', 1e9),
                   b'\xa1\xb2\x3c\x4d': ('>', 1e9)}
        if len(header) != 24 or header[:4] not in formats:
            raise ValueError('Expected classic PCAP; PCAPNG is unsupported')
        endian, precision = formats[header[:4]]
        major, minor, _, _, snaplen, linktype = struct.unpack(endian + 'HHiIII', header[4:])
        if (major, minor) != (2, 4) or linktype != 1:
            raise ValueError('Only PCAP 2.4 with Ethernet linktype=1 is supported')
        while True:
            record = stream.read(16)
            if not record:
                return
            if len(record) != 16:
                raise ValueError('Truncated PCAP record header')
            seconds, fraction, captured, original = struct.unpack(endian + 'IIII', record)
            if captured > original or captured > snaplen or captured > 16 * 1024 * 1024:
                raise ValueError('Invalid or unsupported packet length')
            data = stream.read(captured)
            if len(data) != captured:
                raise ValueError('Truncated PCAP packet data')
            yield seconds + fraction / precision, data, captured < original


def mac(raw):
    return ':'.join(f'{byte:02x}' for byte in raw)


def parse_packet(timestamp, data, truncated):
    row = {'time': timestamp, 'length': len(data)}
    if truncated:
        raise ValueError('Capture-truncated packet: full header analysis not attempted')
    if len(data) < 14:
        raise ValueError('Incomplete Ethernet header')
    eth = dpkt.ethernet.Ethernet(data)
    row.update(src_mac=mac(eth.src), dst_mac=mac(eth.dst), ethertype=f'0x{eth.type:04x}')
    if eth.type != dpkt.ethernet.ETH_TYPE_IP:
        return dict(row, protocol='OTHER', note='Unsupported EtherType')
    ip = eth.data
    if not isinstance(ip, dpkt.ip.IP) or ip.v != 4:
        raise ValueError('Invalid IPv4 header')
    if ip.hl < 5 or ip.len < ip.hl * 4 or ip.len > len(data) - 14:
        raise ValueError('Invalid IPv4 header/total length')
    row.update(src_ip=socket.inet_ntoa(ip.src), dst_ip=socket.inet_ntoa(ip.dst),
               ip_protocol=ip.p, ttl=ip.ttl)
    if ip.mf or ip.offset:
        return dict(row, protocol='OTHER', note='IPv4 fragmentation unsupported')
    transport = ip.data
    if ip.p == 6:
        if not isinstance(transport, dpkt.tcp.TCP) or transport.off < 5 or transport.off * 4 > ip.len - ip.hl * 4:
            raise ValueError('Invalid TCP header')
        row.update(protocol='TCP', src_port=transport.sport, dst_port=transport.dport,
                   flags=transport.flags, seq=transport.seq, ack=transport.ack)
    elif ip.p == 17:
        if not isinstance(transport, dpkt.udp.UDP) or transport.ulen < 8 or transport.ulen != ip.len - ip.hl * 4:
            raise ValueError('Invalid UDP length/header')
        row.update(protocol='UDP', src_port=transport.sport, dst_port=transport.dport)
    elif ip.p == 1:
        if not isinstance(transport, dpkt.icmp.ICMP):
            raise ValueError('Invalid ICMP header')
        row.update(protocol='ICMP', type=transport.type, code=transport.code)
    else:
        row.update(protocol='OTHER', note='Unsupported IPv4 protocol')
    return row


def analyze(path):
    packets = []
    counts = collections.Counter(dict.fromkeys(['TCP', 'UDP', 'ICMP', 'OTHER', 'ERROR'], 0))
    for number, (timestamp, data, truncated) in enumerate(read_packets(path), 1):
        try:
            row = parse_packet(timestamp, data, truncated)
        except (ValueError, dpkt.UnpackError, struct.error) as error:
            row = {'time': timestamp, 'length': len(data), 'protocol': 'ERROR', 'note': str(error)}
        row['number'] = number
        packets.append(row)
        counts[row['protocol']] += 1
    return {'packets': packets, 'counts': dict(counts), 'total': len(packets)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pcap')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        result = analyze(args.pcap)
    except (OSError, ValueError) as error:
        print(f'FILE ERROR: {error}', file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for row in result['packets']:
            print(json.dumps(row))
        print('TOTAL=' + str(result['total']), ' '.join(f'{key}={value}' for key, value in result['counts'].items()))
    return 2 if result['counts']['ERROR'] else 0


if __name__ == '__main__':
    sys.exit(main())
