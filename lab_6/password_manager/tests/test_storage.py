import pytest
import json
from unittest.mock import mock_open, patch, MagicMock
from src.logic.storage import PasswordStorage


# Тест 5: Тест на сохранение (Мокаем запись в файл)
@patch("builtins.open", new_callable = mock_open)
@patch("json.dump")
@patch("os.path.exists")
def test_save_entry_writes_to_file(mock_exists, mock_json_dump, mock_file):
    mock_exists.return_value = False

    storage = PasswordStorage("test.json")
    storage.save_entry("VK", "user", "12345")

    mock_file.assert_called_with("test.json", "w", encoding = "utf-8")

    args, _ = mock_json_dump.call_args
    saved_data = args[0]
    assert saved_data[0]["service"] == "VK"
    assert saved_data[0]["password"] == "12345"


# Тест 6: Тест на дубликаты (Мокаем чтение файла)
@patch("src.logic.storage.PasswordStorage._load_data")  # Мокаем внутренний метод
def test_save_duplicate_raises_error(mock_load):
    mock_load.return_value = [{"service": "Google", "username": "me", "password": "old"}]

    storage = PasswordStorage()

    with pytest.raises(ValueError):
        storage.save_entry("Google", "me", "new_pass")


# Тест 7: Простой тест чтения
@patch("builtins.open", new_callable = mock_open, read_data = '[{"service": "X", "username": "y", "password": "z"}]')
@patch("os.path.exists")
def test_get_all_returns_data(mock_exists, mock_file):
    mock_exists.return_value = True
    storage = PasswordStorage()
    data = storage.get_all()

    assert len(data) == 1
    assert data[0]["service"] == "X"


# Тест 8: Тест на битый файл
@patch("builtins.open", new_callable = mock_open)
@patch("os.path.exists")
@patch("json.load")
def test_load_data_corrupted_file(mock_json_load, mock_exists, mock_file):
    mock_exists.return_value = True

    mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)

    storage = PasswordStorage()

    data = storage.get_all()

    assert data == []