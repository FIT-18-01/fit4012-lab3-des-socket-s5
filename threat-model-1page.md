# Threat Model - Lab 3

## Thông tin nhóm
- Thành viên 1: Phạm Thế Đức
- Thành viên 2: Claude

## Assets
- **Bản tin gốc (plaintext)**: nội dung cần truyền bí mật giữa sender và receiver.
- **DES key (8 byte)**: bí mật dùng để mã hoá/giải mã — lộ key đồng nghĩa với lộ toàn bộ bản tin.
- **IV (8 byte)**: kết hợp với key để tạo ciphertext; nếu IV bị tái sử dụng sẽ để lộ pattern bản rõ.
- **Tính toàn vẹn của ciphertext**: đảm bảo bản tin nhận được không bị sửa đổi trên đường truyền.

## Attacker model
Kẻ tấn công có khả năng **nghe lén mạng nội bộ** (passive eavesdropper) hoặc **chặn và sửa gói tin** (active man-in-the-middle) trên đường truyền TCP giữa sender và receiver. Kẻ tấn công biết giao thức (cấu trúc packet: key | IV | length | ciphertext) nhưng không có quyền truy cập trực tiếp vào máy sender hoặc receiver. Kẻ tấn công có thể thực hiện brute-force offline nếu thu thập được ciphertext.

## Threats
1. **Lộ key qua plaintext header**: key và IV được gửi rõ (không mã hoá) trong 16 byte đầu của packet — kẻ nghe lén mạng đọc được key và có thể giải mã toàn bộ bản tin ngay lập tức.
2. **Brute-force DES key**: không gian key DES chỉ 56-bit (~7.2×10¹⁶ giá trị) — đã bị phá hoàn toàn từ 1998; kẻ tấn công có thể khôi phục key trong vài giờ bằng phần cứng chuyên dụng.
3. **Giả mạo ciphertext (bit-flipping)**: DES-CBC không có MAC — kẻ tấn công có thể lật bit trong ciphertext, làm thay đổi có kiểm soát một phần bản rõ mà receiver không phát hiện được (ngoài lỗi PKCS#7 padding).
4. **Tấn công replay**: kẻ tấn công ghi lại packet hợp lệ và gửi lại — receiver sẽ chấp nhận và giải mã thành công vì không có cơ chế nonce hay timestamp.

## Mitigations
1. **Thay DES bằng AES-256-GCM**: AES-256 có không gian key 2²⁵⁶, miễn nhiễm brute-force; chế độ GCM cung cấp tích hợp xác thực (AEAD) — loại bỏ đồng thời mối đe doạ 2 và 3.
2. **Trao đổi key qua kênh bảo mật (TLS/ECDH)**: không truyền key/IV plaintext trong packet; thay bằng handshake Diffie-Hellman hoặc bọc toàn bộ kết nối trong TLS — loại bỏ mối đe doạ 1.
3. **Thêm MAC hoặc dùng AEAD**: gắn HMAC-SHA256 vào cuối mỗi packet; receiver kiểm tra MAC trước khi giải mã — phát hiện giả mạo ciphertext và tấn công replay (kết hợp với nonce/sequence number).

## Residual risks
Ngay cả khi áp dụng AES-256-GCM và TLS, hệ thống vẫn còn rủi ro **tấn công vào endpoint**: nếu kẻ tấn công có quyền truy cập máy sender hoặc receiver (malware, physical access), key có thể bị lấy từ bộ nhớ tiến trình (process memory dumping), vô hiệu hoá mọi biện pháp mã hoá trên đường truyền. Cần kết hợp thêm hardware security module (HSM) hoặc secure enclave để bảo vệ key tại chỗ lưu trữ.
