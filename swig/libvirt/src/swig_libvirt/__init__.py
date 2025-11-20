"""SWIG Libvirt Package."""

from typing import Any

from . import native  # type: ignore[attr-defined]


def version() -> None:
    """ハイパーバイザーのバージョンを取得する."""
    native.virEventRegisterDefaultImpl()

    conn = native.virConnectOpen(None)

    hvtype = native.virConnectGetType(conn)

    _ret, ver = native.virConnectGetVersion(conn)
    major = ver // 1000000
    minor = (ver // 1000) % 1000
    release = ver % 1000

    print(f"{hvtype}: {major}.{minor}.{release}")

    native.virConnectClose(conn)


def pool_events() -> None:
    """ストレージプールのイベントを監視する."""

    def timeout(timer: int) -> None:
        pass

    def pool_event_callback(
        conn: Any,  # noqa: ANN401
        pool: Any,  # noqa: ANN401
        event: int,
        detail: int,
    ) -> None:
        name = native.virStoragePoolGetName(pool)
        print(f"{name}: event={event}, detail={detail}")

    native.virEventRegisterDefaultImpl()
    timer = native.virEventAddTimeout(100, timeout)

    conn = native.virConnectOpen(None)

    # 0: VIR_STORAGE_POOL_EVENT_ID_LIFECYCLE
    event = native.virConnectStoragePoolEventRegisterAny(
        conn,
        None,
        0,
        pool_event_callback,
    )

    try:
        while True:
            if native.virEventRunDefaultImpl() < 0:
                break
    except KeyboardInterrupt:
        pass

    native.virConnectStoragePoolEventDeregisterAny(conn, event)
    native.virEventRemoveTimeout(timer)
    native.virConnectClose(conn)


def pool_names() -> None:
    """アクティブなストレージプールの名前を取得する."""
    native.virEventRegisterDefaultImpl()

    conn = native.virConnectOpen(None)

    num_pools = native.virConnectNumOfStoragePools(conn)
    _ret, names = native.virConnectListStoragePools(conn, num_pools)
    for name in names:
        print(name)

    native.virConnectClose(conn)


def pools() -> None:
    """すべてのストレージプールの名前を取得する."""
    native.virEventRegisterDefaultImpl()

    conn = native.virConnectOpen(None)

    # 1: VIR_CONNECT_LIST_STORAGE_POOLS_INACTIVE
    # 2: VIR_CONNECT_LIST_STORAGE_POOLS_ACTIVE
    _ret, pools = native.virConnectListAllStoragePools(conn, 1 | 2)
    for pool in pools:
        name = native.virStoragePoolGetName(pool)
        print(name)

        native.virStoragePoolFree(pool)

    native.virConnectClose(conn)


if __name__ == "__main__":
    version()
    pool_events()
    pool_names()
    pools()
