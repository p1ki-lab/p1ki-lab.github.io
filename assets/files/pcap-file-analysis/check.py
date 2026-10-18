"""Check sample fields against TShark and reject incomplete input."""
import json
from pathlib import Path
import subprocess
import tempfile

from analyze import analyze


def main():
    result = analyze('demo.pcap')
    assert result['total'] == 8
    assert result['counts'] == {'TCP': 3, 'UDP': 2, 'ICMP': 2, 'OTHER': 1, 'ERROR': 0}
    tshark = Path(r'C:\Program Files\Wireshark\tshark.exe')
    fields = ['frame.number', 'ip.src', 'ip.dst', 'ip.proto', 'tcp.srcport',
              'tcp.dstport', 'udp.srcport', 'udp.dstport', 'tcp.flags', 'icmp.type', 'icmp.code']
    command = [str(tshark), '-n', '-r', 'demo.pcap', '-T', 'fields']
    for field in fields:
        command.extend(['-e', field])
    output = subprocess.run(command, check=True, capture_output=True, text=True).stdout
    Path('tshark_fields.tsv').write_text('\t'.join(fields) + '\n' + output, encoding='utf-8')
    lines = output.splitlines()
    assert len(lines) == result['total']
    for packet, line in zip(result['packets'], lines):
        number, src, dst, proto, ts, td, us, ud, flags, kind, code = line.split('\t')
        assert packet['number'] == int(number)
        assert packet.get('src_ip', '') == src and packet.get('dst_ip', '') == dst
        assert str(packet.get('ip_protocol', '')) == proto
        if packet['protocol'] in ('TCP', 'UDP'):
            assert packet['src_port'] == int(ts or us)
            assert packet['dst_port'] == int(td or ud)
        if packet['protocol'] == 'TCP':
            assert packet['flags'] == int(flags, 16)
        if packet['protocol'] == 'ICMP':
            assert packet['type'] == int(kind) and packet['code'] == int(code)
    with tempfile.TemporaryDirectory(dir='.') as folder:
        path = Path(folder) / 'broken.pcap'
        path.write_bytes(Path('demo.pcap').read_bytes()[:-1])
        try:
            analyze(path)
        except ValueError:
            pass
        else:
            raise AssertionError('Truncated file was accepted')
        path.write_bytes(b'\x0a\x0d\x0d\x0a' + b'\0' * 20)
        try:
            analyze(path)
        except ValueError:
            pass
        else:
            raise AssertionError('PCAPNG marker was accepted')
    print('PASS: sample totals, 8 frames and IP/port/protocol/TCP flag/ICMP fields match TShark')
    print('PASS: truncated PCAP and unsupported PCAPNG rejected')
    print(json.dumps(result['counts']))


if __name__ == '__main__':
    main()
