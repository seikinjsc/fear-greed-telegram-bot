"""
setup_venv.py - Tạo môi trường ảo và cài đặt thư viện
Chạy lệnh: python setup_venv.py
"""

import subprocess
import sys
import os
import platform

VENV_NAME = "venv_chi_bao_tam_ly"

REQUIRED_PACKAGES = [
    'python-dotenv==1.0.0',
    'python-telegram-bot==22.5',
    'APScheduler==3.11.0',
    'requests==2.31.0',
    'pandas==2.3.3',
    'matplotlib==3.10.6',
    'seaborn==0.13.2',
    'numpy==2.2.6',
]

def print_header(text):
    print("\n" + "=" * 70)
    print(f" {text}")
    print("=" * 70 + "\n")

def run_command(command, description):
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Thành công!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Thất bại!")
        print(f"   Lỗi: {e.stderr}")
        return False

def check_venv_exists():
    return os.path.exists(VENV_NAME)

def create_virtual_environment():
    print_header("🔧 TẠO MÔI TRƯỜNG ẢO")
    
    if check_venv_exists():
        print(f"⚠️  Môi trường ảo \'{VENV_NAME}\' đã tồn tại!")
        print(f"❓ Bạn có muốn xóa và tạo lại không? (y/n): ", end='')
        choice = input().strip().lower()
        
        if choice == 'y' or choice == 'yes':
            print(f"\n🗑️  Đang xóa môi trường ảo cũ...")
            if platform.system() == "Windows":
                run_command(f'rmdir /s /q {VENV_NAME}', 'Xóa môi trường ảo')
            else:
                run_command(f'rm -rf {VENV_NAME}', 'Xóa môi trường ảo')
        else:
            print("\n✅ Giữ nguyên môi trường ảo hiện tại")
            return True
    
    python_cmd = sys.executable
    success = run_command(f'\"{python_cmd}\" -m venv {VENV_NAME}', f'Tạo môi trường ảo {VENV_NAME}')
    
    if success:
        print(f"\n✨ Môi trường ảo \'{VENV_NAME}\' đã được tạo!")
    
    return success

def get_pip_command():
    if platform.system() == "Windows":
        return os.path.join(VENV_NAME, "Scripts", "pip.exe")
    else:
        return os.path.join(VENV_NAME, "bin", "pip")

def upgrade_pip():
    print_header("📦 NÂNG CẤP PIP")
    pip_cmd = get_pip_command()
    success = run_command(f'\"{pip_cmd}\" install --upgrade pip', 'Nâng cấp pip')
    return success

