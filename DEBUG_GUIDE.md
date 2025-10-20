# 🐛 HƯỚNG DẪN SỬ DỤNG DEBUG LOGGING

**Ngày:** 13/10/2025  
**Tác giả:** Cline AI Assistant

---

## ✅ ĐÃ HOÀN TẤT

Debug logging đã được thêm trực tiếp vào `telegram_bot.py` cho hai lệnh quan trọng:
- **`/gauge`** - Tạo biểu đồ gauge (9 bước)
- **`/report`** - Tạo báo cáo đầy đủ (12 bước)

---

## 📊 DEBUG LOGGING CHO `/gauge`

### Các bước được log:

```
Step 1: Fetching data (7 records)...
Step 2: Data fetched successfully
Step 3: Creating gauge chart, saving to: [filename]
Step 4: Gauge created successfully
Step 5: File verified - exists, size=[X] bytes
Step 6: Opening file to send...
Step 7: Sending photo to Telegram...
Step 8: Photo sent successfully
Step 9: Removing temp file...
```

### Ý nghĩa:
- **Step 1-2:** Lấy dữ liệu từ API
- **Step 3-4:** Tạo biểu đồ gauge
- **Step 5:** Kiểm tra file đã tạo thành công chưa
- **Step 6-8:** Gửi ảnh lên Telegram
- **Step 9:** Xóa file tạm

---

## 📈 DEBUG LOGGING CHO `/report`

### Các bước được log:

```
Step 1: Fetching data (90 records)...
Step 2: Data fetched successfully
Step 3: Creating full report, saving to: [filename]
This may take 10-30 seconds...
Step 4: Report created in [X.XX] seconds
Step 5: Report file verified - exists, size=[X] bytes
Step 6: Saving CSV data...
Step 7: CSV saved successfully
Step 8: Sending report photo to Telegram...
Step 9: Report photo sent successfully
Step 10: Sending CSV document...
Step 11: CSV document sent successfully
Step 12: Removing temp files...
```

### Ý nghĩa:
- **Step 1-2:** Lấy dữ liệu 90 ngày từ API
- **Step 3-5:** Tạo báo cáo đầy đủ (có timing)
- **Step 6-7:** Lưu dữ liệu CSV
- **Step 8-9:** Gửi ảnh báo cáo lên Telegram
- **Step 10-11:** Gửi file CSV lên Telegram
- **Step 12:** Xóa các file tạm

---

## 🚀 CÁCH SỬ DỤNG

### 1. Chạy bot:
```bash
cd CHI_BAO_TAM_LY_BOT
python telegram_bot.py
```

### 2. Gửi lệnh trong Telegram:
- Gửi `/gauge` hoặc `/report` cho bot

### 3. Xem logs:
Terminal sẽ hiển thị chi tiết từng bước:

```
2025-10-13 15:10:00 - __main__ - INFO - === GAUGE COMMAND STARTED ===
2025-10-13 15:10:00 - __main__ - INFO - Step 1: Fetching data (7 records)...
2025-10-13 15:10:01 - __main__ - INFO - Step 2: Data fetched successfully
2025-10-13 15:10:01 - __main__ - INFO - Step 3: Creating gauge chart, saving to: ...
...
```

### 4. Xem log file:
```bash
type CHI_BAO_TAM_LY_BOT\logs\bot.log
```

---

## 🔍 PHÂN TÍCH LỖI

### Nếu lệnh bị treo/lỗi:

1. **Kiểm tra Step cuối cùng:**
   - Nếu dừng ở Step X → Lỗi xảy ra ở Step X

2. **Các lỗi phổ biến:**

| Step | Lỗi có thể | Giải pháp |
|------|-----------|-----------|
| 1-2 | API không phản hồi | Kiểm tra kết nối internet |
| 3-4 | Lỗi tạo biểu đồ | Kiểm tra thư viện matplotlib |
| 5 | File không tồn tại | Kiểm tra quyền ghi thư mục |
| 6-8 | Lỗi gửi Telegram | Kiểm tra bot token |
| 9 | Không xóa được file | Kiểm tra quyền xóa |

3. **Error messages:**
   - Log sẽ hiển thị `ERROR -` nếu có lỗi
   - Xem chi tiết trong exception traceback

---

## 📝 VÍ DỤ LOG THÀNH CÔNG

