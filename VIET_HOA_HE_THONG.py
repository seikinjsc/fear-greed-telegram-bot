"""
VIET_HOA_HE_THONG.py - Việt hóa toàn bộ hệ thống Fear & Greed Bot
Chạy trong folder CHI_BAO_TAM_LY_BOT
"""

import os
import shutil
from datetime import datetime

def backup_file(filename):
    """Backup file trước khi sửa"""
    if os.path.exists(filename):
        backup = f"{filename}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy(filename, backup)
        print(f"✅ Backup: {backup}")
        return True
    return False

print("=" * 70)
print(" 🇻🇳 VIỆT HÓA HỆ THỐNG FEAR & GREED BOT")
print("=" * 70)
print()

# ============================================================
# FILE 1: fear_greed_dashboard.py - Việt hóa hoàn toàn
# ============================================================

DASHBOARD_CONTENT = '''"""
fear_greed_dashboard.py - Dashboard vẽ biểu đồ Chỉ Báo Tâm Lý (100% Tiếng Việt)
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Wedge, FancyBboxPatch
import numpy as np
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.dates as mdates

# Cấu hình font tiếng Việt
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

plt.style.use('dark_background')
sns.set_palette("husl")


class FearGreedDashboard:
    def __init__(self):
        self.base_url = "https://api.alternative.me/fng/"
        self.data = None
        self.current_value = None
        self.current_classification = None
        
        # Bảng dịch tiếng Việt
        self.translations = {
            'Extreme Fear': 'Sợ Hãi Cực Độ',
            'Fear': 'Sợ Hãi',
            'Neutral': 'Trung Lập',
            'Greed': 'Tham Lam',
            'Extreme Greed': 'Tham Lam Cực Độ'
        }
        
    def translate(self, text):
        """Dịch sang tiếng Việt"""
        return self.translations.get(text, text)
        
    def fetch_data(self, limit=90):
        """Lấy dữ liệu từ API"""
        try:
            response = requests.get(f"{self.base_url}?limit={limit}")
            data = response.json()
            
            if data['metadata']['error']:
                print("❌ Lỗi khi lấy dữ liệu")
                return False
            
            df = pd.DataFrame(data['data'])
            df['value'] = df['value'].astype(int)
            df['timestamp'] = pd.to_datetime(df['timestamp'].astype(int), unit='s')
            df = df.sort_values('timestamp').reset_index(drop=True)
            
            # Thêm cột tiếng Việt
            df['value_classification_vi'] = df['value_classification'].map(self.translations)
            
            self.data = df
            self.current_value = df.iloc[-1]['value']
            self.current_classification = df.iloc[-1]['value_classification']
            self.current_classification_vi = self.translate(self.current_classification)
            
            print(f"✅ Đã lấy {len(df)} bản ghi")
            print(f"📊 Giá trị hiện tại: {self.current_value} - {self.current_classification_vi}")
            
            return True
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return False
    
    def get_color_for_value(self, value):
        """Lấy màu gradient dựa trên giá trị"""
        if value <= 25:
            return '#d32f2f'
        elif value <= 45:
            return '#ff9800'
        elif value <= 55:
            return '#fdd835'
        elif value <= 75:
            return '#66bb6a'
        else:
            return '#2e7d32'
    
    def draw_gauge_chart(self, ax):
        """Vẽ đồng hồ gauge"""
        value = self.current_value
        classification_vi = self.current_classification_vi
        
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-0.2, 1.2)
        ax.axis('off')
        
        # Vẽ nửa vòng tròn với gradient màu
        segments = [
            (180, 145, '#d32f2f'),  # Sợ hãi cực độ
            (145, 110, '#ff9800'),  # Sợ hãi
            (110, 90, '#fdd835'),   # Trung lập
            (90, 55, '#66bb6a'),    # Tham lam
            (55, 0, '#2e7d32')      # Tham lam cực độ
        ]
        
        for start, end, color in segments:
            wedge = Wedge(
                center=(0, 0),
                r=1,
                theta1=end,
                theta2=start,
                width=0.3,
                facecolor=color,
                edgecolor='none',
                alpha=0.8
            )
            ax.add_patch(wedge)
        
        # Vòng tròn trong
        inner_circle = plt.Circle((0, 0), 0.7, color='#1a1a1a', zorder=10)
        ax.add_patch(inner_circle)
        
        # Kim chỉ
        angle_rad = np.pi * (1 - value / 100)
        needle_length = 0.65
        needle_x = needle_length * np.cos(angle_rad)
        needle_y = needle_length * np.sin(angle_rad)
        
        ax.plot([0, needle_x], [0, needle_y], 
                color='white', linewidth=4, zorder=15)
        ax.plot([0, needle_x], [0, needle_y], 
                color=self.get_color_for_value(value), linewidth=2.5, zorder=16)
        
        # Điểm tròn giữa
        center_circle = plt.Circle((0, 0), 0.08, color='white', zorder=20)
        ax.add_patch(center_circle)
        
        # Hiển thị số
        ax.text(0, -0.15, f'{value}', 
                fontsize=72, fontweight='bold', ha='center', va='center',
                color='white', zorder=25)
        
        # Hiển thị phân loại tiếng Việt
        ax.text(0, -0.45, classification_vi, 
                fontsize=18, ha='center', va='center',
                color='#aaaaaa', zorder=25)
        
        # Label đầu cuối
        ax.text(-1.15, -0.1, '0', fontsize=14, color='#666666', ha='center')
        ax.text(1.15, -0.1, '100', fontsize=14, color='#666666', ha='center')
    
    def draw_stats_boxes(self, ax):
        """Vẽ các ô thống kê"""
        ax.axis('off')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        
        yesterday_value = self.data.iloc[-2]['value']
        yesterday_class_vi = self.translate(self.data.iloc[-2]['value_classification'])
        
        week_avg = self.data.tail(7)['value'].mean()
        # Xác định phân loại tuần trước
        if week_avg <= 25:
            week_class_vi = 'Sợ Hãi Cực Độ'
        elif week_avg <= 45:
            week_class_vi = 'Sợ Hãi'
        elif week_avg <= 55:
            week_class_vi = 'Trung Lập'
        elif week_avg <= 75:
            week_class_vi = 'Tham Lam'
        else:
            week_class_vi = 'Tham Lam Cực Độ'
        
        # Box 1: Hôm qua
        rect1 = FancyBboxPatch((0.5, 6.5), 4, 2.8, 
                               boxstyle="round,pad=0.15", 
                               facecolor='#2a2a2a', 
                               edgecolor='#404040',
                               linewidth=2)
        ax.add_patch(rect1)
        
        ax.text(2.5, 8.8, 'Hôm Qua', 
                fontsize=13, ha='center', color='#999999', fontweight='bold')
        ax.text(2.5, 8.2, yesterday_class_vi, 
                fontsize=10, ha='center', color='#ffa726')
        ax.text(2.5, 7.3, f'{yesterday_value}', 
                fontsize=36, ha='center', color='white', fontweight='bold')
        
        # Box 2: Tuần trước
        rect2 = FancyBboxPatch((5.5, 6.5), 4, 2.8, 
                               boxstyle="round,pad=0.15", 
                               facecolor='#2a2a2a', 
                               edgecolor='#404040',
                               linewidth=2)
        ax.add_patch(rect2)
        
        ax.text(7.5, 8.8, 'Tuần Trước', 
                fontsize=13, ha='center', color='#999999', fontweight='bold')
        ax.text(7.5, 8.2, week_class_vi, 
                fontsize=10, ha='center', color='#66bb6a')
        ax.text(7.5, 7.3, f'{int(week_avg)}', 
                fontsize=36, ha='center', color='white', fontweight='bold')
        
        # Câu hỏi
        ax.text(5, 5.8, 'Bạn nghĩ gì về Bitcoin hôm nay?', 
                fontsize=13, ha='center', color='white', fontweight='bold')
        
        # Nút Giảm
        rect_down = FancyBboxPatch((1, 4.2), 3.5, 1.2, 
                                   boxstyle="round,pad=0.08", 
                                   facecolor='#d32f2f', 
                                   edgecolor='none')
        ax.add_patch(rect_down)
        ax.text(2.75, 4.8, '📉 Giảm Giá', 
                fontsize=14, ha='center', va='center', 
                color='white', fontweight='bold')
        
        # Nút Tăng
        rect_up = FancyBboxPatch((5.5, 4.2), 3.5, 1.2, 
                                 boxstyle="round,pad=0.08", 
                                 facecolor='#2e7d32', 
                                 edgecolor='none')
        ax.add_patch(rect_up)
        ax.text(7.25, 4.8, '📈 Tăng Giá', 
                fontsize=14, ha='center', va='center', 
                color='white', fontweight='bold')
        
        # Mô tả
        description = ("Chỉ số dao động từ 0 (Sợ hãi tối đa) đến 100 (Tham lam cực độ). "
                      "Phản ánh tâm lý và cảm xúc của nhà đầu tư crypto. "
                      "Dữ liệu được tổng hợp từ nhiều nguồn để phân tích chính xác xu hướng thị trường.")
        
        ax.text(5, 2.3, description, 
                fontsize=9.5, ha='center', va='top', 
                color='#999999', wrap=True, 
                multialignment='center',
                bbox=dict(boxstyle='round,pad=0.6', 
                         facecolor='#1a1a1a', 
                         edgecolor='#333333',
                         linewidth=1.5))
    
    def draw_historical_chart(self, ax):
        """Vẽ biểu đồ lịch sử"""
        df = self.data.tail(30).copy()
        colors = [self.get_color_for_value(v) for v in df['value']]
        
        # Vẽ đường line
        ax.plot(df['timestamp'], df['value'], 
                color='white', linewidth=3, alpha=0.9, zorder=10)
        
        # Tô vùng dưới đường
        ax.fill_between(df['timestamp'], df['value'], 0, 
                        alpha=0.3, color='#3f51b5')
        
        # Vẽ các điểm
        scatter = ax.scatter(df['timestamp'], df['value'], 
                           c=colors, s=80, zorder=15, 
                           edgecolors='white', linewidths=2)
        
        ax.set_facecolor('#1a1a1a')
        ax.set_xlabel('Ngày Tháng', fontsize=14, color='#999999', labelpad=10)
        ax.set_ylabel('Chỉ Số Tâm Lý', fontsize=14, color='#999999', labelpad=10)
        ax.set_title('Lịch Sử 30 Ngày Gần Nhất', 
                    fontsize=16, color='white', fontweight='bold', pad=20)
        
        # Grid
        ax.grid(True, alpha=0.15, linestyle='--', linewidth=0.5)
        ax.set_ylim(0, 100)
        
        # Vùng màu nền
        ax.axhspan(0, 25, alpha=0.08, color='#d32f2f', zorder=1)
        ax.axhspan(25, 45, alpha=0.08, color='#ff9800', zorder=1)
        ax.axhspan(45, 55, alpha=0.08, color='#fdd835', zorder=1)
        ax.axhspan(55, 75, alpha=0.08, color='#66bb6a', zorder=1)
        ax.axhspan(75, 100, alpha=0.08, color='#2e7d32', zorder=1)
        
        # Label tiếng Việt cho các vùng
        ax.text(df['timestamp'].iloc[1], 12, 'Sợ Hãi Cực Độ', 
                fontsize=9, color='#d32f2f', alpha=0.7, fontweight='bold')
        ax.text(df['timestamp'].iloc[1], 35, 'Sợ Hãi', 
                fontsize=9, color='#ff9800', alpha=0.7, fontweight='bold')
        ax.text(df['timestamp'].iloc[1], 50, 'Trung Lập', 
                fontsize=9, color='#fdd835', alpha=0.7, fontweight='bold')
        ax.text(df['timestamp'].iloc[1], 65, 'Tham Lam', 
                fontsize=9, color='#66bb6a', alpha=0.7, fontweight='bold')
        ax.text(df['timestamp'].iloc[1], 87, 'Tham Lam Cực Độ', 
                fontsize=9, color='#2e7d32', alpha=0.7, fontweight='bold')
        
        # Format trục X
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        
        plt.setp(ax.xaxis.get_majorticklabels(), 
                rotation=45, ha='right', fontsize=11)
        
        ax.tick_params(colors='#666666', labelsize=11, length=6, width=1.5)
        
        for spine in ax.spines.values():
            spine.set_color('#333333')
            spine.set_linewidth(1.5)
    
    def create_full_report(self, save_path='bao_cao_tam_ly.png'):
        """Tạo báo cáo đầy đủ"""
        fig = plt.figure(figsize=(22, 14), facecolor='#0d0d0d')
        
        gs = fig.add_gridspec(4, 2, 
                             height_ratios=[0.15, 0.8, 0.05, 1.2],
                             hspace=0.15, wspace=0.3,
                             left=0.08, right=0.92, top=0.95, bottom=0.08)
        
        # Tiêu đề chính
        fig.text(0.5, 0.98, 'CHỈ SỐ SỢ HÃI VÀ THAM LAM - THỊ TRƯỜNG TIỀN MÃ HÓA', 
                fontsize=26, fontweight='bold', ha='center', 
                color='white', va='top')
        
        # Thông tin cập nhật
        fig.text(0.5, 0.96, 
                f'Cập nhật: {datetime.now().strftime("%d/%m/%Y lúc %H:%M")} | ' + 
                f'Hiện tại: {self.current_value} điểm - {self.current_classification_vi}',
                fontsize=13, ha='center', color='#999999', va='top')
        
        # Vẽ gauge
        ax1 = fig.add_subplot(gs[1, 0])
        self.draw_gauge_chart(ax1)
        
        # Vẽ stats boxes
        ax2 = fig.add_subplot(gs[1, 1])
        self.draw_stats_boxes(ax2)
        
        # Vẽ biểu đồ lịch sử
        ax3 = fig.add_subplot(gs[3, :])
        self.draw_historical_chart(ax3)
        
        plt.savefig(save_path, dpi=150, facecolor='#0d0d0d', 
                   edgecolor='none', bbox_inches='tight')
        print(f"\\n✅ Đã lưu báo cáo: {save_path}")
        plt.close()
    
    def create_simple_gauge(self, save_path='dong_ho_tam_ly.png'):
        """Tạo gauge đơn giản"""
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#0d0d0d')
        self.draw_gauge_chart(ax)
        
        fig.text(0.5, 0.95, 'Chỉ Số Sợ Hãi & Tham Lam', 
                fontsize=20, fontweight='bold', ha='center', 
                color='white', va='top')
        fig.text(0.5, 0.90, f'{self.current_classification_vi} - {self.current_value} điểm', 
                fontsize=14, ha='center', color='#999999', va='top')
        
        plt.savefig(save_path, dpi=150, facecolor='#0d0d0d', 
                   edgecolor='none', bbox_inches='tight')
        print(f"✅ Đã lưu đồng hồ: {save_path}")
        plt.close()


if __name__ == "__main__":
    print("=" * 60)
    print("CHỈ SỐ SỢ HÃI & THAM LAM - KIỂM TRA")
    print("=" * 60)
    
    dashboard = FearGreedDashboard()
    
    print("\\n📥 Đang lấy dữ liệu từ API...")
    if dashboard.fetch_data(limit=90):
        print("\\n🎨 Đang tạo báo cáo...")
        dashboard.create_full_report('test_bao_cao.png')
        dashboard.create_simple_gauge('test_dong_ho.png')
        print("\\n✅ Kiểm tra thành công!")
'''

