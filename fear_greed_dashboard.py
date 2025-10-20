"""
fear_greed_dashboard.py - Dashboard vẽ biểu đồ Chỉ Báo Tâm Lý (100% Tiếng Việt)
"""

import requests
import pandas as pd
import matplotlib
matplotlib.use('Agg')
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
    
    def get_text_color_for_classification(self, classification_vi):
        """Lấy màu chữ dựa trên phân loại"""
        colors = {
            'Sợ Hãi Cực Độ': '#ff5252',
            'Sợ Hãi': '#ffa726',
            'Trung Lập': '#ffeb3b',
            'Tham Lam': '#81c784',
            'Tham Lam Cực Độ': '#66bb6a'
        }
        return colors.get(classification_vi, '#ffffff')
    
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
        
        # Hiển thị số - DI CHUYỂN XUỐNG DƯỚI VÀ GIẢM KÍCH THƯỚC
        ax.text(0, -0.25, f'{value}', 
                fontsize=52, fontweight='bold', ha='center', va='center',
                color='white', zorder=25)
        
        # Hiển thị phân loại tiếng Việt - PHÓNG TO, TÔ MÀU, IN ĐẬM
        text_color = self.get_text_color_for_classification(classification_vi)
        ax.text(0, -0.55, classification_vi, 
                fontsize=20, ha='center', va='center',
                color=text_color, zorder=25, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', 
                         facecolor='#1a1a1a', 
                         edgecolor=text_color,
                         linewidth=2.5, alpha=0.8))
        
        # Label đầu cuối
        ax.text(-1.15, -0.1, '0', fontsize=13, color='#666666', ha='center')
        ax.text(1.15, -0.1, '100', fontsize=13, color='#666666', ha='center')
    
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
        
        # Box 1: Hôm qua - GIẢM KÍCH THƯỚC
        rect1 = FancyBboxPatch((0.5, 6.8), 4, 2.5, 
                               boxstyle="round,pad=0.15", 
                               facecolor='#2a2a2a', 
                               edgecolor='#404040',
                               linewidth=2)
        ax.add_patch(rect1)
        
        ax.text(2.5, 8.9, 'Hôm Qua', 
                fontsize=12, ha='center', color='#999999', fontweight='bold')
        ax.text(2.5, 8.4, yesterday_class_vi, 
                fontsize=9, ha='center', color='#ffa726')
        ax.text(2.5, 7.5, f'{yesterday_value}', 
                fontsize=32, ha='center', color='white', fontweight='bold')
        
        # Box 2: Tuần trước - GIẢM KÍCH THƯỚC
        rect2 = FancyBboxPatch((5.5, 6.8), 4, 2.5, 
                               boxstyle="round,pad=0.15", 
                               facecolor='#2a2a2a', 
                               edgecolor='#404040',
                               linewidth=2)
        ax.add_patch(rect2)
        
        ax.text(7.5, 8.9, 'Tuần Trước', 
                fontsize=12, ha='center', color='#999999', fontweight='bold')
        ax.text(7.5, 8.4, week_class_vi, 
                fontsize=9, ha='center', color='#66bb6a')
        ax.text(7.5, 7.5, f'{int(week_avg)}', 
                fontsize=32, ha='center', color='white', fontweight='bold')
        
        # Câu hỏi - TĂNG KHOẢNG CÁCH
        ax.text(5, 6.0, 'Ban nghĩ gì về Bitcoin hôm nay?', 
                fontsize=12, ha='center', color='white', fontweight='bold')
        
        # Nút Giảm
        rect_down = FancyBboxPatch((1, 4.4), 3.5, 1.1, 
                                   boxstyle="round,pad=0.08", 
                                   facecolor='#d32f2f', 
                                   edgecolor='none')
        ax.add_patch(rect_down)
        ax.text(2.75, 5.0, '📉 Giảm Giá', 
                fontsize=13, ha='center', va='center', 
                color='white', fontweight='bold')
        
        # Nút Tăng
        rect_up = FancyBboxPatch((5.5, 4.4), 3.5, 1.1, 
                                 boxstyle="round,pad=0.08", 
                                 facecolor='#2e7d32', 
                                 edgecolor='none')
        ax.add_patch(rect_up)
        ax.text(7.25, 5.0, '📈 Tăng Giá', 
                fontsize=13, ha='center', va='center', 
                color='white', fontweight='bold')
        
        # Mô tả - GIẢM KÍCH THƯỚC VÀ TĂNG KHOẢNG CÁCH
        description = ("Chỉ số dao động từ 0 (Sợ hãi tối đa) đến 100 (Tham lam cực độ). "
                      "Phản ánh tâm lý và cảm xúc của nhà đầu tư crypto. "
                      "Dữ liệu được tổng hợp từ nhiều nguồn để phân tích chính xác xu hướng thị trường.")
        
        ax.text(5, 2.5, description, 
                fontsize=8.5, ha='center', va='top', 
                color='#999999', wrap=True, 
                multialignment='center',
                bbox=dict(boxstyle='round,pad=0.5', 
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
        ax.set_xlabel('Ngày Tháng', fontsize=13, color='#999999', labelpad=12)
        ax.set_ylabel('Chỉ Số Tâm Lý', fontsize=13, color='#999999', labelpad=12)
        ax.set_title('Lịch Sử 30 Ngày Gần Nhất', 
                    fontsize=15, color='white', fontweight='bold', pad=15)
        
        # Grid
        ax.grid(True, alpha=0.15, linestyle='--', linewidth=0.5)
        ax.set_ylim(0, 100)
        
        # Vùng màu nền
        ax.axhspan(0, 25, alpha=0.08, color='#d32f2f', zorder=1)
        ax.axhspan(25, 45, alpha=0.08, color='#ff9800', zorder=1)
        ax.axhspan(45, 55, alpha=0.08, color='#fdd835', zorder=1)
        ax.axhspan(55, 75, alpha=0.08, color='#66bb6a', zorder=1)
        ax.axhspan(75, 100, alpha=0.08, color='#2e7d32', zorder=1)
        
        # Label tiếng Việt cho các vùng - GIẢM KÍCH THƯỚC
        ax.text(df['timestamp'].iloc[1], 12, 'Sợ Hãi Cực Độ', 
                fontsize=8, color='#d32f2f', alpha=0.7, fontweight='bold')
        ax.text(df['timestamp'].iloc[1], 35, 'Sợ Hãi', 
                fontsize=8, color='#ff9800', alpha=0.7, fontweight='bold')
        ax.text(df['timestamp'].iloc[1], 50, 'Trung Lập', 
                fontsize=8, color='#fdd835', alpha=0.7, fontweight='bold')
        ax.text(df['timestamp'].iloc[1], 65, 'Tham Lam', 
                fontsize=8, color='#66bb6a', alpha=0.7, fontweight='bold')
        ax.text(df['timestamp'].iloc[1], 87, 'Tham Lam Cực Độ', 
                fontsize=8, color='#2e7d32', alpha=0.7, fontweight='bold')
        
        # Format trục X - GIẢM SỐ LABELS VÀ TĂNG ROTATION
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=4))  # Thay đổi từ 3 thành 4
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        
        plt.setp(ax.xaxis.get_majorticklabels(), 
                rotation=60, ha='right', fontsize=10)  # Tăng rotation từ 45 thành 60
        
        ax.tick_params(colors='#666666', labelsize=10, length=6, width=1.5)
        
        for spine in ax.spines.values():
            spine.set_color('#333333')
            spine.set_linewidth(1.5)
    
    def create_full_report(self, save_path='bao_cao_tam_ly.png'):
        """Tạo báo cáo đầy đủ"""
        # TĂNG KÍCH THƯỚC FIGURE
        fig = plt.figure(figsize=(24, 15), facecolor='#0d0d0d')
        
        # ĐIỀU CHỈNH SPACING
        gs = fig.add_gridspec(4, 2, 
                             height_ratios=[0.12, 0.8, 0.08, 1.2],
                             hspace=0.25, wspace=0.35,  # Tăng hspace và wspace
                             left=0.08, right=0.92, top=0.94, bottom=0.08)
        
        # Tiêu đề chính - GIẢM KÍCH THƯỚC VÀ DI CHUYỂN XUỐNG
        fig.text(0.5, 0.975, 'CHỈ SỐ SỢ HÃI VÀ THAM LAM - THỊ TRƯỜNG TIỀN MÃ HÓA', 
                fontsize=22, fontweight='bold', ha='center', 
                color='white', va='top')
        
        # Thông tin cập nhật - TĂNG KHOẢNG CÁCH
        fig.text(0.5, 0.945, 
                f'Cập nhật: {datetime.now().strftime("%d/%m/%Y lúc %H:%M")} | ' + 
                f'Hiện tại: {self.current_value} điểm - {self.current_classification_vi}',
                fontsize=12, ha='center', color='#999999', va='top')
        
        # Vẽ gauge
        ax1 = fig.add_subplot(gs[1, 0])
        self.draw_gauge_chart(ax1)
        
        # Vẽ stats boxes
        ax2 = fig.add_subplot(gs[1, 1])
        self.draw_stats_boxes(ax2)
        
        # Vẽ biểu đồ lịch sử
        ax3 = fig.add_subplot(gs[3, :])
        self.draw_historical_chart(ax3)
        
        # TĂNG DPI ĐỂ CHỮ RÕ HƠN
        plt.savefig(save_path, dpi=180, facecolor='#0d0d0d', 
                   edgecolor='none', bbox_inches='tight', pad_inches=0.3)
        print(f"\n✅ Đã lưu báo cáo: {save_path}")
        plt.close()
    
    def create_simple_gauge(self, save_path='dong_ho_tam_ly.png'):
        """Tạo gauge đơn giản"""
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#0d0d0d')
        self.draw_gauge_chart(ax)
        
        # GIẢM KÍCH THƯỚC VÀ TĂNG KHOẢNG CÁCH
        fig.text(0.5, 0.92, 'Chỉ Số Sợ Hãi & Tham Lam', 
                fontsize=18, fontweight='bold', ha='center', 
                color='white', va='top')
        fig.text(0.5, 0.87, f'{self.current_classification_vi} - {self.current_value} điểm', 
                fontsize=13, ha='center', color='#999999', va='top')
        
        plt.savefig(save_path, dpi=150, facecolor='#0d0d0d', 
                   edgecolor='none', bbox_inches='tight', pad_inches=0.2)
        print(f"✅ Đã lưu đồng hồ: {save_path}")
        plt.close()


if __name__ == "__main__":
    print("=" * 60)
    print("CHỈ SỐ SỢ HÃI & THAM LAM - KIỂM TRA")
    print("=" * 60)
    
    dashboard = FearGreedDashboard()
    
    print("\n🔥 Đang lấy dữ liệu từ API...")
    if dashboard.fetch_data(limit=90):
        print("\n🎨 Đang tạo báo cáo...")
        dashboard.create_full_report('test_bao_cao.png')
        dashboard.create_simple_gauge('test_dong_ho.png')
        print("\n✅ Kiểm tra thành công!")