import pytest


# scope=session нужен для testcontainers — поднимаем БД один раз на всю сессию
pytest_plugins = ["anyio"]
