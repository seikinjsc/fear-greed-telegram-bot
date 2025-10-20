"""
test_send.py - Test gửi báo cáo qua Telegram
Chạy local để kiểm tra trước khi deploy
"""

import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from telegram import Bot
from fear_greed_dashboard import FearGreedDashboard

load_dotenv()

async def test_send_report():
    """Test gửi báo cáo"""
    
    print("\n" + "="*60)
    print("🧪 TEST GỬI BÁO CÁO QUA TELEGRAM")
    print("="*60)
    
    # Kiểm tra config
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    owner_id = os.getenv('OWNER_CHAT_ID')
    group_id = os.getenv('GROUP_CHAT_ID')
    
    if not bot_token or bot_token == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Lỗi: Chưa cấu hình TELEGRAM_BOT_TOKEN trong .env")
        return
    
    if not owner_id or owner_id == 'YOUR_CHAT_ID':
        print("❌ Lỗi: Chưa cấu hình OWNER_CHAT_ID trong .env")
        return
    
    print(f"✅ Bot Token: {bot_token[:20]}...")
    print(f"✅ Owner Chat ID: {owner_id}")
    print(f"✅ Group Chat ID: {group_id}")
    print()
    
    # Khởi tạo dashboard
    print("🔄 Bước 1/5: Khởi tạo dashboard...")
    dashboard = FearGreedDashboard()
    
    # Lấy dữ liệu
    print("🔄 Bước 2/5: Lấy dữ liệu từ API...")
    if not dashboard.fetch_data(limit=90):
        print("❌ Không thể lấy dữ liệu từ API")
        return
    
    print(f"✅ Đã lấy {len(dashboard.data)} bản ghi")
    print(f"📊 Giá trị hiện tại: {dashboard.current_value} - {dashboard.current_classification_vi}")
    print()
    
    # Tạo báo cáo
    print("🔄 Bước 3/5: Tạo báo cáo...")
    report_file = 'test_report_temp.png'
    dashboard.create_full_report(save_path=report_file)
    
    if not os.path.exists(report_file):
        print("❌ Không thể tạo file báo cáo")
        return
    
    file_size = os.path.getsize(report_file) / 1024  # KB
    print(f"✅ Đã tạo báo cáo: {report_file} ({file_size:.1f} KB)")
    print()
    
    # Gửi Telegram
    print("🔄 Bước 4/5: Gửi qua Telegram...")
    bot = Bot(token=bot_token)
    
    caption = f"""
📊 **BÁO CÁO CHỈ SỐ TÂM LÝ THỊ TRƯỜNG**
⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}

**Hiện tại:** {dashboard.current_value} - {dashboard.current_classification_vi}

🧪 **Test từ máy local**
#FearGreed #Crypto #TestReport
"""
    
    try:
        # Gửi cho owner
        with open(report_file, 'rb') as photo:
            await bot.send_photo(
                chat_id=owner_id,
                photo=photo,
                caption=caption,
                parse_mode='Markdown'
            )
        print(f"✅ Đã gửi cho owner: {owner_id}")
        
        # Gửi vào group nếu có
        if group_id and group_id != 'YOUR_GROUP_ID':
            with open(report_file, 'rb') as photo:
                await bot.send_photo(
                    chat_id=group_id,
                    photo=photo,
                    caption=caption,
                    parse_mode='Markdown'
                )
            print(f"✅ Đã gửi vào group: {group_id}")
        
    except Exception as e:
        print(f"❌ Lỗi khi gửi: {e}")
        return
    
    print()
    
    # Dọn dẹp
    print("🔄 Bước 5/5: Dọn dẹp...")
    os.remove(report_file)
    print(f"✅ Đã xóa file tạm: {report_file}")
    
    print()
    print("="*60)
    print("🎉 TEST THÀNH CÔNG!")
    print("="*60)
    print()
    print("📱 Kiểm tra Telegram, bạn sẽ thấy báo cáo!")
    print()
    print("🚀 Nếu test thành công, có thể deploy lên GitHub Actions")

if __name__ == '__main__':
    asyncio.run(test_send_report())