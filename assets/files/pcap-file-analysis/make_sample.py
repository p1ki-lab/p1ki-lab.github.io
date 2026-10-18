"""Generate synthetic traffic locally. No packets are transmitted."""
import socket
import dpkt


def frame(src, dst, protocol, payload):
    ip = dpkt.ip.IP(src=socket.inet_aton(src), dst=socket.inet_aton(dst), p=protocol, ttl=64, data=payload)
    ip.len = len(ip)
    src_mac, dst_mac = ('020000000001', '020000000002') if src == '192.0.2.10' else ('020000000002', '020000000001')
    return bytes(dpkt.ethernet.Ethernet(src=bytes.fromhex(src_mac),
                                      dst=bytes.fromhex(dst_mac), type=0x0800, data=ip))


def main():
    a, b = '192.0.2.10', '192.0.2.20'
    packets = []
    for src, dst, sport, dport, flags, seq, ack in [
        (a, b, 53000, 443, 2, 100, 0),
        (b, a, 443, 53000, 18, 500, 101),
        (a, b, 53000, 443, 16, 101, 501)]:
        packets.append(frame(src, dst, 6, dpkt.tcp.TCP(sport=sport, dport=dport, flags=flags, seq=seq, ack=ack)))
    for src, dst, sport, dport in [(a, b, 54000, 9999), (b, a, 9999, 54000)]:
        udp = dpkt.udp.UDP(sport=sport, dport=dport, data=b'hello')
        udp.ulen = len(udp)
        packets.append(frame(src, dst, 17, udp))
    for src, dst, kind in [(a, b, 8), (b, a, 0)]:
        packets.append(frame(src, dst, 1, dpkt.icmp.ICMP(type=kind, data=dpkt.icmp.ICMP.Echo(id=1, seq=1, data=b'hello'))))
    arp = dpkt.arp.ARP(sha=bytes.fromhex('020000000001'), spa=socket.inet_aton(a),
                       tha=b'\x00' * 6, tpa=socket.inet_aton(b))
    packets.append(bytes(dpkt.ethernet.Ethernet(src=arp.sha, dst=b'\xff' * 6, type=0x0806, data=arp)))
    with open('demo.pcap', 'wb') as stream:
        writer = dpkt.pcap.Writer(stream)
        for index, packet in enumerate(packets):
            writer.writepkt(packet, ts=1700000000 + index / 10)
    print('Created demo.pcap: 8 synthetic frames; no live traffic sent')


if __name__ == '__main__':
    main()
