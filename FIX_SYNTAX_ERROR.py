"""
FIX_REPORT_HANG.py - Sửa lỗi báo cáo bị treo
"""

import shutil
from datetime import datetime

print("=" * 70)
print(" 🔧 SỬA LỖI BÁO CÁO BỊ TREO")
print("=" * 70)
print()

# Backup
backup = f"fear_greed_dashboard.py.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
shutil.copy('fear_greed_dashboard.py', backup)
print(f"✅ Backup: {backup}\n")

# Đọc file
with open('fear_greed_dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Tìm và sửa import matplotlib
new_lines = []
found_import = False

for i, line in enumerate(lines):
    # Thêm backend Agg TRƯỚC khi import pyplot
    if 'import matplotlib.pyplot as plt' in line and not found_import:
        new_lines.append('import matplotlib\n')
        new_lines.append('matplotlib.use(\'Agg\')  # Non-GUI backend\n')
        new_lines.append(line)
        found_import = True
        print("✅ Đã thêm matplotlib backend Agg")
    elif 'plt.rcParams[\'font.family\']' in line:
        # Bỏ dòng font không tồn tại
        new_lines.append('# ' + line)
        print("✅ Đã comment dòng font.family")
    elif 'plt.rcParams[\'axes.unicode_minus\']' in line:
        new_lines.append(line)
    else:
        new_lines.append(line)

# Ghi file
with open('fear_greed_dashboard.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print()
print("=" * 70)
print(" ✅ HOÀN TẤT SỬA LỖI!")
print("=" * 70)
print()
print("🔧 ĐÃ SỬA:")
print("   • Thêm matplotlib.use('Agg') - non-GUI backend")
print("   • Comment dòng font.family (không cần thiết)")
print()
print("🚀 KHỞI ĐỘNG LẠI BOT:")
print("   Ctrl+C để dừng bot hiện tại")
print("   python telegram_bot.py")
print()
print("📊 TEST:")
print("   Gửi /report cho bot")
print()