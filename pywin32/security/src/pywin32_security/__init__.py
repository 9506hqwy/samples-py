"""pywin32 Security Package."""

from __future__ import annotations

import sys
from enum import IntEnum, IntFlag
from pathlib import Path

import ntsecuritycon
import winnt
from win32security import (
    DACL_SECURITY_INFORMATION,
    GROUP_SECURITY_INFORMATION,
    OWNER_SECURITY_INFORMATION,
    SE_FILE_OBJECT,
    GetNamedSecurityInfo,
    LookupAccountSid,
)


class AceType(IntEnum):
    """ACE 文字列 種別.

    https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-ace_header
    """

    ACCESS_ALLOWED_ACE_TYPE = ntsecuritycon.ACCESS_ALLOWED_ACE_TYPE
    ACCESS_ALLOWED_CALLBACK_ACE_TYPE = ntsecuritycon.ACCESS_ALLOWED_CALLBACK_ACE_TYPE
    ACCESS_ALLOWED_CALLBACK_OBJECT_ACE_TYPE = ntsecuritycon.ACCESS_ALLOWED_CALLBACK_OBJECT_ACE_TYPE
    ACCESS_ALLOWED_COMPOUND_ACE_TYPE = ntsecuritycon.ACCESS_ALLOWED_COMPOUND_ACE_TYPE
    ACCESS_ALLOWED_OBJECT_ACE_TYPE = ntsecuritycon.ACCESS_ALLOWED_OBJECT_ACE_TYPE
    ACCESS_DENIED_ACE_TYPE = ntsecuritycon.ACCESS_DENIED_ACE_TYPE
    ACCESS_DENIED_CALLBACK_ACE_TYPE = ntsecuritycon.ACCESS_DENIED_CALLBACK_ACE_TYPE
    ACCESS_DENIED_CALLBACK_OBJECT_ACE_TYPE = ntsecuritycon.ACCESS_DENIED_CALLBACK_OBJECT_ACE_TYPE
    ACCESS_DENIED_OBJECT_ACE_TYPE = ntsecuritycon.ACCESS_DENIED_OBJECT_ACE_TYPE
    ACCESS_MAX_MS_ACE_TYPE = ntsecuritycon.ACCESS_MAX_MS_ACE_TYPE
    ACCESS_MAX_MS_V2_ACE_TYPE = ntsecuritycon.ACCESS_MAX_MS_V2_ACE_TYPE
    ACCESS_MAX_MS_V3_ACE_TYPE = ntsecuritycon.ACCESS_MAX_MS_V3_ACE_TYPE
    ACCESS_MAX_MS_V4_ACE_TYPE = ntsecuritycon.ACCESS_MAX_MS_V4_ACE_TYPE
    ACCESS_MAX_MS_OBJECT_ACE_TYPE = ntsecuritycon.ACCESS_MAX_MS_OBJECT_ACE_TYPE
    ACCESS_MIN_MS_ACE_TYPE = ntsecuritycon.ACCESS_MIN_MS_ACE_TYPE
    ACCESS_MIN_MS_OBJECT_ACE_TYPE = ntsecuritycon.ACCESS_MIN_MS_OBJECT_ACE_TYPE
    SYSTEM_ALARM_ACE_TYPE = ntsecuritycon.SYSTEM_ALARM_ACE_TYPE
    SYSTEM_ALARM_CALLBACK_ACE_TYPE = ntsecuritycon.SYSTEM_ALARM_CALLBACK_ACE_TYPE
    SYSTEM_ALARM_CALLBACK_OBJECT_ACE_TYPE = ntsecuritycon.SYSTEM_ALARM_CALLBACK_OBJECT_ACE_TYPE
    SYSTEM_ALARM_OBJECT_ACE_TYPE = ntsecuritycon.SYSTEM_ALARM_OBJECT_ACE_TYPE
    SYSTEM_AUDIT_ACE_TYPE = ntsecuritycon.SYSTEM_AUDIT_ACE_TYPE
    SYSTEM_AUDIT_CALLBACK_ACE_TYPE = ntsecuritycon.SYSTEM_AUDIT_CALLBACK_ACE_TYPE
    SYSTEM_AUDIT_CALLBACK_OBJECT_ACE_TYPE = ntsecuritycon.SYSTEM_AUDIT_CALLBACK_OBJECT_ACE_TYPE
    SYSTEM_AUDIT_OBJECT_ACE_TYPE = ntsecuritycon.SYSTEM_AUDIT_OBJECT_ACE_TYPE
    SYSTEM_MANDATORY_LABEL_ACE_TYPE = ntsecuritycon.SYSTEM_MANDATORY_LABEL_ACE_TYPE

    @classmethod
    def get_label(cls, value: AceType) -> str:
        """表示名を取得する."""
        match value:
            case AceType.ACCESS_ALLOWED_ACE_TYPE:
                return "許可"
            case AceType.ACCESS_DENIED_ACE_TYPE:
                return "拒否"
            case _:
                return ""