backup_file('fear_greed_dashboard.py')
with open('fear_greed_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(DASHBOARD_CONTENT)

print("✅ Đã Việt hóa: fear_greed_dashboard.py")
print()

# ============================================================
# FILE 2: telegram_bot.py - Việt hóa messages
# ============================================================

print("📝 Đang Việt hóa telegram_bot.py...")

# Đọc file hiện tại
with open('telegram_bot.py', 'r', encoding='utf-8') as f:
    bot_content = f.read()

# Thay thế các chuỗi tiếng Anh
replacements = {
    # Emoji và giải thích
    '"💡 **Extreme Fear**': '"💡 **Sợ Hãi Cực Độ**',
    '"💡 **Fear**': '"💡 **Sợ Hãi**',
    '"💡 **Neutral**': '"💡 **Trung Lập**',
    '"💡 **Greed**': '"💡 **Tham Lam**',
    '"💡 **Extreme Greed**': '"💡 **Tham Lam Cực Độ**',
    
    # Giải thích chi tiết
    'Extreme Fear** - Thị trường quá bi quan': 'Sợ Hãi Cực Độ** - Thị trường quá bi quan',
    'Fear** - Nhà đầu tư đang thận trọng': 'Sợ Hãi** - Nhà đầu tư đang thận trọng',
    'Neutral** - Thị trường cân bằng': 'Trung Lập** - Thị trường cân bằng',
    'Greed** - Thị trường lạc quan': 'Tham Lam** - Thị trường lạc quan',
    'Extreme Greed** - FOMO đang lan tỏa': 'Tham Lam Cực Độ** - FOMO đang lan tỏa',
    
    # Các label khác
    'Fear & Greed Index': 'Chỉ Số Tâm Lý Thị Trường',
    'FEAR & GREED INDEX': 'CHỈ SỐ TÂM LÝ THỊ TRƯỜNG',
}

for old, new in replacements.items():
    bot_content = bot_content.replace(old, new)

backup_file('telegram_bot.py')
with open('telegram_bot.py', 'w', encoding='utf-8') as f:
    f.write(bot_content)

print("✅ Đã Việt hóa: telegram_bot.py")
print()

# ============================================================
# Tạo bảng tra cứu
# ============================================================

TRANSLATION_TABLE = '''
# 🇻🇳 BẢNG TRA CỨU TIẾNG VIỆT

## Thuật ngữ chính:

| Tiếng Anh | Tiếng Việt |
|-----------|------------|
| Fear & Greed Index | Chỉ Số Sợ Hãi & Tham Lam |
| Extreme Fear | Sợ Hãi Cực Độ |
| Fear | Sợ Hãi |
| Neutral | Trung Lập |
| Greed | Tham Lam |
| Extreme Greed | Tham Lam Cực Độ |

## Các phần trong báo cáo:

| Tiếng Anh | Tiếng Việt |
|-----------|------------|
| Yesterday | Hôm Qua |
| Last Week | Tuần Trước |
| Historical Chart | Biểu Đồ Lịch Sử |
| 30 Days History | Lịch Sử 30 Ngày |
| Current Value | Giá Trị Hiện Tại |
| Updated | Cập Nhật |
| Price | Giá |
| Increase | Tăng Giá |
| Decrease | Giảm Giá |

## Giải thích:

- **0-25**: Sợ Hãi Cực Độ - Cơ hội mua tốt
- **25-45**: Sợ Hãi - Thận trọng nhưng có thể mua
- **45-55**: Trung Lập - Quan sát
- **55-75**: Tham Lam - Cân nhắc chốt lời
- **75-100**: Tham Lam Cực Độ - Nên bán
'''

with open('BANG_DICH_TIENG_VIET.md', 'w', encoding='utf-8') as f:
    f.write(TRANSLATION_TABLE)

print("✅ Đã tạo: BANG_DICH_TIENG_VIET.md")
print()

print("=" * 70)
print(" ✅ HOÀN TẤT VIỆT HÓA!")
print("=" * 70)
print()
print("📋 ĐÃ CẬP NHẬT:")
print("   ✅ fear_greed_dashboard.py - 100% tiếng Việt")
print("   ✅ telegram_bot.py - Việt hóa messages")
print("   ✅ BANG_DICH_TIENG_VIET.md - Bảng tra cứu")
print()
print("🎨 CÁC THAY ĐỔI:")
print("   • Fear & Greed → Sợ Hãi & Tham Lam")
print("   • Extreme Fear → Sợ Hãi Cực Độ")
print("   • Fear → Sợ Hãi")
print("   • Neutral → Trung Lập")
print("   • Greed → Tham Lam")
print("   • Extreme Greed → Tham Lam Cực Độ")
print("   • Yesterday → Hôm Qua")
print("   • Last Week → Tuần Trước")
print("   • Current Value → Giá Trị Hiện Tại")
print()
print("🚀 CHẠY BOT:")
print("   python telegram_bot.py")
print()
print("📊 TEST NGAY:")
print("   Gửi /report cho bot để xem báo cáo tiếng Việt!")
print()