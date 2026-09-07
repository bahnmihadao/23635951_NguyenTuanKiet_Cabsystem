# CAB System API – hướng dẫn sử dụng

- Chạy local bằng Docker: xem [DOCKER.md](DOCKER.md). Từ thư mục gốc chạy `docker compose -f api-document/compose.yaml up -d`, rồi mở http://localhost:8081.
- File chính: `openapi.yaml` (OpenAPI 3.0.3).
- Đây là hợp đồng API đề xuất từ README, chưa phải backend đã triển khai.
- Mở https://editor.swagger.io/ và import file YAML để đọc tài liệu.
- Khi có backend, sửa `servers.url`, đăng nhập lấy token rồi dùng Authorize để gọi thử.
- Các mục chưa chốt, giới hạn đồ án và quy tắc dùng chung nằm trong `info.description`.
- `x-readme-fr`, `x-readme-use-cases` và `x-readme-business-rules` dùng đối chiếu yêu cầu.
- `build_openapi.py` là nguồn sinh file; sửa nguồn rồi chạy lại nếu muốn duy trì tự động. PyYAML là tùy chọn khi sinh, giúp định dạng dễ đọc.
- `validate_openapi.py` cần PyYAML và openapi-spec-validator; kiểm tra chuẩn, tham chiếu, operationId, path parameters và độ phủ mã yêu cầu.

Đã kiểm tra: 81 thao tác trên 71 đường dẫn; 54 FR và 16 UC có trong README. Bao phủ UC001–UC016; tác vụ tự động như điều phối và phát thông báo được mô tả ở các API kích hoạt và truy vấn liên quan.

## Ma trận yêu cầu → API

