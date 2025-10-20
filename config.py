"""
config.py - Cấu hình cho Telegram Bot
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Cấu hình cho bot"""
    
    # Telegram credentials
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
    
    # Chat IDs
    OWNER_CHAT_ID = os.getenv('OWNER_CHAT_ID', 'YOUR_CHAT_ID')
    GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID', 'YOUR_GROUP_ID')
    
    # Chỉ owner mới được dùng bot
    ALLOWED_USERS = [int(OWNER_CHAT_ID)] if OWNER_CHAT_ID.isdigit() else []
    
    # API Settings
    API_URL = "https://api.alternative.me/fng/"
    API_TIMEOUT = 10
    API_RETRY = 3
    
    # File paths
    OUTPUT_DIR = "outputs"
    REPORTS_DIR = os.path.join(OUTPUT_DIR, "reports")
    GAUGES_DIR = os.path.join(OUTPUT_DIR, "gauges")
    DATA_DIR = os.path.join(OUTPUT_DIR, "data")
    LOGS_DIR = "logs"
    
    # Chart settings
    CHART_DPI = 150
    CHART_STYLE = 'dark_background'
    
    # Schedule settings
    SCHEDULE_TIMES = [
        "08:00",  # Sáng sớm
        "12:00",  # Trưa
        "16:00",  # Chiều
        "20:00",  # Tối
    ]
    
    # Message templates
    WELCOME_MESSAGE = """
🤖 **Chào mừng đến với Fear & Greed Index Bot!**

📊 Bot này giúp bạn theo dõi chỉ số Sợ hãi & Tham lam của thị trường Crypto

**Các lệnh có sẵn:**
/current - Xem chỉ số hiện tại
/gauge - Xem đồng hồ F&G
/report - Báo cáo đầy đủ
/history - Lịch sử 30 ngày
/stats - Thống kê 90 ngày
/signal - Tín hiệu mua/bán
/schedule - Quản lý lịch gửi tự động
/help - Trợ giúp

👤 Chỉ có chủ sở hữu mới dùng được bot này.
"""
    
    HELP_MESSAGE = """
📖 **HƯỚNG DẪN SỬ DỤNG**

**Lệnh cơ bản:**
• `/current` - Xem giá trị F&G hiện tại
• `/gauge` - Đồng hồ Fear & Greed
• `/report` - Báo cáo chi tiết với biểu đồ
• `/history [days]` - Lịch sử (mặc định 30 ngày)
• `/stats [days]` - Thống kê (mặc định 90 ngày)
• `/signal` - Phân tích tín hiệu mua/bán

**Gửi vào nhóm:**
• `/send_to_group` - Gửi báo cáo vào nhóm

**Lịch tự động:**
• `/schedule` - Xem lịch hiện tại
• `/schedule on` - Bật lịch tự động
• `/schedule off` - Tắt lịch tự động
• `/schedule status` - Trạng thái lịch

**Thời gian gửi tự động:** 8h, 12h, 16h, 20h hàng ngày

💡 **Tips:** 
- Extreme Fear (0-25): Cơ hội mua tốt
- Extreme Greed (75-100): Nên chốt lời
"""
    
    @classmethod
    def create_directories(cls):
        """Tạo các thư mục cần thiết"""
        dirs = [
            cls.OUTPUT_DIR,
            cls.REPORTS_DIR,
            cls.GAUGES_DIR,
            cls.DATA_DIR,
            cls.LOGS_DIR
        ]
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
    
    @classmethod
    def validate_config(cls):
        """Kiểm tra cấu hình"""
        errors = []
        
        if cls.BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
            errors.append("❌ Chưa cấu hình TELEGRAM_BOT_TOKEN")
        
        if cls.OWNER_CHAT_ID == 'YOUR_CHAT_ID':
            errors.append("❌ Chưa cấu hình OWNER_CHAT_ID")
        
        if errors:
            print("\n".join(errors))
            print("\n⚠️  Vui lòng chỉnh sửa file .env với thông tin của bạn!")
            return False
        
        return True


if __name__ == "__main__":
    print("🔧 Kiểm tra cấu hình...")
    Config.create_directories()
    print("✅ Đã tạo các thư mục")
    
    if Config.validate_config():
        print("✅ Cấu hình hợp lệ!")
        print(f"📱 Bot Token: {Config.BOT_TOKEN[:20]}...")
        print(f"👤 Owner Chat ID: {Config.OWNER_CHAT_ID}")
        if Config.GROUP_CHAT_ID != 'YOUR_GROUP_ID':
            print(f"👥 Group Chat ID: {Config.GROUP_CHAT_ID}")
    else:
        print("❌ Cấu hình chưa đầy đủ!")
