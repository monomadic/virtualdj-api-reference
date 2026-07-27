#!/usr/bin/env python3
"""Subscribe arbitrary VDJScript queries over the VirtualDJ Remote protocol.

Impersonates a Remote device: reuses a captured opener's setup/info/panel prefix
verbatim, substitutes your own SUBSCRIBE/KIND frames, and prints every value
VirtualDJ pushes. VirtualDJ is the TCP client, so pair this with an advert:

    python3 tools/vdjremote_subscribe.py tests/vdjremote-opener.bin \
        'left:get_title' 'left:get_bpm' 'get_clock' &
    dns-sd -R "iPad" _vdjremote8._tcp . 4243

Each query is `[scope:]script`, where scope is `left`, `righ`, or omitted for
global. Deck scoping also works inside the script itself (`deck 3 get_bpm`).
If VirtualDJ does not dial in, drop and re-add the dns-sd registration.

See docs/Remote Protocol.md.
"""
import socket
import struct
import sys
import threading
import time

MAGIC = b"8JDV"
PORT = 4243
SCOPES = {"left", "righ", "right"}


def ts() -> str:
    return time.strftime("%H:%M:%S")


def frame(mtype: int, body: bytes) -> bytes:
    return MAGIC + struct.pack("<I", 8 + 2 + len(body)) + struct.pack("<H", mtype) + body


def scope_bytes(word: str) -> bytes:
    """Deck scope is a fourcc stored little-endian: 'left' goes out as b'tfel'."""
    if not word:
        return b"\x00\x00\x00\x00"
    return word.encode()[:4].ljust(4, b"\x00")[::-1]


def fourcc(raw: bytes) -> str:
    return "".join(chr(c) if 32 <= c < 127 else "." for c in raw)[::-1].strip(".")


def parse_query(arg: str):
    head, sep, rest = arg.partition(":")
    if sep and head in SCOPES:
        return head[:4], rest
    return "", arg


def build_opener(capture: str, queries) -> bytes:
    data = open(capture, "rb").read()
    off = 0
    while off + 8 <= len(data):
        total = struct.unpack_from("<I", data, off + 4)[0]
        if struct.unpack_from("<H", data, off + 8)[0] == 0x01:
            break
        off += total
    out = bytearray(data[:off])
    for i, (scope, script) in enumerate(queries):
        out += frame(0x01, struct.pack("<H", i) + scope_bytes(scope) + script.encode())
        # KIND is only a hint — VirtualDJ answers with whatever type the query yields.
        out += frame(0x03, struct.pack("<H", 1) + struct.pack("<I", i))
    return bytes(out)


def decode(buf: bytearray, queries) -> None:
    while len(buf) >= 8:
        if bytes(buf[:4]) != MAGIC:
            nxt = bytes(buf).find(MAGIC, 1)
            del buf[: nxt if nxt > 0 else len(buf)]
            continue
        total = struct.unpack_from("<I", buf, 4)[0]
        if total < 8 or len(buf) < total:
            return
        payload = bytes(buf[8:total])
        del buf[:total]
        if struct.unpack_from("<H", payload, 0)[0] != 0x05 or len(payload) < 8:
            continue
        body = payload[2:]
        qid = struct.unpack_from("<H", body, 0)[0]
        kind = fourcc(body[2:6])
        rest = body[6:]
        if kind == "val" and len(rest) >= 4:
            shown = f"{struct.unpack_from('<f', rest, 0)[0]:g}"
        elif kind == "txt" and len(rest) >= 4:
            length = struct.unpack_from("<I", rest, 0)[0]
            shown = rest[4:4 + length].decode(errors="replace")
        elif kind == "fail":
            shown = "(no value)"
        else:
            shown = rest.hex(" ")
        label = queries[qid][1] if qid < len(queries) else f"id={qid}"
        print(f"{ts()} {kind:<4} {shown:<40} {label}", flush=True)


def handle(conn, addr, opener, queries, hold) -> None:
    print(f"{ts()} VirtualDJ connected from {addr[0]}:{addr[1]}", flush=True)
    conn.sendall(opener)
    conn.settimeout(hold)
    buf = bytearray()
    try:
        while True:
            data = conn.recv(65536)
            if not data:
                break
            buf += data
            decode(buf, queries)
    except (socket.timeout, OSError):
        pass
    finally:
        conn.close()
    print(f"{ts()} session closed", flush=True)


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    capture, args = sys.argv[1], sys.argv[2:]
    queries = [parse_query(a) for a in args]
    opener = build_opener(capture, queries)
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", PORT))
    srv.listen(5)
    print(f"{ts()} listening on {PORT} with {len(queries)} subscriptions "
          f"({len(opener)} byte opener); advertise the service to be dialed", flush=True)
    while True:
        conn, addr = srv.accept()
        threading.Thread(target=handle, args=(conn, addr, opener, queries, 300), daemon=True).start()


if __name__ == "__main__":
    main()
