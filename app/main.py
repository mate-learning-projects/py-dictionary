class Dictionary:
    def __init__(self) -> None:
        # Ініціалізуємо початкові значення: розмір таблиці 8 і поріг заповнення в 2/3
        self.length = 0
        self.hash_table: list = [None] * 8
        self.factor = int(
            2 / 3 * len(self.hash_table)
        )  # Поріг заповнення для збільшення розміру таблиці

    def resize(self) -> None:
        """Збільшує розмір хеш-таблиці в 2 рази та перехешує всі елементи."""
        new_hash_table = [None] * len(self.hash_table) * 2
        for item in self.hash_table:
            if item is not None:
                # Обчислюємо новий індекс для ключа в новій таблиці
                new_index = hash(item[0]) % len(new_hash_table)

                # Лінійне пробування для вирішення колізій у новій таблиці
                while new_hash_table[new_index] is not None:
                    new_index = (new_index + 1) % len(new_hash_table)

                # Додаємо елемент до нової таблиці
                new_hash_table[new_index] = item

        # Оновлюємо посилання на нову таблицю та поріг заповнення
        self.hash_table = new_hash_table
        self.factor = int(
            2 / 3 * len(self.hash_table)
        )  # Оновлюємо поріг для нової таблиці

    def __setitem__(self, key, value):
        """Додає новий елемент або оновлює існуючий за ключем."""
        # Перевірка заповненості таблиці: якщо перевищили поріг, викликаємо resize
        if self.length >= self.factor:
            self.resize()

        # Обчислюємо початковий індекс для ключа
        hash_key = hash(key)
        idx = hash_key % len(self.hash_table)
        original_idx = (
            idx  # Зберігаємо початковий індекс для відстеження повного обходу
        )

        # Лінійне пробування
        while True:
            if self.hash_table[idx] is None:
                # Якщо ячейка пуста, додаємо елемент
                self.hash_table[idx] = (key, hash_key, value)
                self.length += 1
                return
            elif self.hash_table[idx][0] == key:
                # Якщо ключ вже існує, оновлюємо його значення
                self.hash_table[idx] = (key, hash_key, value)
                return

            # Переходимо до наступного індексу в разі колізії
            idx = (idx + 1) % len(self.hash_table)

            # Якщо повернулися до початкової позиції, значить, таблиця переповнена (рідкий випадок)
            if idx == original_idx:
                raise RuntimeError(
                    "Hashtable is full, even after resize. This should not happen."
                )

    def __getitem__(self, key):
        """Повертає значення за ключем або викликає KeyError, якщо ключ не знайдено."""
        hash_key = hash(key)
        idx = hash_key % len(self.hash_table)
        original_idx = idx  # Початковий індекс для відстеження повного обходу

        # Лінійне пробування
        while True:
            if self.hash_table[idx] is None:
                # Якщо ячейка пуста, ключ не знайдено
                raise KeyError(f"Key {key} not found")

            if self.hash_table[idx][0] == key:
                # Якщо ключ збігся, повертаємо значення
                return self.hash_table[idx][2]

            # Лінійне пробування для переходу до наступного індексу
            idx = (idx + 1) % len(self.hash_table)

            # Якщо повернулися до початкової позиції, ключ не знайдено
            if idx == original_idx:
                raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        """Повертає кількість елементів у хеш-таблиці."""
        return self.length
