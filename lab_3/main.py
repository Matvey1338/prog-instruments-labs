import csv
import re
from typing import List
from checksum import calculate_checksum, serialize_result


def get_regex_patterns() -> dict:
    """
    Возвращает словарь с регулярными выражениями для валидации полей.
    """
    return {
        'email': re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
        'height': re.compile(r'^[1-2]\.\d{2}$'),  # Рост: 1.xx или 2.xx
        'snils': re.compile(r'^\d{11}$'),  # 11 цифр подряд
        'passport': re.compile(r'^\d{2} \d{2} \d{6}$'),  # Формат: 22 22 666666
        'occupation': re.compile(r'^[A-Za-zА-Яа-яЁё\s-]+$'),  # Буквы, пробелы, дефис
        'longitude': re.compile(r'^-?((1[0-7]\d|\d{1,2})\.\d+|180\.0+)$'),  # Долгота -180..180
        'hex_color': re.compile(r'^#[a-fA-F0-9]{6}$'),  # #ffffff
        'issn': re.compile(r'^\d{4}-\d{4}$'),  # 0000-0000
        'locale_code': re.compile(r'^[a-z]{2}(-[a-z]{2,})?$'),  # ru или en-us
        'time': re.compile(r'^([0-1]\d|2[0-3]):[0-5]\d:[0-5]\d\.\d{6}$')  # HH:MM:SS.ms
    }


def validate_row(row: dict, patterns: dict) -> bool:
    """
    Проверяет строку на соответствие всем регулярным выражениям.
    Возвращает False, если хотя бы одно поле невалидно.
    """
    for key, pattern in patterns.items():
        # Если в CSV есть лишние столбцы, пропускаем их проверку,
        # либо проверяем только те, что есть в patterns
        if key in row:
            if not pattern.match(row[key]):
                return False
    return True


def process_csv(filepath: str) -> List[int]:
    """
    Читает CSV и возвращает список индексов невалидных строк.
    """
    invalid_indices = []
    patterns = get_regex_patterns()

    try:
        with open(filepath, mode = 'r', encoding = 'utf-16', newline = '') as csvfile:
            # Используем DictReader, чтобы брать по названиям столбцов
            reader = csv.DictReader(csvfile, delimiter = ';')

            for i, row in enumerate(reader):
                if not validate_row(row, patterns):
                    invalid_indices.append(i)

    except FileNotFoundError:
        print(f"Файл {filepath} не найден.")

    return invalid_indices


if __name__ == '__main__':
    csv_filename = '59.csv'
    my_variant = 59

    invalid_rows = process_csv(csv_filename)
    print(f"Найдено невалидных строк: {len(invalid_rows)}")

    print(invalid_rows)

    if len(invalid_rows) == 1000:
        result_hash = calculate_checksum(invalid_rows)
        print(f"Контрольная сумма: {result_hash}")

        serialize_result(my_variant, result_hash)
    else:
        print(f"ОШИБКА: Найдено {len(invalid_rows)} строк. Должно быть 1000")
