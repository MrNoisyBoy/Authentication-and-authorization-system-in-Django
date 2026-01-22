#!/usr/bin/env python
"""
Запуск сервера без проверок для Python 3.14
"""
import os
import sys
import subprocess

if __name__ == "__main__":
    print("🚀 Запуск сервера Django...")
    print("📡 Адрес: http://127.0.0.1:8000/")
    print("🛑 Для остановки нажмите Ctrl+C\n")

    # Запускаем сервер через subprocess
    cmd = [sys.executable, 'manage.py', 'runserver', '--skip-checks']

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 Сервер остановлен")
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")