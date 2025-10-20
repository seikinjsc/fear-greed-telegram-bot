"""
telegram_bot.py - Telegram Bot chính cho Chỉ Số Tâm Lý Thị Trường (FIXED)
"""

import logging
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    CallbackQueryHandler,
    ContextTypes,
)
from telegram.constants import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from config import Config
from fear_greed_dashboard import FearGreedDashboard

# ===== FIX: Tạo thư mục TRƯỚC KHI setup logging =====
Config.create_directories()

# Setup logging SAU KHI đã tạo thư mục
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(os.path.join(Config.LOGS_DIR, 'bot.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Khởi tạo scheduler KHÔNG start ngay
scheduler = AsyncIOScheduler()
dashboard = FearGreedDashboard()


def owner_only(func):
    """Decorator để chỉ cho phép owner sử dụng"""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id not in Config.ALLOWED_USERS:
            await update.message.reply_text(
                "🚫 **Truy cập bị từ chối**\n\n"
                "Bot này chỉ dành cho chủ sở hữu.",
                parse_mode=ParseMode.MARKDOWN
            )
            logger.warning(f"Unauthorized access attempt by user {user_id}")
            return
        
        return await func(update, context)
    return wrapper


@owner_only
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler cho /start"""
    await update.message.reply_text(
        Config.WELCOME_MESSAGE,
        parse_mode=ParseMode.MARKDOWN
    )
    logger.info(f"User {update.effective_user.id} started bot")


@owner_only
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler cho /help"""
    await update.message.reply_text(
        Config.HELP_MESSAGE,
        parse_mode=ParseMode.MARKDOWN
    )


@owner_only
async def current_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler cho /current"""
    await update.message.reply_text("⏳ Đang lấy dữ liệu...")
    
    try:
        logger.info("Attempting to fetch data...")
        fetch_result = dashboard.fetch_data(limit=1)
        logger.info(f"Fetch result: {fetch_result}")
        
        if fetch_result:
            value = dashboard.current_value
            classification = dashboard.current_classification
            color_emoji = get_emoji_for_value(value)
            
            message = f"""
{color_emoji} **CHỈ SỐ TÂM LÝ THỊ TRƯỜNG**

**Giá trị:** `{value}/100`
**Phân loại:** `{classification}`
**Thời gian:** {datetime.now().strftime('%d/%m/%Y %H:%M')}

{get_interpretation(value)}
"""
            
            keyboard = [
                [
                    InlineKeyboardButton("📊 Xem Gauge", callback_data='show_gauge'),
                    InlineKeyboardButton("📈 Xem Report", callback_data='show_report')
                ],
                [
                    InlineKeyboardButton("📤 Gửi vào nhóm", callback_data='send_to_group')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                message,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
            
            logger.info(f"Current value sent: {value}")
        else:
            error_msg = "❌ Không thể lấy dữ liệu. Vui lòng thử lại sau."
            logger.error(f"Failed to fetch data. Dashboard state: {dashboard.__dict__}")
            await update.message.reply_text(error_msg)
    
    except Exception as e:
        logger.error(f"Error in current_command: {e}", exc_info=True)
        await update.message.reply_text(f"❌ Lỗi: {str(e)}")


@owner_only
async def gauge_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler cho /gauge"""
    logger.info("=== GAUGE COMMAND STARTED ===")
    await update.message.reply_text("⏳ Đang tạo gauge chart...")
    await execute_gauge_logic(update.message)


@owner_only
async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler cho /report"""
    logger.info("=== REPORT COMMAND STARTED ===")
    await update.message.reply_text("⏳ Đang tạo báo cáo đầy đủ...")
    await execute_report_logic(update.message)


@owner_only
async def signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler cho /signal"""
    await update.message.reply_text("⏳ Đang phân tích tín hiệu...")
    await execute_signal_logic(update.message)


@owner_only
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler cho /stats"""
    await update.message.reply_text("⏳ Đang tính toán thống kê...")
    
    days = 90
    if context.args and context.args[0].isdigit():
        days = int(context.args[0])
    
    await execute_stats_logic(update.message, days=days)


@owner_only
async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler cho /schedule"""
    if not context.args:
        jobs = scheduler.get_jobs()
        status = "🟢 Đang bật" if jobs else "🔴 Đang tắt"
        
        message = f"""
⏰ **LỊCH GỬI TỰ ĐỘNG**

**Trạng thái:** {status}
**Số job:** {len(jobs)}

**Thời gian gửi:**
"""
        for time in Config.SCHEDULE_TIMES:
            message += f"• {time}\n"
        
        message += "\n**Lệnh:**\n"
        message += "• `/schedule on` - Bật lịch\n"
        message += "• `/schedule off` - Tắt lịch\n"
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
        
        # Thêm gợi ý lệnh tiếp theo
        await update.message.reply_text(
            "✅ Bạn muốn làm gì tiếp theo?",
            reply_markup=get_next_commands_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif context.args[0] == 'on':
        setup_schedule(context)
        await update.message.reply_text(
            "✅ Đã bật lịch gửi tự động!\n\n"
            f"Bot sẽ gửi báo cáo vào nhóm lúc: {', '.join(Config.SCHEDULE_TIMES)}",
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Schedule enabled")
        
        # Thêm gợi ý lệnh tiếp theo
        await update.message.reply_text(
            "✅ Bạn muốn làm gì tiếp theo?",
            reply_markup=get_next_commands_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif context.args[0] == 'off':
        scheduler.remove_all_jobs()
        await update.message.reply_text(
            "✅ Đã tắt lịch gửi tự động!",
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Schedule disabled")
        
        # Thêm gợi ý lệnh tiếp theo
        await update.message.reply_text(
            "✅ Bạn muốn làm gì tiếp theo?",
            reply_markup=get_next_commands_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler cho inline keyboard buttons"""
    query = update.callback_query
    await query.answer()
    
    # Kiểm tra quyền owner
    user_id = update.effective_user.id
    if user_id not in Config.ALLOWED_USERS:
        await query.message.reply_text("🚫 Bạn không có quyền sử dụng chức năng này.")
        return
    
    # Xử lý các lệnh từ keyboard gợi ý
    if query.data == 'cmd_gauge':
        await query.message.reply_text("⏳ Đang tạo gauge chart...")
        await execute_gauge_logic(query.message)
        return
    
    elif query.data == 'cmd_report':
        await query.message.reply_text("⏳ Đang tạo báo cáo đầy đủ...")
        await execute_report_logic(query.message)
        return
    
    elif query.data == 'cmd_signal':
        await query.message.reply_text("⏳ Đang phân tích tín hiệu...")
        await execute_signal_logic(query.message)
        return
    
    elif query.data == 'cmd_stats':
        await query.message.reply_text("⏳ Đang tính toán thống kê...")
        await execute_stats_logic(query.message, days=90)
        return
    
    elif query.data == 'cmd_schedule':
        await execute_schedule_info(query.message)
        return
    
    elif query.data == 'cmd_help':
        await query.message.reply_text(
            Config.HELP_MESSAGE,
            parse_mode=ParseMode.MARKDOWN
        )
        # Thêm gợi ý lệnh tiếp theo
        await query.message.reply_text(
            "✅ Bạn muốn làm gì tiếp theo?",
            reply_markup=get_next_commands_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Xử lý nút từ /current
    if query.data == 'show_gauge':
        await query.message.reply_text("⏳ Đang tạo gauge chart...")
        await execute_gauge_logic(query.message)
    
    elif query.data == 'show_report':
        await query.message.reply_text("⏳ Đang tạo báo cáo đầy đủ...")
        await execute_report_logic(query.message)
    
    elif query.data == 'send_to_group':
        try:
            await send_to_group(context)
            await query.message.reply_text("✅ Đã gửi vào nhóm!")
            # Thêm gợi ý lệnh tiếp theo
            await query.message.reply_text(
                "✅ Bạn muốn làm gì tiếp theo?",
                reply_markup=get_next_commands_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            logger.error(f"Error sending to group from button: {e}", exc_info=True)
            await query.message.reply_text(f"❌ Lỗi khi gửi vào nhóm: {str(e)}")


async def execute_gauge_logic(message):
    """Logic tạo gauge chart - dùng chung cho command và button"""
    try:
        logger.info("=== GAUGE EXECUTION ===")
        if dashboard.fetch_data(limit=7):
            filename = os.path.join(
                Config.GAUGES_DIR, 
                f"gauge_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
            
            dashboard.create_simple_gauge(save_path=filename)
            
            caption = f"""
📊 **Chỉ Số Tâm Lý Thị Trường**
Giá trị: {dashboard.current_value} - {dashboard.current_classification}
Cập nhật: {datetime.now().strftime('%d/%m/%Y %H:%M')}
"""
            
            with open(filename, 'rb') as photo:
                await message.reply_photo(
                    photo=photo,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN
                )
            
            os.remove(filename)
            logger.info("Gauge sent successfully")
            
            # Thêm gợi ý lệnh tiếp theo
            await message.reply_text(
                "✅ **Hoàn tất!** Bạn muốn làm gì tiếp theo?",
                reply_markup=get_next_commands_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await message.reply_text("❌ Không thể tạo gauge chart.")
    
    except Exception as e:
        logger.error(f"Error in gauge execution: {e}", exc_info=True)
        await message.reply_text(f"❌ Lỗi: {str(e)}")


async def execute_report_logic(message):
    """Logic tạo report - dùng chung cho command và button"""
    try:
        logger.info("=== REPORT EXECUTION ===")
        if dashboard.fetch_data(limit=90):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = os.path.join(Config.REPORTS_DIR, f"report_{timestamp}.png")
            data_file = os.path.join(Config.DATA_DIR, f"data_{timestamp}.csv")
            
            dashboard.create_full_report(save_path=report_file)
            dashboard.data.to_csv(data_file, index=False)
            
            caption = f"""
📊 **BÁO CÁO CHỈ SỐ TÂM LÝ THỊ TRƯỜNG**

**Hiện tại:** {dashboard.current_value} - {dashboard.current_classification}
**Cập nhật:** {datetime.now().strftime('%d/%m/%Y %H:%M')}

{get_interpretation(dashboard.current_value)}
"""
            
            with open(report_file, 'rb') as photo:
                await message.reply_photo(
                    photo=photo,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN
                )
            
            with open(data_file, 'rb') as document:
                await message.reply_document(
                    document=document,
                    filename=f"fear_greed_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    caption="📄 Dữ liệu thô (CSV)"
                )
            
            os.remove(report_file)
            os.remove(data_file)
            logger.info("Report sent successfully")
            
            # Thêm gợi ý lệnh tiếp theo
            await message.reply_text(
                "✅ **Hoàn tất!** Bạn muốn làm gì tiếp theo?",
                reply_markup=get_next_commands_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await message.reply_text("❌ Không thể tạo báo cáo.")
    
    except Exception as e:
        logger.error(f"Error in report execution: {e}", exc_info=True)
        await message.reply_text(f"❌ Lỗi: {str(e)}")


async def execute_signal_logic(message):
    """Logic phân tích tín hiệu - dùng chung cho command và button"""
    try:
        if dashboard.fetch_data(limit=30):
            value = dashboard.current_value
            avg_7 = dashboard.data.tail(7)['value'].mean()
            avg_30 = dashboard.data.tail(30)['value'].mean()
            
            if value <= 25:
                signal = "🟢 MUA MẠNH"
                reason = "Extreme Fear - Thị trường quá bi quan"
                action = "Cơ hội tích lũy tốt"
            elif value <= 40:
                signal = "🟢 MUA"
                reason = "Fear - Tâm lý thận trọng"
                action = "Có thể bắt đầu mua DCA"
            elif value <= 60:
                signal = "🟡 GIỮ"
                reason = "Neutral - Thị trường cân bằng"
                action = "Quan sát thêm"
            elif value <= 75:
                signal = "🔴 CHỐT LỜI BỘ PHẬN"
                reason = "Greed - Tâm lý lạc quan"
                action = "Nên chốt lời 20-30%"
            else:
                signal = "🔴 BÁN"
                reason = "Extreme Greed - FOMO đang lan tỏa"
                action = "Nên chốt lời mạnh"
            
            response = f"""
🎯 **TÍN HIỆU GIAO DỊCH**

**Chỉ số hiện tại:** {value}
**Tín hiệu:** {signal}

**Phân tích:**
• Lý do: {reason}
• Hành động: {action}

**Xu hướng:**
• Trung bình 7 ngày: {avg_7:.1f}
• Trung bình 30 ngày: {avg_30:.1f}
• Xu hướng: {'📈 Tăng' if value > avg_7 else '📉 Giảm'}

⚠️ **Lưu ý:** Đây chỉ là tín hiệu tham khảo.
"""
            
            await message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
            logger.info(f"Signal analysis sent: {signal}")
            
            # Thêm gợi ý lệnh tiếp theo
            await message.reply_text(
                "✅ **Hoàn tất!** Bạn muốn làm gì tiếp theo?",
                reply_markup=get_next_commands_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await message.reply_text("❌ Không thể phân tích tín hiệu.")
    
    except Exception as e:
        logger.error(f"Error in signal execution: {e}", exc_info=True)
        await message.reply_text(f"❌ Lỗi: {str(e)}")


async def execute_stats_logic(message, days=90):
    """Logic thống kê - dùng chung cho command và button"""
    try:
        if dashboard.fetch_data(limit=days):
            df = dashboard.data
            stats = df['value'].describe()
            
            # SỬ DỤNG CỘT TIẾNG VIỆT
            counts = df['value_classification_vi'].value_counts()
            
            response = f"""
📊 **THỐNG KÊ {days} NGÀY**

**Chỉ số:**
• Trung bình: {stats['mean']:.1f}
• Trung vị: {stats['50%']:.1f}
• Độ lệch chuẩn: {stats['std']:.1f}
• Thấp nhất: {stats['min']:.0f}
• Cao nhất: {stats['max']:.0f}

**Phân phối:**
"""
            for classification, count in counts.items():
                percentage = (count / len(df)) * 100
                response += f"• {classification}: {count} ngày ({percentage:.1f}%)\n"
            
            await message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
            logger.info(f"Stats sent for {days} days")
            
            # Thêm gợi ý lệnh tiếp theo
            await message.reply_text(
                "✅ **Hoàn tất!** Bạn muốn làm gì tiếp theo?",
                reply_markup=get_next_commands_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await message.reply_text("❌ Không thể tính thống kê.")
    
    except Exception as e:
        logger.error(f"Error in stats execution: {e}", exc_info=True)
        await message.reply_text(f"❌ Lỗi: {str(e)}")


async def execute_schedule_info(message):
    """Hiển thị thông tin lịch - dùng chung cho command và button"""
    try:
        jobs = scheduler.get_jobs()
        status = "🟢 Đang bật" if jobs else "🔴 Đang tắt"
        
        response = f"""
⏰ **LỊCH GỬI TỰ ĐỘNG**

**Trạng thái:** {status}
**Số job:** {len(jobs)}

**Thời gian gửi:**
"""
        for time in Config.SCHEDULE_TIMES:
            response += f"• {time}\n"
        
        response += "\n**Lệnh:**\n"
        response += "• `/schedule on` - Bật lịch\n"
        response += "• `/schedule off` - Tắt lịch\n"
        
        await message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
        
        # Thêm gợi ý lệnh tiếp theo
        await message.reply_text(
            "✅ Bạn muốn làm gì tiếp theo?",
            reply_markup=get_next_commands_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error(f"Error in schedule info: {e}", exc_info=True)
        await message.reply_text(f"❌ Lỗi: {str(e)}")


async def send_scheduled_report(context: ContextTypes.DEFAULT_TYPE):
    """Gửi báo cáo theo lịch"""
    logger.info("Sending scheduled report...")
    try:
        await send_to_group(context)
    except Exception as e:
        logger.error(f"Error sending scheduled report: {e}")


async def send_to_group(context: ContextTypes.DEFAULT_TYPE):
    """Gửi báo cáo vào nhóm"""
    if Config.GROUP_CHAT_ID == 'YOUR_GROUP_ID':
        logger.warning("Group chat ID not configured")
        return
    
    try:
        if dashboard.fetch_data(limit=90):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = os.path.join(Config.REPORTS_DIR, f"report_{timestamp}.png")
            
            dashboard.create_full_report(save_path=report_file)
            
            caption = f"""
📊 **BÁO CÁO CHỈ SỐ TÂM LÝ THỊ TRƯỜNG**
⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}

**Hiện tại:** {dashboard.current_value} - {dashboard.current_classification}

{get_interpretation(dashboard.current_value)}

#FearGreed #Crypto #Analysis
"""
            
            with open(report_file, 'rb') as photo:
                await context.bot.send_photo(
                    chat_id=Config.GROUP_CHAT_ID,
                    photo=photo,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN
                )
            
            os.remove(report_file)
            logger.info("Report sent to group successfully")
    
    except Exception as e:
        logger.error(f"Error sending to group: {e}")


def setup_schedule(context: ContextTypes.DEFAULT_TYPE):
    """Thiết lập lịch gửi tự động"""
    scheduler.remove_all_jobs()
    
    for time_str in Config.SCHEDULE_TIMES:
        hour, minute = map(int, time_str.split(':'))
        scheduler.add_job(
            send_scheduled_report,
            trigger=CronTrigger(hour=hour, minute=minute),
            args=[context],
            id=f'report_{time_str}',
            replace_existing=True
        )
    
    logger.info(f"Scheduled {len(Config.SCHEDULE_TIMES)} jobs")


def get_next_commands_keyboard():
    """Tạo keyboard gợi ý các lệnh tiếp theo"""
    keyboard = [
        [
            InlineKeyboardButton("📊 Gauge", callback_data='cmd_gauge'),
            InlineKeyboardButton("📈 Report", callback_data='cmd_report'),
            InlineKeyboardButton("🎯 Signal", callback_data='cmd_signal')
        ],
        [
            InlineKeyboardButton("📉 Stats", callback_data='cmd_stats'),
            InlineKeyboardButton("⏰ Schedule", callback_data='cmd_schedule'),
            InlineKeyboardButton("ℹ️ Help", callback_data='cmd_help')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_emoji_for_value(value):
    """Lấy emoji dựa trên giá trị"""
    if value <= 25:
        return "😱"
    elif value <= 45:
        return "😰"
    elif value <= 55:
        return "😐"
    elif value <= 75:
        return "😊"
    else:
        return "🤑"


def get_interpretation(value):
    """Giải thích giá trị"""
    if value <= 25:
        return "💡 **Sợ Hãi Cực Độ** - Thị trường quá bi quan, có thể là cơ hội mua tốt!"
    elif value <= 45:
        return "💡 **Sợ Hãi** - Nhà đầu tư đang thận trọng, cân nhắc tích lũy."
    elif value <= 55:
        return "💡 **Trung Lập** - Thị trường cân bằng, quan sát thêm."
    elif value <= 75:
        return "💡 **Tham Lam** - Thị trường lạc quan, cân nhắc chốt lời bộ phận."
    else:
        return "💡 **Tham Lam Cực Độ** - FOMO đang lan tỏa, cẩn thận với điều chỉnh!"


async def send_bot_status(application, status: str):
    """Gửi thông báo trạng thái bot"""
    try:
        timestamp = datetime.now().strftime('%d/%m/%Y lúc %H:%M:%S')
        
        if status == "started":
            message = f"""
🟢 **BOT ĐÃ KHỞI ĐỘNG THÀNH CÔNG**

⏰ **Thời gian:** {timestamp}
📊 **Trạng thái:** Đang hoạt động
🔄 **Scheduler:** Đã kích hoạt

✅ **Bot sẵn sàng nhận lệnh!**

📋 **Các lệnh có sẵn:**
• /current - Xem chỉ số hiện tại
• /report - Báo cáo đầy đủ
• /signal - Tín hiệu giao dịch
• /schedule on - Bật gửi tự động

💡 Gửi /help để xem hướng dẫn chi tiết.
"""
        elif status == "stopped":
            message = f"""
🔴 **BOT ĐÃ DỪNG HOẠT ĐỘNG**

⏰ **Thời gian:** {timestamp}
📊 **Trạng thái:** Đã tắt

⚠️ Bot không còn hoạt động nữa.
"""
        else:
            message = f"ℹ️ **{status}** - {timestamp}"
        
        # Gửi cho owner
        await application.bot.send_message(
            chat_id=Config.OWNER_CHAT_ID,
            text=message,
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Gửi vào group nếu có
        if Config.GROUP_CHAT_ID != 'YOUR_GROUP_ID':
            group_message = f"🔔 **Thông báo:** Bot {status} lúc {timestamp}"
            await application.bot.send_message(
                chat_id=Config.GROUP_CHAT_ID,
                text=group_message,
                parse_mode=ParseMode.MARKDOWN
            )
        
        logger.info(f"Status notification sent: {status}")
    except Exception as e:
        logger.error(f"Error sending status: {e}")


async def post_init(application: Application):
    """Callback sau khi application khởi tạo - start scheduler ở đây"""
    scheduler.start()
    logger.info("Scheduler started successfully")
    
    # Gửi thông báo bot đã khởi động
    await send_bot_status(application, "started")


def main():
    """Khởi động bot"""
    print("=" * 60)
    print("🤖 CHỈ SỐ TÂM LÝ THỊ TRƯỜNG TELEGRAM BOT")
    print("=" * 60)
    
    if not Config.validate_config():
        return
    
    # Không cần gọi lại vì đã gọi ở đầu file
    # Config.create_directories()
    
    # Tạo application
    application = Application.builder().token(Config.BOT_TOKEN).build()
    
    # Thêm handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("current", current_command))
    application.add_handler(CommandHandler("gauge", gauge_command))
    application.add_handler(CommandHandler("report", report_command))
    application.add_handler(CommandHandler("signal", signal_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("schedule", schedule_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Thêm post_init callback để start scheduler SAU KHI event loop đã chạy
    application.post_init = post_init
    
    print("✅ Bot đã sẵn sàng!")
    print(f"👤 Owner: {Config.OWNER_CHAT_ID}")
    print(f"👥 Group: {Config.GROUP_CHAT_ID}")
    print("\n💬 Gửi /start cho bot để bắt đầu!")
    print("⏰ Scheduler sẽ khởi động khi bot chạy")
    print("\nNhấn Ctrl+C để dừng bot\n")
    
    # Chạy bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()