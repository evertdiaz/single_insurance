# flake8: noqa
# fmt: off
# mypy: disable-error-code="no-any-return, no-untyped-call"
# This file was automatically generated by algokit-client-generator.
# DO NOT MODIFY IT BY HAND.
# requires: algokit-utils@^1.2.0
import base64
import dataclasses
import decimal
import typing
from abc import ABC, abstractmethod

import algokit_utils
import algosdk
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    AtomicTransactionResponse,
    TransactionSigner,
    TransactionWithSigner
)

_APP_SPEC_JSON = r"""{
    "hints": {
        "createApp(account)string": {
            "call_config": {
                "no_op": "CREATE"
            }
        },
        "registerAsset(string,string,uint64)string": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "approveAsset(pay)string": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "claimInsurance(asset)string": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "hello(string)string": {
            "call_config": {
                "no_op": "CALL"
            }
        }
    },
    "source": {
        "approval": "I3ByYWdtYSB2ZXJzaW9uIDgKaW50Y2Jsb2NrIDAgMQpieXRlY2Jsb2NrIDB4IDB4MTUxZjdjNzUgMHg2MTczNzM2NTc0NDQ2NTczNjMgMHg2MTczNzM2NTc0NGU2MTZkNjUgMHg2MTczNzM2NTc0NTY2MTZjIDB4NzI2NTcxNzU2NTczNzQ1Mzc0NjE3NDY1IDB4NzI2NTcxNzU2NTczNzQ2NTcyIDB4NjE3MzYxNDk0NAp0eG5hIEFwcGxpY2F0aW9uQXJncyAwCnB1c2hieXRlcyAweDliOTQwZjM5IC8vICJjcmVhdGVBcHAoYWNjb3VudClzdHJpbmciCj09CmJueiBtYWluX2wxMAp0eG5hIEFwcGxpY2F0aW9uQXJncyAwCnB1c2hieXRlcyAweGZkMDhjZWY2IC8vICJyZWdpc3RlckFzc2V0KHN0cmluZyxzdHJpbmcsdWludDY0KXN0cmluZyIKPT0KYm56IG1haW5fbDkKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMApwdXNoYnl0ZXMgMHgyZDMxMTI0ZCAvLyAiYXBwcm92ZUFzc2V0KHBheSlzdHJpbmciCj09CmJueiBtYWluX2w4CnR4bmEgQXBwbGljYXRpb25BcmdzIDAKcHVzaGJ5dGVzIDB4NGQ4YmU5MDcgLy8gImNsYWltSW5zdXJhbmNlKGFzc2V0KXN0cmluZyIKPT0KYm56IG1haW5fbDcKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMApwdXNoYnl0ZXMgMHgwMmJlY2UxMSAvLyAiaGVsbG8oc3RyaW5nKXN0cmluZyIKPT0KYm56IG1haW5fbDYKZXJyCm1haW5fbDY6CnR4biBPbkNvbXBsZXRpb24KaW50Y18wIC8vIE5vT3AKPT0KdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKIT0KJiYKYXNzZXJ0CmNhbGxzdWIgaGVsbG9jYXN0ZXJfOQppbnRjXzEgLy8gMQpyZXR1cm4KbWFpbl9sNzoKdHhuIE9uQ29tcGxldGlvbgppbnRjXzAgLy8gTm9PcAo9PQp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAohPQomJgphc3NlcnQKY2FsbHN1YiBjbGFpbUluc3VyYW5jZWNhc3Rlcl84CmludGNfMSAvLyAxCnJldHVybgptYWluX2w4Ogp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCiE9CiYmCmFzc2VydApjYWxsc3ViIGFwcHJvdmVBc3NldGNhc3Rlcl83CmludGNfMSAvLyAxCnJldHVybgptYWluX2w5Ogp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCiE9CiYmCmFzc2VydApjYWxsc3ViIHJlZ2lzdGVyQXNzZXRjYXN0ZXJfNgppbnRjXzEgLy8gMQpyZXR1cm4KbWFpbl9sMTA6CnR4biBPbkNvbXBsZXRpb24KaW50Y18wIC8vIE5vT3AKPT0KdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKPT0KJiYKYXNzZXJ0CmNhbGxzdWIgY3JlYXRlQXBwY2FzdGVyXzUKaW50Y18xIC8vIDEKcmV0dXJuCgovLyBjcmVhdGVBcHAKY3JlYXRlQXBwXzA6CnByb3RvIDEgMQpieXRlY18wIC8vICIiCmJ5dGVjIDcgLy8gImFzYUlEIgppbnRjXzAgLy8gMAphcHBfZ2xvYmFsX3B1dApieXRlY18yIC8vICJhc3NldERlc2MiCmJ5dGVjXzAgLy8gIiIKYXBwX2dsb2JhbF9wdXQKYnl0ZWNfMyAvLyAiYXNzZXROYW1lIgpieXRlY18wIC8vICIiCmFwcF9nbG9iYWxfcHV0CmJ5dGVjIDQgLy8gImFzc2V0VmFsIgppbnRjXzAgLy8gMAphcHBfZ2xvYmFsX3B1dApieXRlYyA1IC8vICJyZXF1ZXN0U3RhdGUiCmludGNfMCAvLyAwCmFwcF9nbG9iYWxfcHV0CmJ5dGVjIDYgLy8gInJlcXVlc3RlciIKYnl0ZWNfMCAvLyAiIgphcHBfZ2xvYmFsX3B1dApieXRlYyA2IC8vICJyZXF1ZXN0ZXIiCmZyYW1lX2RpZyAtMQp0eG5hcyBBY2NvdW50cwphcHBfZ2xvYmFsX3B1dApmcmFtZV9kaWcgLTEKdHhuYXMgQWNjb3VudHMKZnJhbWVfYnVyeSAwCmZyYW1lX2RpZyAwCmxlbgppdG9iCmV4dHJhY3QgNiAwCmZyYW1lX2RpZyAwCmNvbmNhdApmcmFtZV9idXJ5IDAKcmV0c3ViCgovLyByZWdpc3RlckFzc2V0CnJlZ2lzdGVyQXNzZXRfMToKcHJvdG8gMyAxCmJ5dGVjXzAgLy8gIiIKdHhuIFNlbmRlcgpieXRlYyA2IC8vICJyZXF1ZXN0ZXIiCmFwcF9nbG9iYWxfZ2V0Cj09Ci8vIHVuYXV0aG9yaXplZAphc3NlcnQKYnl0ZWMgNSAvLyAicmVxdWVzdFN0YXRlIgppbnRjXzEgLy8gMQphcHBfZ2xvYmFsX3B1dApieXRlY18zIC8vICJhc3NldE5hbWUiCmZyYW1lX2RpZyAtMwpleHRyYWN0IDIgMAphcHBfZ2xvYmFsX3B1dApieXRlY18yIC8vICJhc3NldERlc2MiCmZyYW1lX2RpZyAtMgpleHRyYWN0IDIgMAphcHBfZ2xvYmFsX3B1dApieXRlYyA0IC8vICJhc3NldFZhbCIKZnJhbWVfZGlnIC0xCmFwcF9nbG9iYWxfcHV0CnB1c2hieXRlcyAweDAwMWM0MTczNzM2NTc0MjA3MjY1Njc2OTczNzQ3MjYxNjQ2ZjIwNjM2ZjZlMjBjM2E5Nzg2OTc0NmYyZSAvLyAweDAwMWM0MTczNzM2NTc0MjA3MjY1Njc2OTczNzQ3MjYxNjQ2ZjIwNjM2ZjZlMjBjM2E5Nzg2OTc0NmYyZQpmcmFtZV9idXJ5IDAKcmV0c3ViCgovLyBhcHByb3ZlQXNzZXQKYXBwcm92ZUFzc2V0XzI6CnByb3RvIDEgMQpieXRlY18wIC8vICIiCnR4biBTZW5kZXIKZ2xvYmFsIENyZWF0b3JBZGRyZXNzCj09Ci8vIHVuYXV0aG9yaXplZAphc3NlcnQKYnl0ZWMgNSAvLyAicmVxdWVzdFN0YXRlIgpwdXNoaW50IDIgLy8gMgphcHBfZ2xvYmFsX3B1dAppdHhuX2JlZ2luCnB1c2hpbnQgMyAvLyBhY2ZnCml0eG5fZmllbGQgVHlwZUVudW0KcHVzaGJ5dGVzIDB4NDk0ZTUzIC8vICJJTlMiCml0eG5fZmllbGQgQ29uZmlnQXNzZXRVbml0TmFtZQpwdXNoYnl0ZXMgMHg0OTRlNTM1NTUyNDE0ZTQzNDUgLy8gIklOU1VSQU5DRSIKaXR4bl9maWVsZCBDb25maWdBc3NldE5hbWUKaW50Y18wIC8vIDAKaXR4bl9maWVsZCBDb25maWdBc3NldERlY2ltYWxzCmludGNfMSAvLyAxCml0eG5fZmllbGQgQ29uZmlnQXNzZXRUb3RhbApwdXNoYnl0ZXMgMHg0OTZlNzM3NTcyNjE2ZTYzNjUyMDc0NmY2YjY1NmUyMDY2NmY3MjIwNjE3MzczNjU3NDNhMjAgLy8gIkluc3VyYW5jZSB0b2tlbiBmb3IgYXNzZXQ6ICIKYnl0ZWNfMyAvLyAiYXNzZXROYW1lIgphcHBfZ2xvYmFsX2dldApjb25jYXQKcHVzaGJ5dGVzIDB4MjAyZDIwNDQ2NTczNjM3MjY5NzA3NDY5NmY2ZTNhMjAgLy8gIiAtIERlc2NyaXB0aW9uOiAiCmNvbmNhdApieXRlY18yIC8vICJhc3NldERlc2MiCmFwcF9nbG9iYWxfZ2V0CmNvbmNhdApwdXNoYnl0ZXMgMHgyMDJkMjA1NjYxNmM3NTY1M2EyMDI0IC8vICIgLSBWYWx1ZTogJCIKY29uY2F0CmJ5dGVjIDQgLy8gImFzc2V0VmFsIgphcHBfZ2xvYmFsX2dldAppdG9iCmNvbmNhdAppdHhuX2ZpZWxkIE5vdGUKaXR4bl9zdWJtaXQKYnl0ZWMgNyAvLyAiYXNhSUQiCml0eG4gQ3JlYXRlZEFzc2V0SUQKYXBwX2dsb2JhbF9wdXQKcHVzaGJ5dGVzIDB4NDE3MzczNjU3NDIwNDk0NDNhMjAgLy8gIkFzc2V0IElEOiAiCml0eG4gQ3JlYXRlZEFzc2V0SUQKaXRvYgpjb25jYXQKZnJhbWVfYnVyeSAwCmZyYW1lX2RpZyAwCmxlbgppdG9iCmV4dHJhY3QgNiAwCmZyYW1lX2RpZyAwCmNvbmNhdApmcmFtZV9idXJ5IDAKcmV0c3ViCgovLyBjbGFpbUluc3VyYW5jZQpjbGFpbUluc3VyYW5jZV8zOgpwcm90byAxIDEKYnl0ZWNfMCAvLyAiIgp0eG4gU2VuZGVyCmJ5dGVjIDYgLy8gInJlcXVlc3RlciIKYXBwX2dsb2JhbF9nZXQKPT0KLy8gdW5hdXRob3JpemVkCmFzc2VydAppdHhuX2JlZ2luCnB1c2hpbnQgNCAvLyBheGZlcgppdHhuX2ZpZWxkIFR5cGVFbnVtCmZyYW1lX2RpZyAtMQp0eG5hcyBBc3NldHMKaXR4bl9maWVsZCBYZmVyQXNzZXQKdHhuIFNlbmRlcgppdHhuX2ZpZWxkIEFzc2V0UmVjZWl2ZXIKaW50Y18xIC8vIDEKaXR4bl9maWVsZCBBc3NldEFtb3VudAppdHhuX3N1Ym1pdApieXRlY18zIC8vICJhc3NldE5hbWUiCmJ5dGVjXzAgLy8gIiIKYXBwX2dsb2JhbF9wdXQKYnl0ZWNfMiAvLyAiYXNzZXREZXNjIgpieXRlY18wIC8vICIiCmFwcF9nbG9iYWxfcHV0CmJ5dGVjIDQgLy8gImFzc2V0VmFsIgppbnRjXzAgLy8gMAphcHBfZ2xvYmFsX3B1dApieXRlYyA1IC8vICJyZXF1ZXN0U3RhdGUiCmludGNfMCAvLyAwCmFwcF9nbG9iYWxfcHV0CnB1c2hieXRlcyAweDAwMTc1NDZmNmI2NTZlMjA2NDY1MjA3MzY1Njc3NTcyNmYyMDY1NmU3NjY5NjE2NDZmIC8vIDB4MDAxNzU0NmY2YjY1NmUyMDY0NjUyMDczNjU2Nzc1NzI2ZjIwNjU2ZTc2Njk2MTY0NmYKZnJhbWVfYnVyeSAwCnJldHN1YgoKLy8gaGVsbG8KaGVsbG9fNDoKcHJvdG8gMSAxCmJ5dGVjXzAgLy8gIiIKcHVzaGJ5dGVzIDB4NDg2NTZjNmM2ZjJjMjAgLy8gIkhlbGxvLCAiCmZyYW1lX2RpZyAtMQpleHRyYWN0IDIgMApjb25jYXQKZnJhbWVfYnVyeSAwCmZyYW1lX2RpZyAwCmxlbgppdG9iCmV4dHJhY3QgNiAwCmZyYW1lX2RpZyAwCmNvbmNhdApmcmFtZV9idXJ5IDAKcmV0c3ViCgovLyBjcmVhdGVBcHBfY2FzdGVyCmNyZWF0ZUFwcGNhc3Rlcl81Ogpwcm90byAwIDAKYnl0ZWNfMCAvLyAiIgppbnRjXzAgLy8gMAp0eG5hIEFwcGxpY2F0aW9uQXJncyAxCmludGNfMCAvLyAwCmdldGJ5dGUKZnJhbWVfYnVyeSAxCmZyYW1lX2RpZyAxCmNhbGxzdWIgY3JlYXRlQXBwXzAKZnJhbWVfYnVyeSAwCmJ5dGVjXzEgLy8gMHgxNTFmN2M3NQpmcmFtZV9kaWcgMApjb25jYXQKbG9nCnJldHN1YgoKLy8gcmVnaXN0ZXJBc3NldF9jYXN0ZXIKcmVnaXN0ZXJBc3NldGNhc3Rlcl82Ogpwcm90byAwIDAKYnl0ZWNfMCAvLyAiIgpkdXBuIDIKaW50Y18wIC8vIDAKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMQpmcmFtZV9idXJ5IDEKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMgpmcmFtZV9idXJ5IDIKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMwpidG9pCmZyYW1lX2J1cnkgMwpmcmFtZV9kaWcgMQpmcmFtZV9kaWcgMgpmcmFtZV9kaWcgMwpjYWxsc3ViIHJlZ2lzdGVyQXNzZXRfMQpmcmFtZV9idXJ5IDAKYnl0ZWNfMSAvLyAweDE1MWY3Yzc1CmZyYW1lX2RpZyAwCmNvbmNhdApsb2cKcmV0c3ViCgovLyBhcHByb3ZlQXNzZXRfY2FzdGVyCmFwcHJvdmVBc3NldGNhc3Rlcl83Ogpwcm90byAwIDAKYnl0ZWNfMCAvLyAiIgppbnRjXzAgLy8gMAp0eG4gR3JvdXBJbmRleAppbnRjXzEgLy8gMQotCmZyYW1lX2J1cnkgMQpmcmFtZV9kaWcgMQpndHhucyBUeXBlRW51bQppbnRjXzEgLy8gcGF5Cj09CmFzc2VydApmcmFtZV9kaWcgMQpjYWxsc3ViIGFwcHJvdmVBc3NldF8yCmZyYW1lX2J1cnkgMApieXRlY18xIC8vIDB4MTUxZjdjNzUKZnJhbWVfZGlnIDAKY29uY2F0CmxvZwpyZXRzdWIKCi8vIGNsYWltSW5zdXJhbmNlX2Nhc3RlcgpjbGFpbUluc3VyYW5jZWNhc3Rlcl84Ogpwcm90byAwIDAKYnl0ZWNfMCAvLyAiIgppbnRjXzAgLy8gMAp0eG5hIEFwcGxpY2F0aW9uQXJncyAxCmludGNfMCAvLyAwCmdldGJ5dGUKZnJhbWVfYnVyeSAxCmZyYW1lX2RpZyAxCmNhbGxzdWIgY2xhaW1JbnN1cmFuY2VfMwpmcmFtZV9idXJ5IDAKYnl0ZWNfMSAvLyAweDE1MWY3Yzc1CmZyYW1lX2RpZyAwCmNvbmNhdApsb2cKcmV0c3ViCgovLyBoZWxsb19jYXN0ZXIKaGVsbG9jYXN0ZXJfOToKcHJvdG8gMCAwCmJ5dGVjXzAgLy8gIiIKZHVwCnR4bmEgQXBwbGljYXRpb25BcmdzIDEKZnJhbWVfYnVyeSAxCmZyYW1lX2RpZyAxCmNhbGxzdWIgaGVsbG9fNApmcmFtZV9idXJ5IDAKYnl0ZWNfMSAvLyAweDE1MWY3Yzc1CmZyYW1lX2RpZyAwCmNvbmNhdApsb2cKcmV0c3Vi",
        "clear": "I3ByYWdtYSB2ZXJzaW9uIDgKcHVzaGludCAwIC8vIDAKcmV0dXJu"
    },
    "state": {
        "global": {
            "num_byte_slices": 3,
            "num_uints": 3
        },
        "local": {
            "num_byte_slices": 0,
            "num_uints": 0
        }
    },
    "schema": {
        "global": {
            "declared": {
                "asaID": {
                    "type": "uint64",
                    "key": "asaID",
                    "descr": ""
                },
                "assetDesc": {
                    "type": "bytes",
                    "key": "assetDesc",
                    "descr": ""
                },
                "assetName": {
                    "type": "bytes",
                    "key": "assetName",
                    "descr": ""
                },
                "assetVal": {
                    "type": "uint64",
                    "key": "assetVal",
                    "descr": ""
                },
                "requestState": {
                    "type": "uint64",
                    "key": "requestState",
                    "descr": ""
                },
                "requester": {
                    "type": "bytes",
                    "key": "requester",
                    "descr": ""
                }
            },
            "reserved": {}
        },
        "local": {
            "declared": {},
            "reserved": {}
        }
    },
    "contract": {
        "name": "insurance",
        "methods": [
            {
                "name": "createApp",
                "args": [
                    {
                        "type": "account",
                        "name": "client"
                    }
                ],
                "returns": {
                    "type": "string"
                }
            },
            {
                "name": "registerAsset",
                "args": [
                    {
                        "type": "string",
                        "name": "name"
                    },
                    {
                        "type": "string",
                        "name": "desc"
                    },
                    {
                        "type": "uint64",
                        "name": "val"
                    }
                ],
                "returns": {
                    "type": "string"
                }
            },
            {
                "name": "approveAsset",
                "args": [
                    {
                        "type": "pay",
                        "name": "tx"
                    }
                ],
                "returns": {
                    "type": "string"
                }
            },
            {
                "name": "claimInsurance",
                "args": [
                    {
                        "type": "asset",
                        "name": "asa"
                    }
                ],
                "returns": {
                    "type": "string"
                }
            },
            {
                "name": "hello",
                "args": [
                    {
                        "type": "string",
                        "name": "name"
                    }
                ],
                "returns": {
                    "type": "string"
                }
            }
        ],
        "networks": {}
    },
    "bare_call_config": {}
}"""
APP_SPEC = algokit_utils.ApplicationSpecification.from_json(_APP_SPEC_JSON)
_TReturn = typing.TypeVar("_TReturn")


