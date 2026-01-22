#!/usr/bin/env python
"""
Скрипт для быстрой настройки проекта - ИСПРАВЛЕННАЯ ВЕРСИЯ
"""
import os
import sys
from pathlib import Path


def setup_project():
    print("🔧 Настройка проекта...")

    # 1. Добавляем текущую директорию в путь
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))

    # 2. Настраиваем окружение ДО импорта Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_system.settings')

    print("📦 Создание миграций...")
    # Выполняем команды через subprocess чтобы избежать повторной инициализации
    import subprocess

    # Команды для выполнения
    commands = [
        ['python', 'manage.py', 'makemigrations', 'api'],
        ['python', 'manage.py', 'migrate'],
    ]

    for cmd in commands:
        print(f"Выполняю: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Успешно: {result.stdout[:100]}...")
            else:
                print(f"⚠️  Ошибка: {result.stderr}")
        except Exception as e:
            print(f"❌ Исключение: {e}")

    # 3. Создаем тестового пользователя через отдельный скрипт
    print("\n👤 Создание тестового пользователя...")
    create_user_script = """
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_system.settings')
django.setup()

from api.models import User

# Удаляем старых тестовых пользователей если есть
User.objects.filter(email__in=['admin@example.com', 'test@example.com']).delete()

# Создаем администратора
admin = User(
    first_name='Админ',
    last_name='Тестовый',
    email='admin@example.com',
    is_active=True
)
admin.set_password('admin123')
admin.save()
print(f"✅ Админ создан: admin@example.com / admin123")

# Создаем обычного пользователя
user = User(
    first_name='Тест',
    last_name='Пользователь',
    email='test@example.com',
    is_active=True
)
user.set_password('test123')
user.save()
print(f"✅ Пользователь создан: test@example.com / test123")

print(f"✅ Всего пользователей: {User.objects.count()}")
"""

    # Запускаем скрипт создания пользователя
    try:
        exec(create_user_script)
    except Exception as e:
        print(f"⚠️  Ошибка при создании пользователя: {e}")
        print("ℹ️  Создайте пользователей через API позже")

    print("\n🎉 Настройка завершена!")
    print("\n🚀 Запустите сервер одной из команд:")
    print("   python run.py")
    print("   python manage.py runserver --skip-checks")
    print("\n🌐 Откройте в браузере: http://127.0.0.1:8000/")
    print("\n🔑 Тестовые пользователи:")
    print("   admin@example.com / admin123")
    print("   test@example.com / test123")


if __name__ == "__main__":
    setup_project()