class AceFlags(IntFlag):
    """ACE 文字列 フラグ.

    https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-ace_header
    """

    CONTAINER_INHERIT_ACE = ntsecuritycon.CONTAINER_INHERIT_ACE
    FAILED_ACCESS_ACE_FLAG = ntsecuritycon.FAILED_ACCESS_ACE_FLAG
    INHERIT_ONLY_ACE = ntsecuritycon.INHERIT_ONLY_ACE
    INHERITED_ACE = winnt.INHERITED_ACE
    NO_PROPAGATE_INHERIT_ACE = ntsecuritycon.NO_PROPAGATE_INHERIT_ACE
    OBJECT_INHERIT_ACE = ntsecuritycon.OBJECT_INHERIT_ACE
    SUCCESSFUL_ACCESS_ACE_FLAG = ntsecuritycon.SUCCESSFUL_ACCESS_ACE_FLAG

    @classmethod
    def get_label(cls, value: AceFlags) -> str:
        """表示名を取得する."""
        match value:
            case AceFlags.INHERITED_ACE:
                return "継承"
            case _:
                return "なし"


class AccessMask(IntFlag):
    """アクセス権.

    https://learn.microsoft.com/en-us/windows/win32/secauthz/access-mask
    https://learn.microsoft.com/en-us/windows/win32/secauthz/standard-access-rights
    https://learn.microsoft.com/en-us/windows/win32/FileIO/file-access-rights-constants
    """

    # Files and Directories.
    FILE_ADD_FILE = ntsecuritycon.FILE_ADD_FILE
    FILE_ADD_SUBDIRECTORY = ntsecuritycon.FILE_ADD_SUBDIRECTORY
    FILE_ALL_ACCESS = ntsecuritycon.FILE_ALL_ACCESS
    FILE_APPEND_DATA = ntsecuritycon.FILE_APPEND_DATA
    FILE_CREATE_PIPE_INSTANCE = ntsecuritycon.FILE_CREATE_PIPE_INSTANCE
    FILE_DELETE_CHILD = ntsecuritycon.FILE_DELETE_CHILD
    FILE_EXECUTE = ntsecuritycon.FILE_EXECUTE
    FILE_LIST_DIRECTORY = ntsecuritycon.FILE_LIST_DIRECTORY
    FILE_READ_ATTRIBUTES = ntsecuritycon.FILE_READ_ATTRIBUTES
    FILE_READ_DATA = ntsecuritycon.FILE_READ_DATA
    FILE_READ_EA = ntsecuritycon.FILE_READ_EA
    FILE_TRAVERSE = ntsecuritycon.FILE_TRAVERSE
    FILE_WRITE_ATTRIBUTES = ntsecuritycon.FILE_WRITE_ATTRIBUTES
    FILE_WRITE_DATA = ntsecuritycon.FILE_WRITE_DATA
    FILE_WRITE_EA = ntsecuritycon.FILE_WRITE_EA
    # Standard rights.
    DELETE = ntsecuritycon.DELETE
    READ_CONTROL = ntsecuritycon.READ_CONTROL
    WRITE_DAC = ntsecuritycon.WRITE_DAC
    WRITE_OWNER = ntsecuritycon.WRITE_OWNER
    SYNCHRONIZE = ntsecuritycon.SYNCHRONIZE
    ACCESS_SYSTEM_SECURITY = ntsecuritycon.ACCESS_SYSTEM_SECURITY
    MAXIMUM_ALLOWED = ntsecuritycon.MAXIMUM_ALLOWED
    GENERIC_ALL = ntsecuritycon.GENERIC_ALL
    GENERIC_EXECUTE = ntsecuritycon.GENERIC_EXECUTE
    GENERIC_WRITE = ntsecuritycon.GENERIC_WRITE
    GENERIC_READ = ntsecuritycon.GENERIC_READ
    STANDARD_RIGHTS_ALL = DELETE | READ_CONTROL | WRITE_DAC | WRITE_OWNER | SYNCHRONIZE
    STANDARD_RIGHTS_EXECUTE = READ_CONTROL
    STANDARD_RIGHTS_READ = READ_CONTROL
    STANDARD_RIGHTS_REQUIRED = DELETE | READ_CONTROL | WRITE_DAC | WRITE_OWNER
    STANDARD_RIGHTS_WRITE = READ_CONTROL

    @classmethod
    def get_perm_list(cls) -> dict[str, AccessMask]:
        """アクセス許可を取得する."""
        return {
            # 高度なアクセス許可
            "フォルダーのスキャン/ファイルの実行": AccessMask.FILE_EXECUTE
            | AccessMask.SYNCHRONIZE,
            "フォルダーの一覧/データの読み取り": AccessMask.FILE_LIST_DIRECTORY
            | AccessMask.SYNCHRONIZE,
            "属性の読み取り": AccessMask.FILE_READ_ATTRIBUTES | AccessMask.SYNCHRONIZE,
            "拡張属性の読み取り": AccessMask.FILE_READ_EA | AccessMask.SYNCHRONIZE,
            "ファイルの作成/データの書き込み": AccessMask.FILE_ADD_FILE | AccessMask.SYNCHRONIZE,
            "フォルダーの作成/データの追加": AccessMask.FILE_ADD_SUBDIRECTORY
            | AccessMask.SYNCHRONIZE,
            "属性の書き込み": AccessMask.FILE_WRITE_ATTRIBUTES | AccessMask.SYNCHRONIZE,
            "拡張属性の書き込み": AccessMask.FILE_WRITE_EA | AccessMask.SYNCHRONIZE,
            "削除": AccessMask.DELETE | AccessMask.SYNCHRONIZE,
            "アクセス許可の読み取り": AccessMask.READ_CONTROL | AccessMask.SYNCHRONIZE,
            "アクセス許可の変更": AccessMask.WRITE_DAC | AccessMask.SYNCHRONIZE,
            "所有権の取得": AccessMask.WRITE_OWNER | AccessMask.SYNCHRONIZE,
            # 基本のアクセス許可
            "フルコントロール": AccessMask.FILE_ALL_ACCESS,
            "変更": AccessMask.FILE_ADD_FILE
            | AccessMask.FILE_ADD_SUBDIRECTORY
            | AccessMask.FILE_EXECUTE
            | AccessMask.FILE_LIST_DIRECTORY
            | AccessMask.FILE_READ_ATTRIBUTES
            | AccessMask.FILE_READ_EA
            | AccessMask.FILE_WRITE_ATTRIBUTES
            | AccessMask.FILE_WRITE_EA
            | AccessMask.DELETE
            | AccessMask.READ_CONTROL
            | AccessMask.SYNCHRONIZE,
            "読み取りと実行": AccessMask.FILE_EXECUTE
            | AccessMask.FILE_LIST_DIRECTORY
            | AccessMask.FILE_READ_ATTRIBUTES
            | AccessMask.FILE_READ_EA
            | AccessMask.READ_CONTROL
            | AccessMask.SYNCHRONIZE,
            "読み取り": AccessMask.FILE_LIST_DIRECTORY
            | AccessMask.FILE_READ_ATTRIBUTES
            | AccessMask.FILE_READ_EA
            | AccessMask.READ_CONTROL
            | AccessMask.SYNCHRONIZE,
            "書き込み": AccessMask.FILE_ADD_FILE
            | AccessMask.FILE_ADD_SUBDIRECTORY
            | AccessMask.FILE_WRITE_ATTRIBUTES
            | AccessMask.FILE_WRITE_EA
            | AccessMask.SYNCHRONIZE,
        }

    @classmethod
    def get_label(cls, value: AccessMask) -> list[str]:
        """表示名を取得する."""
        perms = sorted(cls.get_perm_list().items(), key=lambda kv: kv[1], reverse=True)
        names = []
        combined = AccessMask.SYNCHRONIZE
        for name, mask in perms:
            if (mask & value) == mask:
                if (mask & combined) != mask:
                    names.append(name)
                    combined |= mask

        if value != combined:
            raise ValueError(f"Not supported value '0x{(not combined) & value:x}'")

        return names


