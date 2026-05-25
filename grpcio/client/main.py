"""gRPC Client package."""

from collections.abc import Iterator

import grpc
import service_pb2
import service_pb2_grpc
from google.protobuf import empty_pb2
from google.protobuf.json_format import MessageToJson

"""
Python はサーバ検証処理をスキップできないため TLS 通信をしない。

通信を行うのは C のコードのため Python の設定は効果がない。
https://www.python.org/dev/peps/pep-0476/

対応する PR はあるがマージされていない。
https://github.com/grpc/grpc/pull/12656

C++ は対応する機能が追加されている。
https://github.com/grpc/grpc/pull/21423
"""


def main() -> None:
    """Entrypoint."""
    with grpc.insecure_channel("127.0.0.1:5000") as channel:
        client = service_pb2_grpc.ApiStub(channel)

        # Call
        req = service_pb2.ScalarValueTypes()
        res, _ = client.Call.with_call(req)
        print(MessageToJson(res))

        # Download
        req = empty_pb2.Empty()
        res = client.Download(req)
        count = 0
        for msg in res:
            print(f"Message: {msg.message}")
            count += 1

            if count > 3:  # noqa: PLR2004
                break

        # Upload
        def res() -> Iterator[service_pb2.Message]:
            yield service_pb2.Message(message="count 0")
            yield service_pb2.Message(message="count 1")
            yield service_pb2.Message(message="count 2")

        res, _ = client.Upload.with_call(res())
        print(MessageToJson(res))

        # Async
        def res() -> Iterator[service_pb2.Message]:
            yield service_pb2.Message(message="count 0")
            yield service_pb2.Message(message="count 1")
            yield service_pb2.Message(message="count 2")

        res = client.Async(res())
        for msg in res:
            print(f"Message: {msg.message}")


if __name__ == "__main__":
    main()
