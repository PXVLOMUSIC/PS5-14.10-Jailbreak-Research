#!/usr/bin/env python3
"""Generate a self-signed TLS certificate using Python's standard library.

No external dependencies (no openssl, no cryptography, no pyOpenSSL).
Uses RSA-2048 and SHA-256.

Usage:
    python gen_cert.py --cn manuals.playstation.net --out cert.pem --key key.pem
"""
import argparse
import hashlib
import os
import random
import struct
import sys

# --- ASN.1 DER encoding helpers ---

def der_length(length):
    if length < 128:
        return bytes([length])
    result = []
    while length > 0:
        result.append(length & 0xFF)
        length >>= 8
    result.reverse()
    return bytes([0x80 | len(result)] + result)

def der_tag(tag, data):
    return bytes([tag]) + der_length(len(data)) + data

def der_sequence(data):
    return der_tag(0x30, data)

def der_set(data):
    return der_tag(0x31, data)

def der_integer(value):
    if value == 0:
        return der_tag(0x02, b"\x00")
    # Convert to bytes
    if isinstance(value, int):
        byte_len = (value.bit_length() + 7) // 8
        data = value.to_bytes(byte_len, "big")
    else:
        data = value
    # Add leading zero if high bit set
    if data[0] & 0x80:
        data = b"\x00" + data
    return der_tag(0x02, data)

def der_bit_string(data):
    return der_tag(0x03, b"\x00" + data)

def der_octet_string(data):
    return der_tag(0x04, data)

def der_oid(oid_str):
    parts = [int(x) for x in oid_str.split(".")]
    # First two components encoded as 40*first + second
    first = parts[0] * 40 + parts[1]
    result = [first]
    for p in parts[2:]:
        # Variable-length encoding
        if p < 128:
            result.append(p)
        else:
            temp = []
            while p > 0:
                temp.append(p & 0x7F)
                p >>= 7
            temp.reverse()
            for i in range(len(temp) - 1):
                result.append(temp[i] | 0x80)
            result.append(temp[-1])
    return der_tag(0x06, bytes(result))

def der_null():
    return b"\x05\x00"

def der_utf8_string(s):
    return der_tag(0x0C, s.encode("utf-8"))

def der_printable_string(s):
    return der_tag(0x13, s.encode("ascii"))

def der_ia5_string(s):
    return der_tag(0x16, s.encode("ascii"))

def der_utc_time(dt):
    s = dt.strftime("%y%m%d%H%M%SZ")
    return der_tag(0x17, s.encode("ascii"))

# --- RSA key generation (simplified) ---

def is_prime(n, k=20):
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if n % p == 0:
            return n == p
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    while True:
        n = random.getrandbits(bits)
        n |= (1 << (bits - 1))  # ensure high bit set
        n |= 1  # ensure odd
        if is_prime(n):
            return n

def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("No modular inverse")
    return x % m

def generate_rsa_key(bits=2048):
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    while p == q:
        q = generate_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = modinv(e, phi)
    return (n, e, d, p, q)

def rsa_encrypt(m, e, n):
    return pow(m, e, n)

def rsa_decrypt(c, d, n):
    return pow(c, d, n)

# --- X.509 certificate generation ---

def encode_rsa_public_key(n, e):
    # RSAPublicKey ::= SEQUENCE { modulus INTEGER, publicExponent INTEGER }
    return der_sequence(der_integer(n) + der_integer(e))

def encode_rsa_private_key(n, e, d, p, q):
    # RSAPrivateKey ::= SEQUENCE { version, n, e, d, p, q, dp, dq, qinv }
    dp = d % (p - 1)
    dq = d % (q - 1)
    qinv = modinv(q, p)
    return der_sequence(
        der_integer(0) +  # version
        der_integer(n) +
        der_integer(e) +
        der_integer(d) +
        der_integer(p) +
        der_integer(q) +
        der_integer(dp) +
        der_integer(dq) +
        der_integer(qinv)
    )

