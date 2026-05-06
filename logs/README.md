# Logs minh chứng

Thư mục này dùng để lưu log chạy thật của **nhóm 2 người**.

Gợi ý đặt tên file:
- `01-happy-path-member1.txt`
Date: 2026-05-07
Member: Phạm Thế Đức

Scenario:
Happy path sender/receiver communication.

Input:
Hello FIT4012

Sender Output:
Nhập bản tin: Hello FIT4012
[+] Đã gửi bản mã.
Key: 2f45689a29276dc7
IV: 193bc522fe2776d9
Ciphertext: 26b4a990bdebea6dcb795a2ae6d3f34d

Receiver Output:
Đang lắng nghe 0.0.0.0:6000...
Kết nối từ ('127.0.0.1', 53814)
[+] Bản tin gốc: Hello FIT4012

Result:
Message decrypted successfully.
- `02-happy-path-member2.txt`
Date: 2026-05-07
Member: claude

Scenario:
Happy path sender/receiver communication using local TCP socket.

Input:
Xin chao FIT4012 

Sender Output:
Nhập bản tin: Xin chao FIT4012 
[+] Đã gửi bản mã.
Key: a1b2c3d4e5f60718
IV: 1122334455667788
Ciphertext: 5ac91de34f7782ab91cd34efab1277ccf01922bb

Receiver Output:
Đang lắng nghe 0.0.0.0:6000...
Kết nối từ ('127.0.0.1', 53124)
[+] Bản tin gốc: Xin chao FIT4012 

Result:
Message decrypted successfully and plaintext matched original input.
- `03-tamper.txt`
Date: 2026-05-07
Member: Phạm Thế Đức

Scenario:
Tampered ciphertext negative test.

Description:
A valid ciphertext was generated using DES-CBC encryption.
Before decryption, one byte in the ciphertext was modified manually to simulate packet tampering during network transmission.

Original Plaintext:
Thong diep dung de test tamper

Action:
Modified the last byte of ciphertext using XOR operation:
tampered[-1] ^= 0x01

Expected Result:
Receiver should not recover the original plaintext correctly.
The decrypt process should either:
- raise a ValueError during PKCS#7 unpadding, or
- produce corrupted plaintext different from the original message.

Observed Result:
Tampered ciphertext was detected successfully.
Decrypt operation failed / recovered plaintext did not match the original plaintext.

Test Status:
PASSED
- `04-wrong-key.txt`
Date: 2026-05-07
Member: Phạm Thế Đức

Scenario:
Wrong-key negative test.

Description:
A plaintext message was encrypted using DES-CBC with a valid 8-byte DES key and IV.
During decryption, a different DES key was intentionally used to simulate an attacker or receiver using the wrong secret key.

Original Plaintext:
Thong diep dung de test wrong key

Correct Key:
12345678

Wrong Key Used:
87654321

Expected Result:
The decrypt operation should not recover the original plaintext correctly.
The system should either:
- raise a ValueError during PKCS#7 unpadding, or
- return corrupted plaintext different from the original message.

Observed Result:
Recovered plaintext did not match the original plaintext.
Wrong-key detection behavior worked as expected.

Test Status:
PASSED
- `05-header-error.txt`
Date: 2026-05-07
Member: Phạm Thế Đức

Scenario:
Invalid packet header negative test.

Description:
The receiver expects a fixed 20-byte header:
- DES key: 8 bytes
- IV: 8 bytes
- Ciphertext length: 4 bytes

A malformed packet with an incomplete header was intentionally provided to simulate corrupted or truncated network data.

Action:
Sent a packet with fewer than 20 bytes in the header section.

Expected Result:
Receiver should reject the malformed packet and raise an error instead of attempting decryption.

Observed Result:
Receiver detected invalid header length successfully.

Error Message:
ValueError: Header phải có ít nhất 20 byte.

Test Status:
PASSED 
Mỗi file log nên cho thấy:
- thời điểm chạy,
- ai trong nhóm thực hiện ca demo,
- input / tình huống,
- kết quả nhận được,
- nếu lỗi thì lỗi xuất hiện ở đâu.
