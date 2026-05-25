"""gRPC Server package."""

import copy
import time
from collections.abc import Iterator
from concurrent import futures
from pathlib import Path

import grpc
import service_pb2
import service_pb2_grpc
from google.protobuf import empty_pb2


class Service(service_pb2_grpc.ApiServicer):
    """gRPC Server."""

    def Call(  # noqa: N802
        self, request: service_pb2.ScalarValueTypes, context: grpc.ServicerContext
    ) -> service_pb2.ScalarValueTypes:
        """Call method."""
        req = copy.deepcopy(request)
        return req

    def Download(  # noqa: N802
        self, request: empty_pb2.Empty, context: grpc.ServicerContext
    ) -> Iterator[service_pb2.Message]:
        """Download method."""
        counter = 0
        try:
            while True:
                time.sleep(1)
                yield service_pb2.Message(message=f"count {counter}")

                counter += 1
        except Exception as e:
            print(e)

    def Upload(  # noqa: N802
        self,
        request_iterator: Iterator[service_pb2.Message],
        context: grpc.ServicerContext,
    ) -> empty_pb2.Empty:
        """Upload method."""
        for msg in request_iterator:
            print(f"Upload: {msg.message}")

        return empty_pb2.Empty()

    def Async(  # noqa: N802
        self,
        request_iterator: Iterator[service_pb2.Message],
        context: grpc.ServicerContext,
    ) -> Iterator[service_pb2.Message]:
        """Async method."""
        try:
            yield from request_iterator
        except Exception as e:
            print(e)


def main() -> None:
    """Entrypoint."""
    pkey = Path("key.pem")
    cert = Path("cert.pem")
    creds = grpc.ssl_server_credentials(
        [
            (pkey.read_bytes(), cert.read_bytes()),
        ]
    )
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_ApiServicer_to_server(Service(), server)  # type: ignore[no-untyped-call]
    server.add_insecure_port("0.0.0.0:5000")
    server.add_secure_port("0.0.0.0:5001", creds)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()
