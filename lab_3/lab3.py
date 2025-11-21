class Bank:
    def __init__(self, name):
        self.name = name
        self.clients = {}

    def add_client(self, client):
        self.clients[client.client_id] = client

    def remove_client(self, client_id):
        if client_id in self.clients:
            del self.clients[client_id]
        else:
            raise ValueError("Клиент не найден")

    def get_client(self, client_id):
        return self.clients.get(client_id, None)


class Client:
    def __init__(self, client_id, name):
        self.client_id = client_id
        self.name = name
        self.accounts = {}

    def open_account(self, currency):
        if currency not in self.accounts:
            self.accounts[currency] = Account(currency)
        else:
            raise ValueError(f"Счёт в валюте {currency} уже существует")

    def close_account(self, currency):
        if currency in self.accounts:
            del self.accounts[currency]
        else:
            raise ValueError(f"Счёт в валюте {currency} не найден")

    def get_account(self, currency):
        return self.accounts.get(currency, None)

    def print_statement(self):
        total_balance = 0
        print(f"\nВыписка по счетам клиента: {self.name}")
        if not self.accounts:
            print("У клиента пока нет открытых счетов.")
            return
        for currency, account in self.accounts.items():
            print(f"Валюта: {currency}, Баланс: {account.balance}")
            total_balance += account.balance
        print(f"Суммарный баланс по всем счетам: {total_balance}\n")


class Account:
    def __init__(self, currency, balance=0):
        self.currency = currency
        self.balance = balance

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Нельзя внести отрицательную сумму")
        self.balance += amount

    def withdraw(self, amount):
        if amount < 0:
            raise ValueError("Нельзя снять отрицательную сумму")
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise ValueError("Недостаточно средств на счёте")

    def transfer(self, target_account, amount, conversion_rate=1):
        if amount < 0:
            raise ValueError("Сумма перевода не может быть отрицательной")

        if self.currency != target_account.currency:
            # Конвертация суммы, если валюты разные
            converted_amount = amount / conversion_rate
        else:
            converted_amount = amount

        if self.balance >= amount:
            self.balance -= amount
            target_account.deposit(converted_amount)
        else:
            raise ValueError("Недостаточно средств для перевода")


def run_bank_system(bank):
    while True:
        print("\n=== Добро пожаловать в банк", bank.name, "===")
        client_id = input("Введите ваш ID клиента: ")
        client = bank.get_client(client_id)

        if not client:
            print("❌ Клиент с таким ID не найден. Попробуйте снова.")
            continue

        print(f"\nЗдравствуйте, {client.name}!")

        while True:
            print("\n--- Главное меню ---")
            print("1. Открыть счёт")
            print("2. Закрыть счёт")
            print("3. Пополнить счёт")
            print("4. Снять деньги со счёта")
            print("5. Перевести деньги между счетами")
            print("6. Показать выписку по всем счетам")
            print("7. Выйти")

            choice = input("Выберите действие (1-7): ")

            if choice == "1":
                currency = input("Введите валюту счёта (например, USD, EUR, RUB): ").upper()
                try:
                    client.open_account(currency)
                    print(f"✅ Счёт в валюте {currency} успешно открыт.")
                except ValueError as e:
                    print("⚠️", e)

            elif choice == "2":
                currency = input("Введите валюту счёта, который хотите закрыть: ").upper()
                try:
                    client.close_account(currency)
                    print(f"✅ Счёт в валюте {currency} успешно закрыт.")
                except ValueError as e:
                    print("⚠️", e)

            elif choice == "3":
                currency = input("Введите валюту счёта для пополнения: ").upper()
                amount = float(input("Введите сумму пополнения: "))
                account = client.get_account(currency)
                if account:
                    try:
                        account.deposit(amount)
                        print(f"✅ На счёт {currency} внесено {amount}. Новый баланс: {account.balance}")
                    except ValueError as e:
                        print("⚠️", e)
                else:
                    print(f"❌ Счёт в валюте {currency} не найден.")

            elif choice == "4":
                currency = input("Введите валюту счёта для снятия: ").upper()
                amount = float(input("Введите сумму для снятия: "))
                account = client.get_account(currency)
                if account:
                    try:
                        account.withdraw(amount)
                        print(f"✅ Со счёта {currency} снято {amount}. Остаток: {account.balance}")
                    except ValueError as e:
                        print("⚠️", e)
                else:
                    print(f"❌ Счёт в валюте {currency} не найден.")


            elif choice == "5":

                print("\n--- Перевод денег ---")

                print("1. Между своими счетами")

                print("2. Другому клиенту")

                transfer_type = input("Выберите вариант (1 или 2): ")

                if transfer_type == "1":

                    from_currency = input("Введите валюту счёта, с которого переводите: ").upper()

                    to_currency = input("Введите валюту счёта, на который переводите: ").upper()

                    amount = float(input("Введите сумму перевода: "))

                    from_account = client.get_account(from_currency)

                    to_account = client.get_account(to_currency)

                    if from_account and to_account:

                        if from_account is to_account:
                            print("⚠️ Нельзя перевести деньги на тот же самый счёт!")

                            continue

                        if from_currency != to_currency:

                            conversion_rate = float(input("Введите курс конвертации (из исходной валюты в целевую): "))

                        else:

                            conversion_rate = 1

                        try:

                            from_account.transfer(to_account, amount, conversion_rate)

                            print(f"✅ Перевод успешно выполнен!")

                            print(f"Баланс {from_currency}: {from_account.balance}")

                            print(f"Баланс {to_currency}: {to_account.balance}")

                        except ValueError as e:

                            print("⚠️", e)

                    else:

                        print("❌ Один или оба счёта не найдены.")


                elif transfer_type == "2":

                    target_id = input("Введите ID клиента, которому хотите перевести деньги: ")

                    target_client = bank.get_client(target_id)

                    if not target_client:
                        print("❌ Клиент с таким ID не найден.")

                        continue

                    from_currency = input("Введите валюту вашего счёта: ").upper()

                    to_currency = input("Введите валюту счёта получателя: ").upper()

                    amount = float(input("Введите сумму перевода: "))

                    from_account = client.get_account(from_currency)

                    to_account = target_client.get_account(to_currency)

                    if not from_account:
                        print("❌ У вас нет счёта в валюте", from_currency)

                        continue

                    if not to_account:
                        print("❌ У получателя нет счёта в валюте", to_currency)

                        continue

                    if from_currency != to_currency:

                        conversion_rate = float(input("Введите курс конвертации (из исходной валюты в целевую): "))

                    else:

                        conversion_rate = 1

                    try:

                        from_account.transfer(to_account, amount, conversion_rate)

                        print(f"✅ Перевод клиенту {target_client.name} успешно выполнен!")

                        print(f"Ваш баланс ({from_currency}): {from_account.balance}")

                        print(f"Баланс получателя ({to_currency}): {to_account.balance}")

                    except ValueError as e:

                        print("⚠️", e)


                else:

                    print("⚠️ Неверный выбор, попробуйте снова.")


            elif choice == "6":
                client.print_statement()

            elif choice == "7":
                print("👋 До свидания, возвращайтесь снова!")
                break

            else:
                print("⚠️ Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    # Создаём банк
    bank = Bank("Мой Банк")

    # Добавляем тестового клиента
    client1 = Client("123", "Иван Иванов")
    maria = Client("456", "Мария Смирнова")
    bank.add_client(client1)
    bank.add_client(maria)


    # Запускаем систему
    run_bank_system(bank)
