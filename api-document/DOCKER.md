# Chạy tài liệu API bằng Docker

Máy cần cài Docker Desktop và bật Linux containers. Mở Docker Desktop, chờ engine sẵn sàng.

Từ terminal ở thư mục gốc dự án, chạy:

```powershell
docker compose -f api-document/compose.yaml up -d
```

Mở http://localhost:8081 để xem Swagger UI. Lần đầu cần Internet để tải image.
File `openapi.yaml` được mount chỉ đọc; không cần copy hoặc import bằng tay.

Sau khi sửa YAML, khởi động lại container để Swagger UI nạp bản mới:

```powershell
docker compose -f api-document/compose.yaml restart
```

Sau đó tải lại trình duyệt bằng Ctrl+F5.

Xem trạng thái và log:

```powershell
docker compose -f api-document/compose.yaml ps
docker compose -f api-document/compose.yaml logs --tail 50
```

Dừng và gỡ container (giữ nguyên YAML trên máy):

```powershell
docker compose -f api-document/compose.yaml down
```

Nếu cổng 8081 bị chiếm, đổi `127.0.0.1:8081:8080` trong compose.yaml thành
`127.0.0.1:8082:8080`, chạy lại lệnh up rồi mở http://localhost:8082.

## Tài liệu và backend

Container này chạy trang tài liệu, không tự triển khai 81 API trong YAML.
Nút **Try it out / Execute** chỉ hoạt động khi backend thực sự chạy.
Backend dự kiến trong YAML là `http://localhost:8080/api/v1`.
Request được gửi từ trình duyệt trên máy, nên `localhost:8080` trỏ đến máy của bạn.
Khi có backend, cho phép CORS từ `http://localhost:8081` và các header/phương thức cần dùng,
bao gồm Authorization, Content-Type và Idempotency-Key.

Image dùng tag `latest` cho tiện khởi động; khi cần tái lập đúng phiên bản, ghim tag hoặc digest đã kiểm thử.

Nguồn cấu hình image và SWAGGER_JSON: https://swagger.io/docs/open-source-tools/swagger-ui/usage/installation/
