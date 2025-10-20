"""
debug_secrets.py - Debug chi tiết secrets
"""

import os
import sys

print("\n" + "="*70)
print(" DEBUG GITHUB SECRETS")
print("="*70)

# Lấy secrets
bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
owner_id = os.environ.get('OWNER_CHAT_ID', '')
group_id = os.environ.get('GROUP_CHAT_ID', '')

print("\n Secrets Status:")
print("-"*70)

# Bot Token
print(f"\n1  TELEGRAM_BOT_TOKEN:")
if bot_token:
    print(f"    EXISTS")
    print(f"    Length: {len(bot_token)} chars")
    print(f"    First 20: {bot_token[:20]}...")
    print(f"    Last 10: ...{bot_token[-10:]}")
    print(f"     Has colon: {'YES' if ':' in bot_token else 'NO '}")
    if ':' in bot_token:
        parts = bot_token.split(':')
        print(f"    Bot ID: {parts[0]}")
        print(f"    Auth part length: {len(parts[1])} chars")
    print(f"    Stripped length: {len(bot_token.strip())}")
    print(f"     Has spaces: {'YES ' if bot_token != bot_token.strip() else 'NO '}")
else:
    print(f"    MISSING OR EMPTY")

# Owner Chat ID
print(f"\n2  OWNER_CHAT_ID:")
if owner_id:
    print(f"    EXISTS")
    print(f"    Value: {owner_id}")
    print(f"    Length: {len(owner_id)} chars")
    print(f"    Is numeric: {'YES' if owner_id.isdigit() else 'NO '}")
    print(f"    Stripped: {owner_id.strip()}")
    print(f"     Has spaces: {'YES ' if owner_id != owner_id.strip() else 'NO '}")
else:
    print(f"    MISSING OR EMPTY")

# Group Chat ID
print(f"\n3  GROUP_CHAT_ID:")
if group_id:
    print(f"    EXISTS")
    print(f"    Value: {group_id}")
    print(f"    Length: {len(group_id)} chars")
    print(f"    Type: {type(group_id)}")
else:
    print(f"    MISSING OR EMPTY")

print("\n" + "="*70)
print(" Python Environment:")
print("-"*70)
print(f"   Python: {sys.version}")
print(f"   Platform: {sys.platform}")

# Test telegram import
try:
    import telegram
    print(f"\n python-telegram-bot: {telegram.__version__}")
    
    # Test create bot
    if bot_token:
        print(f"\n Testing Bot Creation:")
        try:
            bot = telegram.Bot(token=bot_token.strip())
            print(f"    Bot object created successfully")
        except Exception as e:
            print(f"    Failed to create bot: {e}")
    
except ImportError as e:
    print(f"\n Cannot import telegram: {e}")

print("\n" + "="*70)
print(" DEBUG COMPLETED")
print("="*70 + "\n")