def file_dacl() -> None:
    """ファイルの Discretionary Access Control を取得する."""
    path = sys.argv[1]
    if not Path(path).exists():
        raise FileNotFoundError(f"Not found file: '{path}'")

    # ファイルのセキュリティ記述子を取得する。
    info = GetNamedSecurityInfo(path, SE_FILE_OBJECT, DACL_SECURITY_INFORMATION)

    # ファイルの DACL を取得する。
    dacl = info.GetSecurityDescriptorDacl()

    for i in range(0, dacl.GetAceCount()):
        # アクセス制御エントリを取得する。
        (ace_type, ace_flags), mask, sid = dacl.GetAce(i)

        ace_type_label = AceType.get_label(AceType(ace_type))
        ace_flags_label = AceFlags.get_label(AceFlags(ace_flags))
        access_masks = ",".join(AccessMask.get_label(AccessMask(mask)))

        account = LookupAccountSid(None, sid)
        account_name = f"{account[1]}\\{account[0]}"

        print(f"{path}: {ace_type_label} {ace_flags_label} {access_masks} {account_name}")


def file_group() -> None:
    """ファイルのグループを取得する."""
    path = sys.argv[1]
    if not Path(path).exists():
        raise FileNotFoundError(f"No found file: '{path}'")

    # ファイルのセキュリティ記述子を取得する。
    info = GetNamedSecurityInfo(path, SE_FILE_OBJECT, GROUP_SECURITY_INFORMATION)

    # ファイルのグループの SID を取得する。
    group_sid = info.GetSecurityDescriptorGroup()  # type: ignore[attr-defined]
    if group_sid is None:
        raise ValueError("Not group SID found.")

    # SID からグループ名を取得する。
    # (アカウント名, ドメイン名, SID タイプ) のタプルが取得できる。
    account = LookupAccountSid(None, group_sid)
    print(f"{path}: {account[1]}\\{account[0]}")


def file_owner() -> None:
    """ファイルの所有者を取得する."""
    path = sys.argv[1]
    if not Path(path).exists():
        raise FileNotFoundError(f"Not found file: '{path}'")

    # ファイルのセキュリティ記述子を取得する。
    info = GetNamedSecurityInfo(path, SE_FILE_OBJECT, OWNER_SECURITY_INFORMATION)

    # ファイルの所有者の SID を取得する。
    owner = info.GetSecurityDescriptorOwner()

    # SID からアカウント名を取得する。
    # (アカウント名, ドメイン名, SID タイプ) のタプルが取得できる。
    account = LookupAccountSid(None, owner)
    print(f"{path}: {account[1]}\\{account[0]}")


if __name__ == "__main__":
    file_dacl()
    file_group()
    file_owner()
