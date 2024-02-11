from conftest import BASE_DIR


try:
    from app.models.financial_base import FinancialBase
except (NameError, ImportError):
    class FinancialBase:
        pass

try:
    from app.core.config import Settings
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен объект настроек приложения `Settings`.'
        'Проверьте и поправьте: он должен быть доступен в модуле '
        '`app.core.config`.',
    )


def test_fin_base_is_abstract():
    if hasattr(FinancialBase, '__abstract__'):
        assert hasattr(FinancialBase, '__abstract__'), (
            'Модель `FinancialBase` должна быть абстрактной. '
            'Добавьте атрибут `__abstract__`'
        )
        assert FinancialBase.__abstract__, (
            'Таблица `FinancialBase` должна быть абстрактной.'
        )


def test_check_migration_file_exist():
    app_dirs = [d.name for d in BASE_DIR.iterdir()]
    assert 'alembic' in app_dirs, (
        'В корневой директории не обнаружена папка `alembic`.'
    )
    ALEMBIC_DIR = BASE_DIR / 'alembic'
    version_dir = [d.name for d in ALEMBIC_DIR.iterdir()]
    assert 'versions' in version_dir, (
        'В папке `alembic` не обнаружена папка `versions`'
    )
    VERSIONS_DIR = ALEMBIC_DIR / 'versions'
    files_in_version_dir = [
        f.name for f in VERSIONS_DIR.iterdir()
        if f.is_file() and 'init' not in f.name
    ]
    assert len(files_in_version_dir) > 0, (
        'В папке `alembic.versions` не обнаружены файлы миграций'
    )


def test_check_db_url():
    for attr_name, attr_value in Settings.schema()['properties'].items():
        if 'db' in attr_name or 'database' in attr_name:
            assert 'sqlite+aiosqlite' in attr_value['default'], (
                'Укажите значение по умолчанию для подключения базы данных '
                'sqlite '
            )