class _ArgsBase(ABC, typing.Generic[_TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ...


_TArgs = typing.TypeVar("_TArgs", bound=_ArgsBase[typing.Any])


@dataclasses.dataclass(kw_only=True)
class _TArgsHolder(typing.Generic[_TArgs]):
    args: _TArgs


@dataclasses.dataclass(kw_only=True)
class DeployCreate(algokit_utils.DeployCreateCallArgs, _TArgsHolder[_TArgs], typing.Generic[_TArgs]):
    pass


def _filter_none(value: dict | typing.Any) -> dict | typing.Any:
    if isinstance(value, dict):
        return {k: _filter_none(v) for k, v in value.items() if v is not None}
    return value


def _as_dict(data: typing.Any, *, convert_all: bool = True) -> dict[str, typing.Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    if convert_all:
        result = dataclasses.asdict(data)
    else:
        result = {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}
    return _filter_none(result)


def _convert_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.CommonCallParametersDict:
    return typing.cast(algokit_utils.CommonCallParametersDict, _as_dict(transaction_parameters))


def _convert_call_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.OnCompleteCallParametersDict:
    return typing.cast(algokit_utils.OnCompleteCallParametersDict, _as_dict(transaction_parameters))


def _convert_create_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
    on_complete: algokit_utils.OnCompleteActionName,
) -> algokit_utils.CreateCallParametersDict:
    result = typing.cast(algokit_utils.CreateCallParametersDict, _as_dict(transaction_parameters))
    on_complete_enum = on_complete.replace("_", " ").title().replace(" ", "") + "OC"
    result["on_complete"] = getattr(algosdk.transaction.OnComplete, on_complete_enum)
    return result


def _convert_deploy_args(
    deploy_args: algokit_utils.DeployCallArgs | None,
) -> algokit_utils.ABICreateCallArgsDict | None:
    if deploy_args is None:
        return None

    deploy_args_dict = typing.cast(algokit_utils.ABICreateCallArgsDict, _as_dict(deploy_args))
    if isinstance(deploy_args, _TArgsHolder):
        deploy_args_dict["args"] = _as_dict(deploy_args.args)
        deploy_args_dict["method"] = deploy_args.args.method()

    return deploy_args_dict


@dataclasses.dataclass(kw_only=True)
class RegisterAssetArgs(_ArgsBase[str]):
    name: str
    desc: str
    val: int

    @staticmethod
    def method() -> str:
        return "registerAsset(string,string,uint64)string"


@dataclasses.dataclass(kw_only=True)
class ApproveAssetArgs(_ArgsBase[str]):
    tx: TransactionWithSigner

    @staticmethod
    def method() -> str:
        return "approveAsset(pay)string"


@dataclasses.dataclass(kw_only=True)
class ClaimInsuranceArgs(_ArgsBase[str]):
    asa: int

    @staticmethod
    def method() -> str:
        return "claimInsurance(asset)string"


@dataclasses.dataclass(kw_only=True)
class HelloArgs(_ArgsBase[str]):
    name: str

    @staticmethod
    def method() -> str:
        return "hello(string)string"


@dataclasses.dataclass(kw_only=True)
class CreateAppArgs(_ArgsBase[str]):
    client: str | bytes

    @staticmethod
    def method() -> str:
        return "createApp(account)string"


class ByteReader:
    def __init__(self, data: bytes):
        self._data = data

    @property
    def as_bytes(self) -> bytes:
        return self._data

    @property
    def as_str(self) -> str:
        return self._data.decode("utf8")

    @property
    def as_base64(self) -> str:
        return base64.b64encode(self._data).decode("utf8")

    @property
    def as_hex(self) -> str:
        return self._data.hex()


class GlobalState:
    def __init__(self, data: dict[bytes, bytes | int]):
        self.asaID = typing.cast(int, data.get(b"asaID"))
        self.assetDesc = ByteReader(typing.cast(bytes, data.get(b"assetDesc")))
        self.assetName = ByteReader(typing.cast(bytes, data.get(b"assetName")))
        self.assetVal = typing.cast(int, data.get(b"assetVal"))
        self.requestState = typing.cast(int, data.get(b"requestState"))
        self.requester = ByteReader(typing.cast(bytes, data.get(b"requester")))


class Composer:

    def __init__(self, app_client: algokit_utils.ApplicationClient, atc: AtomicTransactionComposer):
        self.app_client = app_client
        self.atc = atc

    def build(self) -> AtomicTransactionComposer:
        return self.atc

    def execute(self) -> AtomicTransactionResponse:
        return self.app_client.execute_atc(self.atc)

    def register_asset(
        self,
        *,
        name: str,
        desc: str,
        val: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `registerAsset(string,string,uint64)string` ABI method
        
        :param str name: The `name` ABI parameter
        :param str desc: The `desc` ABI parameter
        :param int val: The `val` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = RegisterAssetArgs(
            name=name,
            desc=desc,
            val=val,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def approve_asset(
        self,
        *,
        tx: TransactionWithSigner,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `approveAsset(pay)string` ABI method
        
        :param TransactionWithSigner tx: The `tx` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = ApproveAssetArgs(
            tx=tx,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def claim_insurance(
        self,
        *,
        asa: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `claimInsurance(asset)string` ABI method
        
        :param int asa: The `asa` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = ClaimInsuranceArgs(
            asa=asa,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def hello(
        self,
        *,
        name: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `hello(string)string` ABI method
        
        :param str name: The `name` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = HelloArgs(
            name=name,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def create_create_app(
        self,
        *,
        client: str | bytes,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `createApp(account)string` ABI method
        
        :param str | bytes client: The `client` ABI parameter
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = CreateAppArgs(
            client=client,
        )
        self.app_client.compose_create(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
            **_as_dict(args, convert_all=True),
        )
        return self

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> "Composer":
        """Adds a call to the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass"""
    
        self.app_client.compose_clear_state(self.atc, _convert_transaction_parameters(transaction_parameters), app_args)
        return self


class InsuranceClient:
    """A class for interacting with the insurance app providing high productivity and
    strongly typed methods to deploy and call the app"""

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account | None = None,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        """
        InsuranceClient can be created with an app_id to interact with an existing application, alternatively
        it can be created with a creator and indexer_client specified to find existing applications by name and creator.
        
        :param AlgodClient algod_client: AlgoSDK algod client
        :param int app_id: The app_id of an existing application, to instead find the application by creator and name
        use the creator and indexer_client parameters
        :param str | Account creator: The address or Account of the app creator to resolve the app_id
        :param IndexerClient indexer_client: AlgoSDK indexer client, only required if deploying or finding app_id by
        creator and app name
        :param AppLookup existing_deployments:
        :param TransactionSigner | Account signer: Account or signer to use to sign transactions, if not specified and
        creator was passed as an Account will use that.
        :param str sender: Address to use as the sender for all transactions, will use the address associated with the
        signer if not specified.
        :param TemplateValueMapping template_values: Values to use for TMPL_* template variables, dictionary keys should
        *NOT* include the TMPL_ prefix
        :param str | None app_name: Name of application to use when deploying, defaults to name defined on the
        Application Specification
            """

        self.app_spec = APP_SPEC
        
        # calling full __init__ signature, so ignoring mypy warning about overloads
        self.app_client = algokit_utils.ApplicationClient(  # type: ignore[call-overload, misc]
            algod_client=algod_client,
            app_spec=self.app_spec,
            app_id=app_id,
            creator=creator,
            indexer_client=indexer_client,
            existing_deployments=existing_deployments,
            signer=signer,
            sender=sender,
            suggested_params=suggested_params,
            template_values=template_values,
            app_name=app_name,
        )

    @property
    def algod_client(self) -> algosdk.v2client.algod.AlgodClient:
        return self.app_client.algod_client

    @property
    def app_id(self) -> int:
        return self.app_client.app_id

    @app_id.setter
    def app_id(self, value: int) -> None:
        self.app_client.app_id = value

    @property
    def app_address(self) -> str:
        return self.app_client.app_address

    @property
    def sender(self) -> str | None:
        return self.app_client.sender

    @sender.setter
    def sender(self, value: str) -> None:
        self.app_client.sender = value

    @property
    def signer(self) -> TransactionSigner | None:
        return self.app_client.signer

    @signer.setter
    def signer(self, value: TransactionSigner) -> None:
        self.app_client.signer = value

    @property
    def suggested_params(self) -> algosdk.transaction.SuggestedParams | None:
        return self.app_client.suggested_params

    @suggested_params.setter
    def suggested_params(self, value: algosdk.transaction.SuggestedParams | None) -> None:
        self.app_client.suggested_params = value

    def get_global_state(self) -> GlobalState:
        """Returns the application's global state wrapped in a strongly typed class with options to format the stored value"""

        state = typing.cast(dict[bytes, bytes | int], self.app_client.get_global_state(raw=True))
        return GlobalState(state)

    def register_asset(
        self,
        *,
        name: str,
        desc: str,
        val: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Calls `registerAsset(string,string,uint64)string` ABI method
        
        :param str name: The `name` ABI parameter
        :param str desc: The `desc` ABI parameter
        :param int val: The `val` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[str]: The result of the transaction"""

        args = RegisterAssetArgs(
            name=name,
            desc=desc,
            val=val,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def approve_asset(
        self,
        *,
        tx: TransactionWithSigner,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Calls `approveAsset(pay)string` ABI method
        
        :param TransactionWithSigner tx: The `tx` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[str]: The result of the transaction"""

        args = ApproveAssetArgs(
            tx=tx,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def claim_insurance(
        self,
        *,
        asa: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Calls `claimInsurance(asset)string` ABI method
        
        :param int asa: The `asa` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[str]: The result of the transaction"""

        args = ClaimInsuranceArgs(
            asa=asa,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def hello(
        self,
        *,
        name: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Calls `hello(string)string` ABI method
        
        :param str name: The `name` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[str]: The result of the transaction"""

        args = HelloArgs(
            name=name,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def create_create_app(
        self,
        *,
        client: str | bytes,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Calls `createApp(account)string` ABI method
        
        :param str | bytes client: The `client` ABI parameter
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[str]: The result of the transaction"""

        args = CreateAppArgs(
            client=client,
        )
        result = self.app_client.create(
            call_abi_method=args.method(),
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
            **_as_dict(args, convert_all=True),
        )
        return result

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Calls the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass
        :returns algokit_utils.TransactionResponse: The result of the transaction"""
    
        return self.app_client.clear_state(_convert_transaction_parameters(transaction_parameters), app_args)

    def deploy(
        self,
        version: str | None = None,
        *,
        signer: TransactionSigner | None = None,
        sender: str | None = None,
        allow_update: bool | None = None,
        allow_delete: bool | None = None,
        on_update: algokit_utils.OnUpdate = algokit_utils.OnUpdate.Fail,
        on_schema_break: algokit_utils.OnSchemaBreak = algokit_utils.OnSchemaBreak.Fail,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        create_args: DeployCreate[CreateAppArgs],
        update_args: algokit_utils.DeployCallArgs | None = None,
        delete_args: algokit_utils.DeployCallArgs | None = None,
    ) -> algokit_utils.DeployResponse:
        """Deploy an application and update client to reference it.
        
        Idempotently deploy (create, update/delete if changed) an app against the given name via the given creator
        account, including deploy-time template placeholder substitutions.
        To understand the architecture decisions behind this functionality please see
        <https://github.com/algorandfoundation/algokit-cli/blob/main/docs/architecture-decisions/2023-01-12_smart-contract-deployment.md>
        
        ```{note}
        If there is a breaking state schema change to an existing app (and `on_schema_break` is set to
        'ReplaceApp' the existing app will be deleted and re-created.
        ```
        
        ```{note}
        If there is an update (different TEAL code) to an existing app (and `on_update` is set to 'ReplaceApp')
        the existing app will be deleted and re-created.
        ```
        
        :param str version: version to use when creating or updating app, if None version will be auto incremented
        :param algosdk.atomic_transaction_composer.TransactionSigner signer: signer to use when deploying app
        , if None uses self.signer
        :param str sender: sender address to use when deploying app, if None uses self.sender
        :param bool allow_delete: Used to set the `TMPL_DELETABLE` template variable to conditionally control if an app
        can be deleted
        :param bool allow_update: Used to set the `TMPL_UPDATABLE` template variable to conditionally control if an app
        can be updated
        :param OnUpdate on_update: Determines what action to take if an application update is required
        :param OnSchemaBreak on_schema_break: Determines what action to take if an application schema requirements
        has increased beyond the current allocation
        :param dict[str, int|str|bytes] template_values: Values to use for `TMPL_*` template variables, dictionary keys
        should *NOT* include the TMPL_ prefix
        :param DeployCreate[CreateAppArgs] create_args: Arguments used when creating an application
        :param algokit_utils.DeployCallArgs | None update_args: Arguments used when updating an application
        :param algokit_utils.DeployCallArgs | None delete_args: Arguments used when deleting an application
        :return DeployResponse: details action taken and relevant transactions
        :raises DeploymentError: If the deployment failed"""

        return self.app_client.deploy(
            version,
            signer=signer,
            sender=sender,
            allow_update=allow_update,
            allow_delete=allow_delete,
            on_update=on_update,
            on_schema_break=on_schema_break,
            template_values=template_values,
            create_args=_convert_deploy_args(create_args),
            update_args=_convert_deploy_args(update_args),
            delete_args=_convert_deploy_args(delete_args),
        )

    def compose(self, atc: AtomicTransactionComposer | None = None) -> Composer:
        return Composer(self.app_client, atc or AtomicTransactionComposer())
