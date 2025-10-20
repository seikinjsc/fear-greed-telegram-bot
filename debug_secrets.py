"""
debug_secrets.py - Debug secrets
Thêm vào workflow để kiểm tra
"""

import os
import sys

print("\n" + "="*60)
print("🔍 DEBUG ENVIRONMENT VARIABLES")
print("="*60)

# Lấy từ environment
bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
owner_id = os.environ.get('OWNER_CHAT_ID')
group_id = os.environ.get('GROUP_CHAT_ID')

print("\n📊 Secrets Status:")
print(f"   TELEGRAM_BOT_TOKEN: {'✅ EXISTS' if bot_token else '❌ MISSING'}")
if bot_token:
    print(f"      • Length: {len(bot_token)}")
    print(f"      • First 20 chars: {bot_token[:20]}...")
    print(f"      • Has colon: {'✅ YES' if ':' in bot_token else '❌ NO'}")
    if ':' in bot_token:
        parts = bot_token.split(':')
        print(f"      • Bot ID: {parts[0]}")
        print(f"      • Auth length: {len(parts[1])}")

print(f"\n   OWNER_CHAT_ID: {'✅ EXISTS' if owner_id else '❌ MISSING'}")
if owner_id:
    print(f"      • Value: {owner_id}")
    print(f"      • Is numeric: {'✅ YES' if owner_id.isdigit() else '❌ NO'}")

print(f"\n   GROUP_CHAT_ID: {'✅ EXISTS' if group_id else '❌ MISSING'}")
if group_id:
    print(f"      • Value: {group_id}")

print("\n" + "="*60)
print("🐍 Python Environment:")
print(f"   Python version: {sys.version}")
print(f"   Platform: {sys.platform}")

# Test import telegram
try:
    import telegram
    print(f"\n✅ python-telegram-bot: {telegram.__version__}")
except ImportError as e:
    print(f"\n❌ Cannot import telegram: {e}")

print("="*60 + "\n")