def install_packages():
    print_header("📚 CÀI ĐẶT THƯ VIỆN")
    
    pip_cmd = get_pip_command()
    
    print(f"📋 Danh sách {len(REQUIRED_PACKAGES)} thư viện:")
    for pkg in REQUIRED_PACKAGES:
        print(f"   • {pkg}")
    print()
    
    success_count = 0
    fail_count = 0
    failed_packages = []
    
    for i, package in enumerate(REQUIRED_PACKAGES, 1):
        pkg_name = package.split('==')[0]
        print(f"[{i}/{len(REQUIRED_PACKAGES)}] Đang cài {pkg_name}...", end=' ')
        
        result = subprocess.run(f'\"{pip_cmd}\" install {package}', shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅")
            success_count += 1
        else:
            print("❌")
            fail_count += 1
            failed_packages.append(package)
    
    print(f"\n📊 Kết quả:")
    print(f"   ✅ Thành công: {success_count}/{len(REQUIRED_PACKAGES)}")
    print(f"   ❌ Thất bại: {fail_count}/{len(REQUIRED_PACKAGES)}")
    
    if failed_packages:
        print(f"\n⚠️  Các package thất bại:")
        for pkg in failed_packages:
            print(f"   • {pkg}")
    
    return fail_count == 0

def create_activation_scripts():
    print_header("📝 TẠO SCRIPT KÍCH HOẠT")
    
    activate_bat = f"""@echo off
echo ================================
echo KICH HOAT MOI TRUONG AO
echo ================================
echo.
call {VENV_NAME}\\Scripts\\activate.bat
echo.
echo Mo truong ao da duoc kich hoat!
echo.
echo Cac lenh co san:
echo    python telegram_bot.py  - Chay bot
echo    python config.py        - Kiem tra cau hinh
echo    deactivate              - Tat moi truong ao
echo.
"""
    
    with open('ACTIVATE.bat', 'w', encoding='utf-8') as f:
        f.write(activate_bat)
    
    print("✅ Đã tạo: ACTIVATE.bat (Windows)")
    
    activate_sh = f"""#!/bin/bash
echo "================================"
echo "KÍCH HOẠT MÔI TRƯỜNG ẢO"
echo "================================"
echo ""
source {VENV_NAME}/bin/activate
echo ""
echo "✅ Môi trường ảo đã được kích hoạt!"
echo ""
exec $SHELL
"""
    
    with open('activate.sh', 'w', encoding='utf-8') as f:
        f.write(activate_sh)
    
    if platform.system() != "Windows":
        os.chmod('activate.sh', 0o755)
    
    print("✅ Đã tạo: activate.sh (Linux/Mac)")
    
    run_bot_bat = f"""@echo off
echo ================================
echo FEAR ^& GREED INDEX BOT
echo ================================
echo.
echo Dang khoi dong bot voi moi truong ao...
echo.
call {VENV_NAME}\\Scripts\\activate.bat
python telegram_bot.py
pause
"""
    
    with open('RUN_BOT.bat', 'w', encoding='utf-8') as f:
        f.write(run_bot_bat)
    
    print("✅ Đã tạo: RUN_BOT.bat")
    
    run_bot_sh = f"""#!/bin/bash
echo "================================"
echo "FEAR & GREED INDEX BOT"
echo "================================"
echo ""
source {VENV_NAME}/bin/activate
python telegram_bot.py
"""
    
    with open('run_bot.sh', 'w', encoding='utf-8') as f:
        f.write(run_bot_sh)
    
    if platform.system() != "Windows":
        os.chmod('run_bot.sh', 0o755)
    
    print("✅ Đã tạo: run_bot.sh")

def create_requirements_txt():
    print_header("📄 TẠO REQUIREMENTS.TXT")
    
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        for package in REQUIRED_PACKAGES:
            f.write(package + '\n')
    
    print("✅ Đã tạo: requirements.txt")

def main():
    print("\n" + "=" * 70)
    print(" 🚀 THIẾT LẬP MÔI TRƯỜNG ẢO - CHỈ BÁO TÂM LÝ BOT")
    print("=" * 70)
    print()
    print(f"📍 Thư mục: {os.getcwd()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"💻 OS: {platform.system()}")
    print(f"📦 Venv: {VENV_NAME}")
    print()
    
    if not create_virtual_environment():
        print("\n❌ Không thể tạo môi trường ảo!")
        return False
    
    if not upgrade_pip():
        print("\n⚠️  Không thể nâng cấp pip, nhưng vẫn tiếp tục...")
    
    if not install_packages():
        print("\n⚠️  Một số thư viện cài đặt thất bại!")
    
    create_requirements_txt()
    create_activation_scripts()
    
    print("\n" + "=" * 70)
    print(" ✅ HOÀN TẤT!")
    print("=" * 70)
    print()
    print("📋 CÁC BƯỚC TIẾP THEO:")
    print("1️⃣  Chỉnh sửa file .env")
    if platform.system() == "Windows":
        print("2️⃣  Double-click RUN_BOT.bat")
    else:
        print("2️⃣  Chạy: ./run_bot.sh")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Đã hủy")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Lỗi: {e}")
        sys.exit(1)
