@echo off
echo ========================================
echo   Установка системы аутентификации
echo ========================================
echo.

REM Проверка Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python не найден в PATH!
    echo Установите Python 3.8+ и добавьте в PATH
    pause
    exit /b 1
)

echo ✅ Python найден
python --version

echo.
echo 📦 Установка зависимостей...
python -m pip install Django==4.2.7 django-cors-headers==4.2.0

if %errorlevel% neq 0 (
    echo ❌ Ошибка установки зависимостей
    pause
    exit /b 1
)

echo ✅ Зависимости установлены
echo.
echo 🔧 Настройка проекта...

REM Удаляем старые миграции если есть
if exist api\migrations rmdir /s /q api\migrations
if exist db.sqlite3 del db.sqlite3

echo.
echo 📊 Создание миграций...
python manage.py makemigrations api

if %errorlevel% neq 0 (
    echo ⚠️  Предупреждение при создании миграций
)

echo.
echo 💾 Применение миграций...
python manage.py migrate

echo.
echo 👤 Создание тестовых пользователей...

REM Создаем Python скрипт для создания пользователей
echo import os > create_users.py
echo import django >> create_users.py
echo os.environ.setdefault^('DJANGO_SETTINGS_MODULE', 'auth_system.settings'^) >> create_users.py
echo django.setup^(^) >> create_users.py
echo. >> create_users.py
echo from api.models import User >> create_users.py
echo. >> create_users.py
echo # Создаем администратора >> create_users.py
echo admin = User^( >> create_users.py
echo     first_name='Админ', >> create_users.py
echo     last_name='Тестовый', >> create_users.py
echo     email='admin@example.com', >> create_users.py
echo     is_active=True >> create_users.py
echo ^) >> create_users.py
echo admin.set_password^('admin123'^) >> create_users.py
echo admin.save^(^) >> create_users.py
echo print^(f"✅ Админ создан: admin@example.com / admin123"^) >> create_users.py
echo. >> create_users.py
echo # Создаем обычного пользователя >> create_users.py
echo user = User^( >> create_users.py
echo     first_name='Тест', >> create_users.py
echo     last_name='Пользователь', >> create_users.py
echo     email='test@example.com', >> create_users.py
echo     is_active=True >> create_users.py
echo ^) >> create_users.py
echo user.set_password^('test123'^) >> create_users.py
echo user.save^(^) >> create_users.py
echo print^(f"✅ Пользователь создан: test@example.com / test123"^) >> create_users.py

python create_users.py
del create_users.py

echo.
echo ========================================
echo   НАСТРОЙКА ЗАВЕРШЕНА!
echo ========================================
echo.
echo 🚀 Запустите сервер командой:
echo    python run.py
echo    ИЛИ
echo    python manage.py runserver --skip-checks
echo.
echo 🌐 Затем откройте в браузере:
echo    http://127.0.0.1:8000/
echo.
echo 🔑 Тестовые пользователи:
echo    admin@example.com / admin123
echo    test@example.com / test123
echo.
pause