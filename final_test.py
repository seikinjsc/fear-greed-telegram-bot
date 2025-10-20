"""
final_test.py - Mô phỏng đúng cách GitHub Actions chạy
Test này sẽ giống 100% với workflow
"""

import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

async def final_test():
    """Test giống GitHub Actions"""
    
    print("\n" + "="*60)
    print("🧪 FINAL TEST - MÔ PHỎNG GITHUB ACTIONS")
    print("="*60)
    
    # Giống workflow: lấy từ environment variables
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    owner_id = os.environ.get('OWNER_CHAT_ID')
    group_id = os.environ.get('GROUP_CHAT_ID')
    
    # Debug giống workflow
    print("\n🔍 KIỂM TRA BIẾN MÔI TRƯỜNG")
    print("="*60)
    print(f"Bot Token: {'✅ Có (' + bot_token[:20] + '...)' if bot_token else '❌ Không có'}")
    print(f"Token Length: {len(bot_token) if bot_token else 0}")
    print(f"Owner ID: {'✅ Có (' + owner_id + ')' if owner_id else '❌ Không có'}")
    print(f"Group ID: {'✅ Có (' + group_id + ')' if group_id else '❌ Không có'}")
    print("="*60 + "\n")
    
    if not bot_token or not bot_token.strip():
        print("❌ TELEGRAM_BOT_TOKEN không được thiết lập!")
        return False
    
    if not owner_id:
        print("❌ OWNER_CHAT_ID không được thiết lập!")
        return False
    
    # Import sau khi đã check
    from telegram import Bot
    from fear_greed_dashboard import FearGreedDashboard
    
    # Lấy dữ liệu
    print("🔄 Bước 1/4: Lấy dữ liệu...")
    dashboard = FearGreedDashboard()
    
    if not dashboard.fetch_data(limit=90):
        print("❌ Không thể lấy dữ liệu từ API")
        return False
    
    print(f"✅ Đã lấy {len(dashboard.data)} bản ghi")
    print(f"📊 Giá trị: {dashboard.current_value} - {dashboard.current_classification_vi}\n")
    
    # Tạo báo cáo
    print("🔄 Bước 2/4: Tạo báo cáo...")
    report_file = 'final_test_report.png'
    dashboard.create_full_report(save_path=report_file)
    
    if not os.path.exists(report_file):
        print("❌ Không thể tạo file báo cáo")
        return False
    
    file_size = os.path.getsize(report_file) / 1024
    print(f"✅ Đã tạo báo cáo ({file_size:.1f} KB)\n")
    
    # Gửi Telegram
    print("🔄 Bước 3/4: Gửi qua Telegram...")
    bot = Bot(token=bot_token)
    
    caption = f"""📊 **BÁO CÁO CHỈ SỐ TÂM LÝ THỊ TRƯỜNG**
⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}

**Hiện tại:** {dashboard.current_value} - {dashboard.current_classification_vi}

🧪 **Final Test - Giống GitHub Actions**
#FearGreed #Crypto #FinalTest"""
    
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
        if group_id and group_id != 'YOUR_GROUP_ID' and group_id.strip():
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
        return False
    
    # Dọn dẹp
    print("\n🔄 Bước 4/4: Dọn dẹp...")
    os.remove(report_file)
    print("✅ Đã xóa file tạm")
    
    print("\n" + "="*60)
    print("🎉 FINAL TEST THÀNH CÔNG!")
    print("="*60)
    print("\n✅ Nếu test này pass:")
    print("   • GitHub Actions sẽ chạy tương tự")
    print("   • Có thể deploy an tâm")
    print("\n🚀 Bước tiếp theo:")
    print("   1. Cập nhật GitHub Secrets giống .env")
    print("   2. Push code lên GitHub")
    print("   3. Chạy workflow")
    print()
    
    return True

if __name__ == '__main__':
    result = asyncio.run(final_test())
    
    if not result:
        print("\n⚠️  Test thất bại - cần fix trước khi deploy")
        exit(1)