def create_certificate(cn, n, e, d, days=825):
    # Subject and issuer: CN=<cn>
    subject = der_sequence(
        der_set(
            der_sequence(
                der_oid("2.5.4.3") +  # commonName
                der_utf8_string(cn)
            )
        )
    )
    issuer = subject  # self-signed

    # Validity
    now = __import__("datetime").datetime.utcnow()
    not_before = now
    not_after = now + __import__("datetime").timedelta(days=days)

    # Serial number
    serial = random.getrandbits(64)

    # TBSCertificate
    tbs = der_sequence(
        der_tag(0xA0, der_integer(2)) +  # version v3
        der_integer(serial) +
        der_sequence(der_oid("1.2.840.113549.1.1.11") + der_null()) +  # sha256WithRSAEncryption
        issuer +
        der_sequence(der_utc_time(not_before) + der_utc_time(not_after)) +
        subject +
        der_sequence(der_sequence(der_oid("1.2.840.113549.1.1.1") + der_null()) + der_bit_string(encode_rsa_public_key(n, e))) +
        der_tag(0xA3, der_sequence(
            der_sequence(
                der_oid("2.5.29.17") +  # subjectAltName
                der_octet_string(der_sequence(der_tag(0x82, cn.encode("ascii"))))  # dNSName
            )
        ))
    )

    # Sign with SHA-256 + RSA
    tbs_hash = hashlib.sha256(tbs).digest()
    # PKCS#1 v1.5 padding
    k = (n.bit_length() + 7) // 8
    em = b"\x00\x01" + b"\xff" * (k - len(tbs_hash) - 3) + b"\x00" + tbs_hash
    em_int = int.from_bytes(em, "big")
    signature = pow(em_int, d, n)
    sig_bytes = signature.to_bytes(k, "big")

    # Certificate
    cert = der_sequence(
        tbs +
        der_sequence(der_oid("1.2.840.113549.1.1.11") + der_null()) +
        der_bit_string(sig_bytes)
    )

    return cert

def to_pem(data, label):
    b64 = __import__("base64").b64encode(data).decode("ascii")
    lines = [f"-----BEGIN {label}-----"]
    for i in range(0, len(b64), 64):
        lines.append(b64[i:i+64])
    lines.append(f"-----END {label}-----")
    return "\n".join(lines) + "\n"

def main():
    parser = argparse.ArgumentParser(description="Generate self-signed TLS cert with Python")
    parser.add_argument("--cn", default="manuals.playstation.net", help="Common Name")
    parser.add_argument("--out", default="cert.pem", help="Certificate output file")
    parser.add_argument("--key", default="key.pem", help="Private key output file")
    parser.add_argument("--days", type=int, default=825, help="Validity days")
    args = parser.parse_args()

    print("Generating 2048-bit RSA key...")
    n, e, d, p, q = generate_rsa_key(2048)

    print(f"Generating self-signed certificate for {args.cn}...")
    cert_der = create_certificate(args.cn, n, e, d, args.days)

    # Save certificate
    with open(args.out, "w") as f:
        f.write(to_pem(cert_der, "CERTIFICATE"))
    print(f"Certificate saved to: {args.out}")

    # Save private key (PKCS#8 format)
    # PKCS#8 PrivateKeyInfo ::= SEQUENCE { version, algorithm, privateKey }
    pkcs8 = der_sequence(
        der_integer(0) +
        der_sequence(der_oid("1.2.840.113549.1.1.1") + der_null()) +
        der_octet_string(encode_rsa_private_key(n, e, d, p, q))
    )
    with open(args.key, "w") as f:
        f.write(to_pem(pkcs8, "PRIVATE KEY"))
    print(f"Private key saved to: {args.key}")

    print("\nUsage with host.py:")
    print(f"  python host.py --cert {args.out} --key {args.key}")

if __name__ == "__main__":
    main()
PY