| Yêu cầu | API |
|---|---|
| FR01.1 | `POST /auth/registrations`<br>`POST /auth/registrations/verify` |
| FR01.2 | `POST /auth/login` |
| FR01.3 | `GET /users/me`<br>`PATCH /users/me` |
| FR01.4 | `POST /auth/registrations`<br>`GET /drivers/me/profile`<br>`PUT /drivers/me/profile`<br>`POST /documents`<br>`GET /documents/{documentId}` |
| FR01.5 | `GET /drivers/me/vehicle`<br>`PUT /drivers/me/vehicle`<br>`POST /documents` |
| FR02.1 | `GET /places`<br>`POST /routes` |
| FR02.2 | `GET /places`<br>`POST /routes` |
| FR02.3 | `GET /vehicle-types` |
| FR02.4 | `POST /trips` |
| FR02.5 | `GET /trips`<br>`GET /trips/{tripId}` |
| FR03.1 | `PUT /drivers/me/availability`<br>`POST /drivers/me/locations`<br>`POST /trips` |
| FR03.2 | `POST /drivers/me/locations`<br>`POST /trips` |
| FR03.3 | `POST /trips`<br>`GET /drivers/me/offers` |
| FR03.4 | `POST /drivers/me/offers/{offerId}/accept` |
| FR03.5 | `POST /drivers/me/offers/{offerId}/reject` |
| FR03.6 | `POST /trips`<br>`GET /drivers/me/offers`<br>`POST /drivers/me/offers/{offerId}/reject` |
| FR03.7 | `POST /trips` |
| FR04.1 | `POST /drivers/me/offers/{offerId}/accept` |
| FR04.2 | `POST /trips/{tripId}/status-transitions` |
| FR04.3 | `POST /trips/{tripId}/status-transitions` |
| FR04.4 | `POST /trips/{tripId}/status-transitions` |
| FR04.5 | `POST /trips/{tripId}/status-transitions` |
| FR04.6 | `GET /trips/{tripId}`<br>`GET /trips/{tripId}/tracking`<br>`GET /trips/{tripId}/events` |
| FR04.7 | `POST /drivers/me/locations`<br>`GET /trips/{tripId}/tracking`<br>`GET /admin/trips/{tripId}/locations` |
| FR05.1 | `POST /trips/{tripId}/status-transitions`<br>`GET /trips/{tripId}/fare` |
| FR05.2 | `POST /fare-estimates`<br>`POST /trips/{tripId}/status-transitions`<br>`GET /trips/{tripId}/fare` |
| FR06.1 | `POST /trips/{tripId}/payments`<br>`POST /payments/{paymentId}/confirm-cash` |
| FR06.2 | `POST /trips/{tripId}/payments` |
| FR06.3 | `GET /payments/{paymentId}`<br>`POST /integrations/payments/callback` |
| FR06.4 | `POST /integrations/payments/callback` |
| FR06.5 | `POST /trips/{tripId}/payments` |
| FR06.6 | `POST /trips/{tripId}/payments`<br>`GET /trips/{tripId}/payments`<br>`GET /payments/{paymentId}`<br>`POST /integrations/payments/callback`<br>`GET /admin/payments` |
| FR07.1 | `POST /trips`<br>`GET /notifications`<br>`POST /devices` |
| FR07.2 | `POST /drivers/me/offers/{offerId}/accept`<br>`GET /notifications` |
| FR07.3 | `POST /trips/{tripId}/status-transitions`<br>`GET /notifications` |
| FR07.4 | `POST /trips/{tripId}/status-transitions`<br>`GET /notifications` |
| FR07.5 | `POST /payments/{paymentId}/confirm-cash`<br>`POST /integrations/payments/callback`<br>`GET /notifications` |
| FR07.6 | `POST /trips`<br>`GET /notifications`<br>`POST /devices` |
| FR07.7 | `POST /trips/{tripId}/cancel`<br>`GET /notifications`<br>`POST /notifications/{notificationId}/read` |
| FR08.1 | `GET /admin/users`<br>`POST /admin/users`<br>`GET /admin/users/{userId}`<br>`PATCH /admin/users/{userId}`<br>`PUT /admin/users/{userId}/status` |
| FR08.2 | `GET /documents/{documentId}`<br>`POST /admin/users`<br>`PATCH /admin/users/{userId}`<br>`GET /admin/drivers`<br>`GET /admin/drivers/{driverId}`<br>`PUT /admin/users/{userId}/status`<br>`PUT /admin/drivers/{driverId}/profile`<br>`POST /admin/drivers/{driverId}/review` |
| FR08.3 | `POST /documents`<br>`GET /documents/{documentId}`<br>`GET /admin/vehicles`<br>`POST /admin/vehicles`<br>`GET /admin/vehicles/{vehicleId}`<br>`PUT /admin/vehicles/{vehicleId}`<br>`POST /admin/vehicles/{vehicleId}/review` |
| FR08.4 | `GET /admin/trips`<br>`GET /admin/trips/{tripId}` |
| FR08.5 | `GET /admin/trips/{tripId}/tracking` |
| FR08.6 | `PUT /drivers/me/availability`<br>`GET /admin/drivers` |
| FR08.7 | `POST /trips/{tripId}/incidents`<br>`GET /admin/trips/{tripId}/events`<br>`GET /admin/trips/{tripId}/locations`<br>`GET /admin/payments`<br>`GET /admin/incidents`<br>`GET /admin/incidents/{incidentId}`<br>`POST /admin/trips/{tripId}/incidents`<br>`POST /admin/incidents/{incidentId}/interventions` |
| FR09.1 | `GET /admin/reports/summary` |
| FR09.2 | `GET /admin/reports/summary` |
| FR09.3 | `GET /admin/reports/summary` |
| FR09.4 | `GET /admin/reports/summary` |
| FR09.5 | `GET /admin/reports/summary` |
| FR10.1 | `POST /auth/registrations`<br>`POST /auth/registrations/verify`<br>`POST /auth/login`<br>`POST /auth/logout`<br>`PUT /admin/users/{userId}/status` |
| FR10.2 | `POST /admin/incidents/{incidentId}/interventions`<br>`POST /admin/interventions/{interventionId}/decision`<br>`GET /users/me/permissions`<br>`GET /admin/roles` |
| FR10.3 | `PUT /admin/users/{userId}/status`<br>`POST /admin/incidents/{incidentId}/interventions`<br>`POST /admin/interventions/{interventionId}/decision`<br>`GET /admin/audit-logs` |
| UC001 | `POST /auth/login` |
| UC002 | `POST /auth/registrations`<br>`POST /auth/registrations/verify`<br>`POST /auth/registrations/resend-otp` |
| UC003 | `GET /vehicle-types`<br>`GET /places`<br>`POST /routes`<br>`POST /fare-estimates`<br>`POST /trips`<br>`POST /trips/{tripId}/cancel` |
| UC004 | `POST /trips`<br>`GET /drivers/me/offers`<br>`POST /drivers/me/offers/{offerId}/accept` |
| UC005 | `GET /drivers/me/offers`<br>`GET /notifications`<br>`POST /notifications/{notificationId}/read`<br>`POST /devices`<br>`POST /notifications/{notificationId}/received` |
| UC006 | `GET /drivers/me/offers`<br>`POST /drivers/me/offers/{offerId}/accept`<br>`POST /drivers/me/offers/{offerId}/reject` |
| UC007 | `POST /drivers/me/offers/{offerId}/accept`<br>`POST /drivers/me/offers/{offerId}/reject` |
| UC008 | `POST /trips/{tripId}/status-transitions`<br>`POST /trips/{tripId}/cancel` |
| UC009 | `GET /trips`<br>`GET /trips/{tripId}`<br>`GET /trips/{tripId}/tracking`<br>`GET /trips/{tripId}/events`<br>`POST /trips/{tripId}/cancel` |
| UC010 | `GET /trips/{tripId}/fare`<br>`POST /trips/{tripId}/payments`<br>`GET /trips/{tripId}/payments`<br>`POST /payments/{paymentId}/confirm-cash` |
| UC011 | `POST /trips/{tripId}/payments`<br>`GET /trips/{tripId}/payments`<br>`GET /payments/{paymentId}`<br>`POST /integrations/payments/callback` |
| UC012 | `GET /trips`<br>`GET /rating-options`<br>`POST /trips/{tripId}/rating`<br>`GET /trips/{tripId}/rating` |
| UC013 | `POST /auth/invitations/activate`<br>`GET /admin/users`<br>`POST /admin/users`<br>`GET /admin/users/{userId}`<br>`PATCH /admin/users/{userId}`<br>`GET /admin/drivers`<br>`GET /admin/drivers/{driverId}`<br>`GET /admin/vehicles`<br>`POST /admin/vehicles`<br>`GET /admin/vehicles/{vehicleId}`<br>`PUT /admin/vehicles/{vehicleId}`<br>`PUT /admin/users/{userId}/status`<br>`PUT /admin/drivers/{driverId}/profile`<br>`POST /admin/drivers/{driverId}/review`<br>`POST /admin/vehicles/{vehicleId}/review`<br>`GET /admin/audit-logs` |
| UC014 | `GET /admin/trips`<br>`GET /admin/trips/{tripId}`<br>`GET /admin/trips/{tripId}/tracking`<br>`POST /admin/trips/{tripId}/incidents` |
| UC015 | `POST /trips/{tripId}/incidents`<br>`GET /admin/trips/{tripId}/events`<br>`GET /admin/trips/{tripId}/locations`<br>`GET /admin/payments`<br>`GET /admin/payments/{paymentId}/refunds`<br>`GET /admin/incidents`<br>`GET /admin/incidents/{incidentId}`<br>`POST /admin/trips/{tripId}/incidents`<br>`POST /admin/incidents/{incidentId}/interventions`<br>`GET /admin/interventions/{interventionId}`<br>`GET /admin/interventions`<br>`POST /admin/interventions/{interventionId}/decision`<br>`GET /admin/audit-logs` |
| UC016 | `GET /regions`<br>`GET /admin/reports/summary`<br>`POST /admin/reports/exports`<br>`GET /admin/reports/exports/{exportId}`<br>`GET /admin/reports/exports/{exportId}/file` |
