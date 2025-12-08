import json
import hashlib
from typing import List

"""
В этом модуле обитают функции, необходимые для автоматизированной проверки результатов ваших трудов.
"""


def calculate_checksum(row_numbers: List[int]) -> str:
    """
    Вычисляет md5 хеш от списка целочисленных значений.

    """
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()


def serialize_result(variant: int, checksum: str) -> None:
    """
    Метод для сериализации результатов лабораторной.
    Сохраняет номер варианта и контрольную сумму в файл result.json.
    """
    data = {
        "variant": variant,
        "checksum": checksum
    }

    with open('result.json', 'w', encoding = 'utf-8') as f:
        json.dump(data, f, indent = 2)

    print("Результат успешно сохранен в result.json")


if __name__ == "__main__":
    pass
