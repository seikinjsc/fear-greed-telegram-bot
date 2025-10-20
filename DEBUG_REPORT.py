"""
ADD_DEBUG_LOGS.py - Thêm debug logging vào telegram_bot.py
"""

import shutil
from datetime import datetime

print("=" * 70)
print(" 🐛 THÊM DEBUG LOGGING VÀO BOT")
print("=" * 70)
print()

# Backup
backup = f"telegram_bot.py.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
shutil.copy('telegram_bot.py', backup)
print(f"✅ Backup: {backup}\n")

# Đọc file
with open('telegram_bot.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Tìm hàm gauge_command và thêm debug
old_gauge = '''@owner_only
async def gauge_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler cho /gauge"""
    await update.message.reply_text("⏳ Đang tạo gauge chart...")
    
    try:
        if dashboard.fetch_data(limit=7):'''

new_gauge = '''@owner_only
async def gauge_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler cho /gauge"""
    logger.info("=== GAUGE COMMAND STARTED ===")
    await update.message.reply_text("⏳ Đang tạo gauge chart...")
    
    try:
        logger.info("Step 1: Fetching data...")
        if dashboard.fetch_data(limit=7):
            logger.info("Step 2: Data fetched successfully")'''

if old_gauge in content:
    content = content.replace(old_gauge, new_gauge)
    print("✅ Đã thêm debug vào gauge_command")

# Thêm debug vào phần tạo file
old_create_gauge = '''            dashboard.create_simple_gauge(save_path=filename)
            
            caption = f"""'''

new_create_gauge = '''            logger.info(f"Step 3: Creating gauge, saving to {filename}")
            dashboard.create_simple_gauge(save_path=filename)
            logger.info(f"Step 4: Gauge created successfully")
            
            import os
            if os.path.exists(filename):
                size = os.path.getsize(filename)
                logger.info(f"Step 5: File exists, size={size} bytes")
            else:
                logger.error(f"Step 5: File NOT created!")
            
            caption = f"""'''

if old_create_gauge in content:
    content = content.replace(old_create_gauge, new_create_gauge)
    print("✅ Đã thêm debug vào phần tạo gauge file")

# Thêm debug vào phần gửi ảnh
old_send_photo = '''            with open(filename, 'rb') as photo:
                await update.message.reply_photo(
                    photo=photo,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN
                )
            
            os.remove(filename)
            logger.info("Gauge chart sent successfully")'''

new_send_photo = '''            logger.info("Step 6: Opening file to send...")
            with open(filename, 'rb') as photo:
                logger.info("Step 7: Sending photo to Telegram...")
                await update.message.reply_photo(
                    photo=photo,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN
                )
                logger.info("Step 8: Photo sent successfully")
            
            logger.info("Step 9: Removing temp file...")
            os.remove(filename)
            logger.info("=== GAUGE COMMAND COMPLETED ===")'''

if old_send_photo in content:
    content = content.replace(old_send_photo, new_send_photo)
    print("✅ Đã thêm debug vào phần gửi ảnh")

# Tương tự cho report_command
old_report_start = '''@owner_only
async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler cho /report"""
    await update.message.reply_text("⏳ Đang tạo báo cáo đầy đủ...")
    
    try:
        if dashboard.fetch_data(limit=90):'''

new_report_start = '''@owner_only
async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler cho /report"""
    logger.info("=== REPORT COMMAND STARTED ===")
    await update.message.reply_text("⏳ Đang tạo báo cáo đầy đủ...")
    
    try:
        logger.info("Step 1: Fetching data (90 records)...")
        if dashboard.fetch_data(limit=90):
            logger.info("Step 2: Data fetched successfully")'''

if old_report_start in content:
    content = content.replace(old_report_start, new_report_start)
    print("✅ Đã thêm debug vào report_command")

# Thêm debug vào phần tạo report
old_create_report = '''            dashboard.create_full_report(save_path=report_file)
            dashboard.data.to_csv(data_file, index=False)'''

new_create_report = '''            logger.info(f"Step 3: Creating full report, saving to {report_file}")
            logger.info("This may take 10-30 seconds...")
            
            import time
            start_time = time.time()
            dashboard.create_full_report(save_path=report_file)
            elapsed = time.time() - start_time
            logger.info(f"Step 4: Report created in {elapsed:.2f} seconds")
            
            import os
            if os.path.exists(report_file):
                size = os.path.getsize(report_file)
                logger.info(f"Step 5: Report file exists, size={size} bytes")
            else:
                logger.error("Step 5: Report file NOT created!")
            
            logger.info("Step 6: Saving CSV...")
            dashboard.data.to_csv(data_file, index=False)
            logger.info("Step 7: CSV saved")'''

if old_create_report in content:
    content = content.replace(old_create_report, new_create_report)
    print("✅ Đã thêm debug vào phần tạo report")

# Ghi file
with open('telegram_bot.py', 'w', encoding='utf-8') as f:
    f.write(content)

print()
print("=" * 70)
print(" ✅ HOÀN TẤT THÊM DEBUG!")
print("=" * 70)
print()
print("🐛 ĐÃ THÊM DEBUG CHO:")
print("   • gauge_command - 9 bước")
print("   • report_command - 10+ bước")
print("   • Hiển thị thời gian tạo báo cáo")
print("   • Hiển thị kích thước file")
print()
print("🚀 CHẠY BOT VÀ XEM LOGS:")
print("   python telegram_bot.py")
print()
print("   Sau đó gửi /gauge hoặc /report")
print("   Xem terminal để thấy từng bước")
print()
print("📝 LOGS SẼ HIỂN THỊ:")
print("   Step 1: Fetching data...")
print("   Step 2: Data fetched successfully")
print("   Step 3: Creating gauge...")
print("   Step 4: Gauge created successfully")
print("   ...")
print()
print("   Nếu dừng ở bước nào = lỗi ở bước đó!")
print()