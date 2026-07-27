#!/usr/bin/env python3
"""Capture and decode the VirtualDJ Remote protocol handshake.

The Remote device is the TCP server and speaks first (VirtualDJ dials out and
stays silent), so capturing its opener needs nothing but a client socket: open
the Remote app, leave it on the connect screen, and dial it.

    python3 tools/vdjremote_dial.py <device-ip> [port] [seconds]
    python3 tools/vdjremote_dial.py --decode <capture.bin>

Frame: b"8JDV" (fourcc 'VDJ8' stored LE) + u32 LE total length (header included)
+ payload, payload starting with a u16 LE message type. See
docs/Remote Protocol.md.
"""
import socket
import struct
import sys
import time

MAGIC = b"8JDV"
DEFAULT_PORT = 4243


def fourcc(raw: bytes) -> str:
    """Decode a little-endian fourcc; 'left' is stored as bytes 'tfel'."""
    text = "".join(chr(c) if 32 <= c < 127 else "." for c in raw)
    return text[::-1]


def decode(data: bytes) -> None:
    off = n = 0
    while off + 8 <= len(data):
        if data[off:off + 4] != MAGIC:
            nxt = data.find(MAGIC, off + 1)
            print(f"!! desync at {off}, resyncing")
            if nxt < 0:
                break
            off = nxt
            continue
        total = struct.unpack_from("<I", data, off + 4)[0]
        if total < 8 or off + total > len(data):
            print(f"!! truncated frame at {off} (len={total}, {len(data) - off} available)")
            break
        payload = data[off + 8:off + total]
        mtype = struct.unpack_from("<H", payload, 0)[0]
        body = payload[2:]
        n += 1
        if mtype == 0x01 and len(body) >= 6:
            qid = struct.unpack_from("<H", body, 0)[0]
            scope = fourcc(body[2:6]).strip(".") or "global"
            print(f"{n:3} SUBSCRIBE id={qid:<3} scope={scope:<8} script={body[6:].decode(errors='replace')!r}")
        elif mtype == 0x03 and len(body) >= 6:
            kind = struct.unpack_from("<H", body, 0)[0]
            qid = struct.unpack_from("<I", body, 2)[0]
            print(f"{n:3} KIND      id={qid:<3} kind={kind}")
        elif mtype == 0x24:
            print(f"{n:3} PANEL     {body[2:].decode(errors='replace')!r}")
        elif mtype == 0x40:
            print(f"{n:3} INFO      {body[6:].decode(errors='replace').strip()!r}")
        else:
            print(f"{n:3} type=0x{mtype:04x}  {body.hex(' ')}")
        off += total
    print(f"--- {n} frames, {off}/{len(data)} bytes consumed")


def dial(host: str, port: int, secs: int) -> bytes:
    print(f"dialing {host}:{port} (sending nothing, listening {secs}s)")
    raw = bytearray()
    try:
        sock = socket.create_connection((host, port), timeout=10)
    except OSError as exc:
        sys.exit(f"connect failed: {exc} — is the Remote app open and on its connect screen?")
    sock.settimeout(secs)
    try:
        while True:
            chunk = sock.recv(65536)
            if not chunk:
                break
            raw += chunk
            print(f"{time.strftime('%H:%M:%S')} recv {len(chunk)} bytes (total {len(raw)})")
    except socket.timeout:
        pass
    finally:
        sock.close()
    return bytes(raw)


def main() -> None:
    if len(sys.argv) >= 3 and sys.argv[1] == "--decode":
        decode(open(sys.argv[2], "rb").read())
        return
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
    secs = int(sys.argv[3]) if len(sys.argv) > 3 else 25
    raw = dial(host, port, secs)
    if not raw:
        sys.exit("no data received — the device sent nothing")
    out = "vdjremote-capture.bin"
    with open(out, "wb") as handle:
        handle.write(raw)
    print(f"saved {len(raw)} bytes to {out}\n")
    decode(raw)


if __name__ == "__main__":
    main()
