import os
import socket
import struct
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad as _pad, unpad as _unpad

BLOCK_SIZE = 8   # DES block size = 8 bytes
HEADER_SIZE = 20  # key(8) + iv(8) + length(4)


def recv_exact(sock: socket.socket, n: int) -> bytes:
    """Nhận đúng n byte từ socket, raise ConnectionError nếu kết nối đóng sớm."""
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError(f"Socket đóng sớm: nhận {len(data)}/{n} byte.")
        data += chunk
    return data


def pad(data: bytes) -> bytes:
    return _pad(data, BLOCK_SIZE)


def unpad(data: bytes) -> bytes:
    return _unpad(data, BLOCK_SIZE)


def encrypt_des_cbc(
    plaintext: bytes,
    key: bytes | None = None,
    iv: bytes | None = None,
) -> tuple[bytes, bytes, bytes]:
    if key is None:
        key = os.urandom(8)
    if iv is None:
        iv = os.urandom(8)

    if len(key) != 8:
        raise ValueError("DES key phải đúng 8 byte.")
    if len(iv) != 8:
        raise ValueError("IV phải đúng 8 byte.")

    cipher = DES.new(key, DES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext))
    return key, iv, ciphertext


def decrypt_des_cbc(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    if len(key) != 8:
        raise ValueError("DES key phải đúng 8 byte.")
    if len(iv) != 8:
        raise ValueError("IV phải đúng 8 byte.")
    if len(ciphertext) % 8 != 0:
        raise ValueError("Ciphertext phải là bội số của 8 byte.")

    cipher = DES.new(key, DES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext))


def build_packet(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    length = len(ciphertext)
    header = key + iv + struct.pack(">I", length)   # >I = unsigned int big-endian
    return header + ciphertext


def parse_header(header: bytes) -> tuple[bytes, bytes, int]:
    if len(header) < 20:
        raise ValueError("Header phải có ít nhất 20 byte.")
    key = header[:8]
    iv = header[8:16]
    length = struct.unpack(">I", header[16:20])[0]
    return key, iv, length