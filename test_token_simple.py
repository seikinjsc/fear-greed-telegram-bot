"""
test_token_simple.py - Test token trực tiếp không qua .env
"""

import asyncio

async def test_token_direct():
    """Test token trực tiếp"""
    
    print("\n" + "="*60)
    print("🔑 TEST TOKEN TRỰC TIẾP")
    print("="*60)
    
    # Nhập token trực tiếp
    print("\nBước 1: Nhập token từ BotFather")
    print("Format: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz")
    token = input("\nPaste token vào đây: ").strip()
    
    if not token:
        print("❌ Token trống!")
        return False
    
    print(f"\n✅ Token nhận được: {token[:20]}...")
    print(f"📏 Độ dài: {len(token)} ký tự")
    
    # Kiểm tra format
    if ':' not in token:
        print("❌ Token sai format (thiếu dấu ':')")
        return False
    
    parts = token.split(':')
    print(f"✅ Bot ID: {parts[0]}")
    print(f"✅ Auth part: {parts[1][:10]}... (length={len(parts[1])})")
    
    # Test kết nối
    print("\n🔄 Đang test kết nối...")
    
    try:
        from telegram import Bot
        bot = Bot(token=token)
        
        print("✅ Bot object created")
        
        # Lấy thông tin bot
        me = await bot.get_me()
        
        print("\n" + "="*60)
        print("🎉 TOKEN HỢP LỆ!")
        print("="*60)
        print(f"👤 Username: @{me.username}")
        print(f"📝 Name: {me.first_name}")
        print(f"🆔 Bot ID: {me.id}")
        print("="*60)
        
        print("\n📋 COPY TOKEN NÀY VÀO GITHUB SECRETS:")
        print(f"   {token}")
        print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        print("\n💡 Có thể:")
        print("   • Token sai")
        print("   • Có ký tự thừa (khoảng trắng)")
        print("   • Internet bị lỗi")
        return False

if __name__ == '__main__':
    result = asyncio.run(test_token_direct())
    
    if result:
        print("✅ Token OK - Có thể dùng cho GitHub!")
    else:
        print("❌ Token có vấn đề - Cần lấy lại từ BotFather")