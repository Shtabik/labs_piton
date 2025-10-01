class Bank:
    def __init__(self, name):
        self.name = name
        self.clients = []

    def add_client(self, client):
        pass

    def remove_client(self, client_id):
        pass


class Client:
    def __init__(self, client_id, name):
        self.client_id = client_id
        self.name = name
        self.accounts = {}

    def open_account(self, currency):
        pass

    def close_account(self, currency):
        pass


class Account:
    def __init__(self, currency, balance=0):
        self.currency = currency
        self.balance = balance

    def deposit(self, amount):
        pass

    def withdraw(self, amount):
        pass

    def transfer(self, target_account, amount):
        pass
