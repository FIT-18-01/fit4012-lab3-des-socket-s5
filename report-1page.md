# Report 1 page - Lab 3

## Thông tin nhóm
- Thành viên 1: Phạm Thế Đức
- Thành viên 2: Claude

## Mục tiêu
Bài lab xây dựng hệ thống truyền tin bảo mật giữa hai tiến trình qua TCP socket, trong đó bản tin được mã hoá bằng thuật toán DES chế độ CBC trước khi gửi. Mục tiêu cụ thể gồm: (1) hiểu cơ chế mã hoá đối xứng DES-CBC và padding PKCS#7; (2) thiết kế giao thức packet với header cố định chứa key, IV và độ dài ciphertext; (3) đảm bảo tính toàn vẹn khi nhận — phát hiện được khi ciphertext bị giả mạo hoặc sai key; (4) viết bộ kiểm thử tự động bao phủ cả trường hợp bình thường lẫn tấn công.

## Phân công thực hiện
- **Phạm Thế Đức**: xây dựng `sender.py` và `receiver.py` — logic kết nối socket, gửi/nhận packet, đọc biến môi trường, ghi log file.
- **Claude**: xây dựng `des_socket_utils.py` — các hàm `pad/unpad`, `encrypt_des_cbc`, `decrypt_des_cbc`, `build_packet`, `parse_header`, `recv_exact`, hằng số `HEADER_SIZE`.
- **Làm chung**: thiết kế cấu trúc packet (key 8B | IV 8B | length 4B | ciphertext), bộ test 5 file trong `tests/`, review chéo và sửa lỗi.

## Cách làm
**Sender** đọc bản tin từ stdin hoặc biến môi trường `MESSAGE`, gọi `encrypt_des_cbc()` để sinh key/IV ngẫu nhiên và mã hoá bằng DES-CBC + PKCS#7, đóng gói thành packet 20-byte header + ciphertext rồi `sendall()` qua TCP.  
**Receiver** bind/listen trên cổng cấu hình, sau `accept()` đọc đúng 20 byte header bằng `recv_exact()` để lấy key, IV, độ dài ciphertext; đọc tiếp đúng `length` byte ciphertext; gọi `decrypt_des_cbc()` và in bản rõ ra màn hình.  
**Kiểm thử**: 5 file pytest — kiểm tra pad/unpad round-trip, cấu trúc packet, integration test sender↔receiver qua subprocess, kiểm tra ciphertext bị tamper và sai key đều không khôi phục được bản rõ gốc.

## Kết quả
Tất cả 6 ca kiểm thử pass (`pytest tests/ -v`):
- `test_pad_unpad_roundtrip` — PASSED
- `test_build_packet_contains_correct_length` — PASSED
- `test_protocol_contract_order_is_key_iv_length_ciphertext` — PASSED
- `test_local_sender_receiver_roundtrip` — PASSED (bản tin `"Xin chao FIT4012 - local integration test"` được khôi phục nguyên vẹn)
- `test_tampered_ciphertext_should_fail_or_change_plaintext` — PASSED
- `test_wrong_key_should_not_recover_original_plaintext` — PASSED

## Kết luận
**Kỹ thuật**: Cần đọc socket theo vòng lặp (`recv_exact`) thay vì một lần `recv` vì TCP có thể phân mảnh dữ liệu; timeout phải set trên cả connection socket, không chỉ server socket. Chuỗi Unicode trong subprocess trên Windows yêu cầu tường minh `encoding='utf-8'` cả phía ghi lẫn đọc.  
**Bảo mật**: DES với key 56-bit hiện đã lỗi thời và dễ bị brute-force; key và IV được truyền plaintext trong header — kẻ tấn công nghe lén mạng có thể giải mã toàn bộ bản tin. Hệ thống thực tế cần dùng AES-256 và trao đổi key qua kênh bảo mật (TLS/ECDH).
