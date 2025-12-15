import random
import string

def generate_password(length=12, use_digits=True, use_special=True):
    if length < 4:
        raise ValueError("Password length must be at least 4")

    chars = string.ascii_letters
    if use_digits:
        chars += string.digits
    if use_special:
        chars += "!@#$%^&*"

    # Гарантируем наличие хотя бы одного символа каждого выбранного типа
    password = []
    password.append(random.choice(string.ascii_letters))
    if use_digits:
        password.append(random.choice(string.digits))
    if use_special:
        password.append(random.choice("!@#$%^&*"))

    # Добиваем до нужной длины
    while len(password) < length:
        password.append(random.choice(chars))

    random.shuffle(password)
    return "".join(password)