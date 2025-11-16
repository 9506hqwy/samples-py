#!/usr/bin/env python3
# /// script
# dependencies = []
# requires-python = ">=3.12"
# ///
"""WoL リクエストを受信する.

マジックパケットを受信してターゲット MAC アドレスを表示する.

マジックパケットのフォーマット:
+--------------------------+----------+-------------------------------|
| ブロードキャストアドレス | 6 バイト | 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF |
| ターゲット MAC アドレス  | 6 バイト | ターゲットの MAC アドレス     |
| x16 繰り返す             |          |                               |
+--------------------------+----------+-------------------------------|
"""

import socket
import struct
from collections.abc import Generator

# ブロードキャストパケットのみ受信
dest_mac = struct.pack(b"!6B", 255, 255, 255, 255, 255, 255)


def iter_wol_request() -> Generator[tuple]:
    """WoL リクエストを受信する."""
    # すべてのインターフェイスで受信する。
    # s = socket.socket(socket.AF_PACKET, socket.SOCK_DGRAM, socket.ntohs(0x0003))
    # proto=0x0003 (ETH_P_ALL): すべてのイーサネットタイプを受信

    # AF_PACKET でパケットを受信できない場合がある。
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", 9))  # WoL ポート番号 9

    print("Listening for WoL requests on UDP port 9...")
    print("Stop with Ctrl-C")
    while True:
        p = s.recvfrom(4096)
        if p[0][0:6] == dest_mac:
            req_mac = p[0][6:12]
            magic = req_mac * 16
            if p[0][6:102] == magic:
                req = struct.unpack(b"!6B", req_mac)
                yield req


def main() -> None:
    """WoL リクエストを受信して MAC アドレスを表示する."""
    for mac in iter_wol_request():
        mac_str = b"req %02x:%02x:%02x:%02x:%02x:%02x" % mac
        print(f"request: {mac_str.decode()}")


if __name__ == "__main__":
    main()
