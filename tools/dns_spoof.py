#!/usr/bin/env python3
"""Standalone DNS spoofer for PS5.
Spoofs manuals.playstation.net -> your PC IP.
All other domains get NXDOMAIN (blocks PSN and updates).

Usage:
    python dns_spoof.py --ip 192.168.1.135
    python dns_spoof.py --ip 192.168.1.135 --target manuals.playstation.net
"""
import argparse
import socket
import socketserver
import struct
import sys

DEFAULT_TARGET = "manuals.playstation.net"
DEFAULT_TTL = 300

def parse_query(data):
    if len(data) < 12:
        return None
    qid, _flags, qdcount, _, _, _ = struct.unpack(">HHHHHH", data[:12])
    if qdcount < 1:
        return None
    offset = 12
    labels = []
    while offset < len(data):
        length = data[offset]
        if length == 0:
            offset += 1
            break
        if length & 0xC0 == 0xC0:
            return None
        offset += 1
        if offset + length > len(data):
            return None
        labels.append(data[offset:offset + length].decode("ascii", "replace"))
        offset += length
    else:
        return None
    if offset + 4 > len(data):
        return None
    end = offset + 4
    return qid, data[12:end], ".".join(labels).lower()

def build_response(qid, question_bytes, ip=None):
    if ip is None:
        flags = 0x8183  # NXDOMAIN
        answer = b""
    else:
        flags = 0x8180
        answer = (
            b"\xc0\x0c"
            + struct.pack(">HHIH", 1, 1, DEFAULT_TTL, 4)
            + socket.inet_aton(ip)
        )
    header = struct.pack(">HHHHHH", qid, flags, 1, 1 if ip else 0, 0, 0)
    return header + question_bytes + answer

class DNSHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data, sock = self.request
        parsed = parse_query(data)
        if parsed is None:
            return
        qid, question_bytes, name = parsed
        target = self.server.target
        ip = self.server.ip
        if name == target:
            print(f"[DNS] {name} -> {ip}")
            sock.sendto(build_response(qid, question_bytes, ip), self.client_address)
        else:
            print(f"[DNS] {name} -> BLOCKED (NXDOMAIN)")
            sock.sendto(build_response(qid, question_bytes), self.client_address)

class DNSServer(socketserver.ThreadingUDPServer):
    allow_reuse_address = True

    def __init__(self, server_address, target, ip):
        self.target = target
        self.ip = ip
        super().__init__(server_address, DNSHandler)
def main():
    parser = argparse.ArgumentParser(description="Standalone DNS spoofer for PS5")
    parser.add_argument("--ip", required=True, help="Your PC's IP (e.g., 192.168.1.135)")
    parser.add_argument("--target", default=DEFAULT_TARGET, help="Domain to spoof")
    parser.add_argument("--port", type=int, default=53, help="DNS port (default: 53)")
    args = parser.parse_args()

    server = DNSServer(("0.0.0.0", args.port), args.target, args.ip)
    print(f"DNS spoofer running on port {args.port}")
    print(f"Spoofing {args.target} -> {args.ip}")
    print("All other domains -> NXDOMAIN (blocks PSN and updates)")
    print("Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.shutdown()

if __name__ == "__main__":
    main()
PY