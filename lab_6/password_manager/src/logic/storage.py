import json
import os


class PasswordStorage:
    def __init__(self, filename="passwords.json"):
        self.filename = filename

    def save_entry(self, service, username, password):
        data = self._load_data()

        # Проверка на дубликаты (бизнес-логика)
        for entry in data:
            if entry["service"] == service and entry["username"] == username:
                raise ValueError("Entry already exists")

        data.append({
            "service": service,
            "username": username,
            "password": password
        })
        self._save_data(data)

    def get_all(self):
        return self._load_data()

    def _load_data(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding = "utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save_data(self, data):
        with open(self.filename, "w", encoding = "utf-8") as f:
            json.dump(data, f, indent = 4)