import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import User, Role, BusinessElement, AccessRule, UserRole


def create_test_data():
    print("Создание тестовых данных...")

    # Создаем роли
    admin_role, _ = Role.objects.get_or_create(
        name='admin',
        defaults={'description': 'Администратор'}
    )

    user_role, _ = Role.objects.get_or_create(
        name='user',
        defaults={'description': 'Обычный пользователь'}
    )

    # Создаем бизнес-элементы
    elements_data = [
        {'name': 'Dashboard', 'code': 'dashboard', 'description': 'Главная страница'},
        {'name': 'Products', 'code': 'products', 'description': 'Управление товарами'},
        {'name': 'Orders', 'code': 'orders', 'description': 'Управление заказами'},
        {'name': 'Roles', 'code': 'roles', 'description': 'Управление ролями'},
        {'name': 'Business Elements', 'code': 'business_elements', 'description': 'Бизнес-элементы'},
        {'name': 'Access Rules', 'code': 'access_rules', 'description': 'Правила доступа'},
    ]

    elements = {}
    for elem_data in elements_data:
        element, _ = BusinessElement.objects.get_or_create(
            code=elem_data['code'],
            defaults=elem_data
        )
        elements[elem_data['code']] = element

    # Создаем администратора
    admin_email = 'admin@example.com'
    if not User.objects.filter(email=admin_email).exists():
        admin_user = User.objects.create(
            email=admin_email,
            first_name='Админ',
            last_name='Системы'
        )
        admin_user.set_password('Admin123')
        admin_user.save()

        UserRole.objects.create(user=admin_user, role=admin_role)
        print(f"Создан администратор: {admin_email} / Admin123")

    # Создаем обычного пользователя
    user_email = 'user@example.com'
    if not User.objects.filter(email=user_email).exists():
        regular_user = User.objects.create(
            email=user_email,
            first_name='Обычный',
            last_name='Пользователь'
        )
        regular_user.set_password('User12345')
        regular_user.save()

        UserRole.objects.create(user=regular_user, role=user_role)
        print(f"Создан пользователь: {user_email} / User12345")

    # Правила для user
    user_access = [
        {'element': 'dashboard', 'read': True},
        {'element': 'products', 'read': True, 'create': True, 'update': True, 'delete': True},
        {'element': 'orders', 'read': True, 'create': True, 'update': True, 'delete': True},
    ]

    for rule_data in user_access:
        element = elements[rule_data['element']]
        AccessRule.objects.get_or_create(
            role=user_role,
            element=element,
            defaults={
                'read_permission': rule_data.get('read', False),
                'create_permission': rule_data.get('create', False),
                'update_permission': rule_data.get('update', False),
                'delete_permission': rule_data.get('delete', False),
            }
        )

    # Правила для admin (полный доступ)
    for element in elements.values():
        AccessRule.objects.get_or_create(
            role=admin_role,
            element=element,
            defaults={
                'read_permission': True,
                'read_all_permission': True,
                'create_permission': True,
                'update_permission': True,
                'update_all_permission': True,
                'delete_permission': True,
                'delete_all_permission': True,
            }
        )

    print("Тестовые данные созданы!")
    print("\nДля входа используйте:")
    print("1. Администратор: admin@example.com / Admin123")
    print("2. Пользователь: user@example.com / User12345")
    print("\nЗапустите сервер: python manage.py runserver")


if __name__ == '__main__':
    create_test_data()