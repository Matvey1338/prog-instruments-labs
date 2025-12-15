import pytest
from src.logic.generator import generate_password


# Тест 1: Проверка длины
def test_password_length():
    pwd = generate_password(length = 15)
    assert len(pwd) == 15


# Тест 2: Проверка ошибки при слишком коротком пароле
def test_password_too_short_raises_error():
    with pytest.raises(ValueError):
        generate_password(length = 3)


# Тест 3: ПАРАМЕТРИЗАЦИЯ
# Проверяем разные конфигурации генерации
@pytest.mark.parametrize("use_digits, use_special", [
    (True, True),
    (False, True),
    (True, False),
    (False, False)
])
def test_generator_content(use_digits, use_special):
    pwd = generate_password(length = 20, use_digits = use_digits, use_special = use_special)

    has_digits = any(char.isdigit() for char in pwd)
    has_special = any(char in "!@#$%^&*" for char in pwd)

    assert has_digits == use_digits
    assert has_special == use_special