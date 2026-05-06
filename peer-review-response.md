# Peer Review Response

## Thông tin nhóm
- Thành viên 1: Phạm Thế Đức
- Thành viên 2: Claude

## Thành viên 1 góp ý cho thành viên 2
Phần `des_socket_utils.py` có cấu trúc rõ ràng, docstring đầy đủ, tuy nhiên thiếu khai báo `HEADER_SIZE` và hàm `recv_exact` mà `receiver.py` cần import — gây `ImportError` ngay khi khởi động. Bộ test bao phủ tốt các trường hợp cơ bản (pad/unpad, header, tamper, wrong key) nhưng chưa kiểm tra trường hợp header không đủ byte hoặc kết nối đóng giữa chừng.

## Thành viên 2 góp ý cho thành viên 1
`receiver.py` và `sender.py` logic mạch lạc, dễ đọc. Tuy nhiên `s.settimeout(TIMEOUT)` chỉ áp dụng cho server socket, không áp cho connection socket `conn` trả về từ `accept()` — khiến `recv_exact(conn, ...)` có thể block vô hạn nếu sender gửi thiếu dữ liệu. Ngoài ra `errors='ignore'` trong `plaintext.decode()` che giấu lỗi giải mã sai key thay vì báo lỗi rõ ràng.

## Nhóm đã sửa gì sau góp ý
- Thêm `HEADER_SIZE = 20` và hàm `recv_exact()` vào `des_socket_utils.py` để `receiver.py` import được.
- Thêm `conn.settimeout(TIMEOUT)` trong `receiver.py` ngay sau `accept()` để connection socket cũng có timeout.
- Bỏ `errors='ignore'` trong `plaintext.decode()` để lỗi giải mã sai key được raise rõ ràng thay vì trả về chuỗi rác.
- Thêm `PYTHONIOENCODING=utf-8` vào môi trường subprocess và `encoding='utf-8'` vào `Popen` trong test để fix lỗi encode tiếng Việt trên Windows (cp1252).
