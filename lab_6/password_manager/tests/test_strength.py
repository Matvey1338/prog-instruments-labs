import pytest
from src.logic.strength import check_strength

# Тест 4: ПАРАМЕТРИЗАЦИЯ бизнес-логики оценки
@pytest.mark.parametrize("password, expected_score", [
    ("abc", "Weak"),                  # Короткий
    ("abcdefgh", "Weak"),             # Длинный, но только буквы
    ("Abcdefgh1", "Medium"),          # Длинный + Большая + Цифра
    ("Abcdefgh1234!", "Strong"),         # Полный набор
])
def test_strength_calculation(password, expected_score):
    assert check_strength(password) == expected_score