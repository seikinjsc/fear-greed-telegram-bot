"""
test_token.py - Kiểm tra token Telegram có hợp lệ không
"""

import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def test_token():
    """Kiểm tra token"""
    
    print("\n" + "="*60)
    print("🔑 KIỂM TRA TELEGRAM BOT TOKEN")
    print("="*60)
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    owner_id = os.getenv('OWNER_CHAT_ID')
    
    if not bot_token or bot_token == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Token không được cấu hình trong .env")
        return False
    
    print(f"✅ Token tìm thấy: {bot_token[:20]}...")
    print(f"✅ Owner ID: {owner_id}")
    print()
    
    # Test import telegram
    try:
        from telegram import Bot
        print("✅ Module telegram đã cài đặt")
    except ImportError:
        print("❌ Chưa cài telegram: pip install python-telegram-bot")
        return False
    
    # Test khởi tạo bot
    print("\n🔄 Đang test kết nối...")
    try:
        bot = Bot(token=bot_token)
        print("✅ Bot object khởi tạo thành công")
    except Exception as e:
        print(f"❌ Lỗi khởi tạo bot: {e}")
        return False
    
    # Test lấy thông tin bot
    try:
        bot_info = await bot.get_me()
        print("\n" + "="*60)
        print("🤖 THÔNG TIN BOT")
        print("="*60)
        print(f"👤 Username: @{bot_info.username}")
        print(f"📝 Name: {bot_info.first_name}")
        print(f"🆔 Bot ID: {bot_info.id}")
        print(f"✅ Can join groups: {bot_info.can_join_groups}")
        print(f"✅ Can read messages: {bot_info.can_read_all_group_messages}")
        print("="*60)
        print("\n✅ TOKEN HỢP LỆ!")
        return True
        
    except Exception as e:
        print(f"\n❌ Lỗi khi test bot: {e}")
        print("\n💡 Nguyên nhân có thể:")
        print("   • Token sai hoặc đã bị thu hồi")
        print("   • Token có ký tự thừa (khoảng trắng, xuống dòng)")
        print("   • Kết nối internet bị lỗi")
        print("\n🔧 Cách fix:")
        print("   1. Lấy token mới từ @BotFather")
        print("   2. Copy chính xác (không có khoảng trắng)")
        print("   3. Paste vào file .env")
        return False

if __name__ == '__main__':
    result = asyncio.run(test_token())
    
    if result:
        print("\n🎉 Token hoạt động tốt!")
        print("📤 Có thể push lên GitHub và chạy workflow")
    else:
        print("\n⚠️  Cần fix token trước khi deploy")