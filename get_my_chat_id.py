"""
get_my_chat_id.py - Lấy Chat ID của bạn
Chạy script này, sau đó gửi tin nhắn cho bot
"""

import os
import asyncio
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """In ra Chat ID mỗi khi nhận tin nhắn"""
    chat_id = update.effective_chat.id
    user = update.effective_user
    chat = update.effective_chat
    
    # Tạo thông báo chi tiết
    message = f"""
🎯 **THÔNG TIN CHAT**

👤 **Người gửi:**
• Tên: {user.first_name} {user.last_name or ''}
• Username: @{user.username or 'Không có'}
• User ID: `{user.id}`

💬 **Chat:**
• **Chat ID: `{chat_id}`** ⬅️ COPY CÁI NÀY!
• Chat Type: {chat.type}
• Chat Title: {chat.title or 'Private Chat'}

✅ **Để thêm vào GitHub Secrets:**
1. Copy số Chat ID ở trên: `{chat_id}`
2. Vào GitHub Settings → Secrets → Actions
3. Tìm secret tên `OWNER_CHAT_ID`
4. Update value = `{chat_id}`

📋 **Console output bên dưới để dễ copy**
"""
    
    await update.message.reply_text(message, parse_mode='Markdown')
    
    # In ra console để dễ copy
    print("\n" + "="*60)
    print("✅ CHAT ID CỦA BẠN")
    print("="*60)
    print(f"👤 Tên: {user.first_name} (@{user.username or 'no username'})")
    print(f"🆔 CHAT ID: {chat_id}")
    print(f"🆔 User ID: {user.id}")
    print("="*60)
    print(f"\n📋 COPY DÒNG NÀY VÀO GITHUB SECRETS:")
    print(f"   {chat_id}")
    print("\n" + "="*60 + "\n")
    
    # Gửi tin nhắn xác nhận
    await update.message.reply_text(
        f"✅ Đã lấy được Chat ID!\n\n"
        f"📊 Chat ID của bạn: `{chat_id}`\n\n"
        f"Hãy thêm số này vào GitHub Secrets với tên `OWNER_CHAT_ID`",
        parse_mode='Markdown'
    )

async def test_send_message():
    """Test gửi tin nhắn sau khi lấy được chat ID"""
    bot = Bot(token=BOT_TOKEN)
    owner_id = os.getenv('OWNER_CHAT_ID')
    
    if owner_id and owner_id != 'YOUR_CHAT_ID':
        try:
            await bot.send_message(
                chat_id=owner_id,
                text="✅ Test: Bot đã kết nối thành công!\n\n"
                     "Nếu bạn nhận được tin nhắn này, Chat ID đã đúng!"
            )
            print(f"✅ Đã gửi tin nhắn test tới Chat ID: {owner_id}")
        except Exception as e:
            print(f"❌ Lỗi gửi tin nhắn: {e}")

def main():
    print("\n" + "="*60)
    print("🤖 BOT ĐANG CHẠY - LẤY CHAT ID")
    print("="*60)
    print(f"✅ Bot: @sign15p_crypto_bot")
    print(f"✅ Bot ID: 8222770890")
    print("\n📱 HƯỚNG DẪN:")
    print("1. Mở Telegram")
    print("2. Tìm bot: @sign15p_crypto_bot")
    print("3. Gửi bất kỳ tin nhắn nào (vd: /start hoặc 'hello')")
    print("4. Bot sẽ reply Chat ID của bạn")
    print("5. Copy Chat ID đó vào GitHub Secrets")
    print("\n⏸️  Nhấn Ctrl+C để dừng\n")
    
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        app.add_handler(MessageHandler(filters.ALL, get_chat_id))
        
        # Nếu đã có OWNER_CHAT_ID, test gửi tin nhắn
        owner_id = os.getenv('OWNER_CHAT_ID')
        if owner_id and owner_id != 'YOUR_CHAT_ID':
            print(f"ℹ️  OWNER_CHAT_ID hiện tại: {owner_id}")
            print("🔄 Đang test gửi tin nhắn...\n")
            asyncio.run(test_send_message())
        
        app.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")

if __name__ == '__main__':
    main()