# 🤖 Chỉ Số Sợ Hãi & Tham Lam Bot

Bot Telegram tự động theo dõi chỉ số Fear & Greed của thị trường Crypto.

## ✨ Tính năng

- 📊 Hiển thị chỉ số hiện tại
- 📈 Báo cáo chi tiết với biểu đồ
- 🎯 Phân tích tín hiệu giao dịch
- ⏰ Gửi báo cáo tự động (8h, 12h, 16h, 20h)
- 🇻🇳 Hoàn toàn bằng tiếng Việt

## 🚀 Cài đặt

1. Clone repository
2. Cài đặt dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` thành `.env` và điền thông tin
4. Chạy bot: `python telegram_bot.py`

## 📝 Lệnh Bot

- `/current` - Xem chỉ số hiện tại
- `/gauge` - Đồng hồ Fear & Greed
- `/report` - Báo cáo đầy đủ
- `/signal` - Tín hiệu mua/bán
- `/schedule on/off` - Bật/tắt lịch tự động

## 🔑 Cấu hình

Cần 3 biến môi trường trong `.env`:
- `TELEGRAM_BOT_TOKEN` - Token từ @BotFather
- `OWNER_CHAT_ID` - Chat ID của bạn
- `GROUP_CHAT_ID` - ID nhóm (tùy chọn)

## 📊 API

Sử dụng API từ: https://alternative.me/crypto/fear-and-greed-index/
```

---

## 2. TẠO REPOSITORY TRÊN GITHUB

### Bước 2.1: Tạo repository mới

1. Truy cập https://github.com
2. Đăng nhập tài khoản
3. Click nút **"New"** (góc trên bên phải)
4. Điền thông tin:
   - **Repository name**: `fear-greed-telegram-bot`
   - **Description**: `Bot Telegram tự động theo dõi chỉ số Fear & Greed thị trường Crypto`
   - Chọn **Private** (để bảo mật)
   - ✅ **KHÔNG** tick "Add a README file" (vì đã có sẵn)
5. Click **"Create repository"**

### Bước 2.2: Lưu lại URL repository

Sau khi tạo, GitHub sẽ cho bạn URL kiểu:
```
https://github.com/YOUR_USERNAME/fear-greed-telegram-bot.git