"""Thêm thông báo trạng thái tự động"""
import re

# Đọc file
with open('telegram_bot.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Code thêm vào
notification_code = '''

async def send_bot_status(context: ContextTypes.DEFAULT_TYPE, status: str):
    """Gửi thông báo trạng thái bot"""
    try:
        timestamp = datetime.now().strftime('%d/%m/%Y lúc %H:%M:%S')
        
        if status == "started":
            message = f"""
🟢 **BOT ĐÃ KHỞI ĐỘNG**

⏰ Thời gian: {timestamp}
📊 Trạng thái: Đang hoạt động
✅ Sẵn sàng nhận lệnh!

Gửi /help để xem hướng dẫn.
"""
        elif status == "stopped":
            message = f"🔴 **BOT ĐÃ DỪNG** - {timestamp}"
        else:
            message = f"ℹ️ {status} - {timestamp}"
        
        await context.bot.send_message(
            chat_id=Config.OWNER_CHAT_ID,
            text=message,
            parse_mode=ParseMode.MARKDOWN
        )
        
        if Config.GROUP_CHAT_ID != 'YOUR_GROUP_ID':
            await context.bot.send_message(
                chat_id=Config.GROUP_CHAT_ID,
                text=f"🔔 Bot {status} lúc {timestamp}"
            )
        
        logger.info(f"Status sent: {status}")
    except Exception as e:
        logger.error(f"Error: {e}")
'''

# Tìm vị trí thêm (sau hàm get_interpretation)
pattern = r'(def get_interpretation\(value\):.*?return.*?\n)'
match = re.search(pattern, content, re.DOTALL)

if match:
    insert_pos = match.end()
    content = content[:insert_pos] + notification_code + content[insert_pos:]
    print("✅ Đã thêm hàm send_bot_status")
else:
    print("❌ Không tìm thấy hàm get_interpretation")
    exit(1)

# Cập nhật hàm post_init
old_post_init = '''async def post_init(application: Application):
    """Callback sau khi application khởi tạo - start scheduler ở đây"""
    scheduler.start()
    logger.info("Scheduler started successfully")'''

new_post_init = '''async def post_init(application: Application):
    """Callback sau khi application khởi tạo - start scheduler ở đây"""
    scheduler.start()
    logger.info("Scheduler started successfully")
    
    # Gửi thông báo bot đã khởi động
    await send_bot_status(application.bot_data, "started")'''

if old_post_init in content:
    content = content.replace(old_post_init, new_post_init)
    print("✅ Đã cập nhật hàm post_init")
else:
    print("❌ Không tìm thấy hàm post_init")

# Lưu file
with open('telegram_bot.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ HOÀN TẤT! Chạy bot để test:")
print("   python telegram_bot.py")