"""
get_group_id.py - Lấy Group Chat ID
"""

import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lấy Chat ID của group"""
    chat = update.effective_chat
    user = update.effective_user
    
    message = f"""
🎯 **THÔNG TIN CHAT**

💬 **Chat:**
• Type: {chat.type}
• Chat ID: `{chat.id}`
• Title: {chat.title or 'N/A'}

👤 **Người gửi:**
• Name: {user.first_name}
• Username: @{user.username or 'N/A'}
• User ID: {user.id}

✅ **Để dùng cho GROUP_CHAT_ID:**
Copy số này: `{chat.id}`
"""
    
    await update.message.reply_text(message, parse_mode='Markdown')
    
    # In ra console
    print("\n" + "="*60)
    if chat.type in ['group', 'supergroup']:
        print(f"🎯 GROUP CHAT ID: {chat.id}")
        print(f"📝 Group Name: {chat.title}")
        print("\n📋 COPY VÀO GITHUB SECRETS:")
        print(f"   {chat.id}")
    else:
        print(f"💬 PRIVATE CHAT ID: {chat.id}")
        print(f"👤 User: {user.first_name}")
    print("="*60 + "\n")

def main():
    print("\n" + "="*60)
    print("🤖 BOT ĐANG CHẠY - LẤY GROUP CHAT ID")
    print("="*60)
    print("\n📱 HƯỚNG DẪN:")
    print("1. Đã thêm bot vào group chưa?")
    print("   → Nếu chưa: Thêm @sign15p_crypto_bot vào group")
    print("\n2. Gửi bất kỳ tin nhắn nào trong group")
    print("   → Bot sẽ reply Chat ID của group")
    print("\n⏸️  Nhấn Ctrl+C để dừng\n")
    
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, get_chat_id))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()