### Gauge command:
```
2025-10-13 15:10:00 - __main__ - INFO - === GAUGE COMMAND STARTED ===
2025-10-13 15:10:00 - __main__ - INFO - Step 1: Fetching data (7 records)...
2025-10-13 15:10:01 - __main__ - INFO - Step 2: Data fetched successfully
2025-10-13 15:10:01 - __main__ - INFO - Step 3: Creating gauge chart, saving to: outputs/gauges/gauge_20251013_151001.png
2025-10-13 15:10:03 - __main__ - INFO - Step 4: Gauge created successfully
2025-10-13 15:10:03 - __main__ - INFO - Step 5: File verified - exists, size=45678 bytes
2025-10-13 15:10:03 - __main__ - INFO - Step 6: Opening file to send...
2025-10-13 15:10:03 - __main__ - INFO - Step 7: Sending photo to Telegram...
2025-10-13 15:10:05 - __main__ - INFO - Step 8: Photo sent successfully
2025-10-13 15:10:05 - __main__ - INFO - Step 9: Removing temp file...
2025-10-13 15:10:05 - __main__ - INFO - === GAUGE COMMAND COMPLETED ===
```

### Report command:
```
2025-10-13 15:15:00 - __main__ - INFO - === REPORT COMMAND STARTED ===
2025-10-13 15:15:00 - __main__ - INFO - Step 1: Fetching data (90 records)...
2025-10-13 15:15:02 - __main__ - INFO - Step 2: Data fetched successfully
2025-10-13 15:15:02 - __main__ - INFO - Step 3: Creating full report, saving to: outputs/reports/report_20251013_151502.png
2025-10-13 15:15:02 - __main__ - INFO - This may take 10-30 seconds...
2025-10-13 15:15:18 - __main__ - INFO - Step 4: Report created in 16.23 seconds
2025-10-13 15:15:18 - __main__ - INFO - Step 5: Report file verified - exists, size=234567 bytes
2025-10-13 15:15:18 - __main__ - INFO - Step 6: Saving CSV data...
2025-10-13 15:15:18 - __main__ - INFO - Step 7: CSV saved successfully
2025-10-13 15:15:18 - __main__ - INFO - Step 8: Sending report photo to Telegram...
2025-10-13 15:15:20 - __main__ - INFO - Step 9: Report photo sent successfully
2025-10-13 15:15:20 - __main__ - INFO - Step 10: Sending CSV document...
2025-10-13 15:15:22 - __main__ - INFO - Step 11: CSV document sent successfully
2025-10-13 15:15:22 - __main__ - INFO - Step 12: Removing temp files...
2025-10-13 15:15:22 - __main__ - INFO - === REPORT COMMAND COMPLETED ===
```

---

## 🎯 LỢI ÍCH

### 1. **Tracking Progress:**
   - Biết chính xác bot đang làm gì
   - Biết thời gian mỗi bước

### 2. **Debug Nhanh:**
   - Xác định ngay bước nào lỗi
   - Không cần đoán mò

### 3. **Monitoring:**
   - Theo dõi performance
   - Tối ưu hóa chỗ chậm

### 4. **Troubleshooting:**
   - Dễ dàng tìm nguyên nhân
   - Giải quyết vấn đề nhanh

---

## 📌 LƯU Ý

1. **Backup đã tạo:**
   - File gốc: `telegram_bot.py.backup_before_debug`
   - Có thể restore nếu cần

2. **Log file:**
   - Được lưu tại: `logs/bot.log`
   - Tự động rotate khi quá lớn

3. **Performance:**
   - Debug logging không ảnh hưởng đáng kể
   - Chỉ thêm vài milliseconds

4. **Production:**
   - Có thể giảm logging level nếu muốn
   - Thay `logging.INFO` → `logging.WARNING`

---

## 🔄 ROLLBACK (NẾU CẦN)

Nếu muốn quay lại version cũ:

```bash
cd CHI_BAO_TAM_LY_BOT
copy telegram_bot.py.backup_before_debug telegram_bot.py
```

---

## 📚 TÀI LIỆU LIÊN QUAN

- `DEBUG_ANALYSIS_REPORT.md` - Phân tích lỗi của script cũ
- `telegram_bot.py` - File đã được update
- `logs/bot.log` - Log file chính

---

## ✨ KẾT LUẬN

Debug logging đã được thêm thành công! Giờ bạn có thể:
- ✅ Theo dõi chính xác từng bước
- ✅ Debug nhanh khi có lỗi
- ✅ Hiểu rõ performance của bot
- ✅ Troubleshoot hiệu quả

**Happy debugging! 🎉**
