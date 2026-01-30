class BankAccount:
    def __init__(self, account_number, initial_balance=0.0):
        self.account_number = account_number
        self.balance = initial_balance
        self.transaction_history = []

    def __str__(self):
        return f"BankAccount(account_number={self.account_number}, balance={self.balance})"

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self.transaction_history.append(('deposit', amount))

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount  # CORRIGIDO
            self.transaction_history.append(('withdraw', amount))
        else:
            raise ValueError("Insufficient funds")

    def get_balance(self):
        return self.balance

    def get_transaction_history(self):
        return self.transaction_history

    def calculate_interest(self, rate):
        if rate < 0:
            raise ValueError("Interest rate must be positive")
        interest = self.balance * (rate / 100)
        self.balance += interest
        self.transaction_history.append(('deposit', interest))

    def apply_fee(self, fee):
        if fee <= self.balance:  # CORRIGIDO
            self.balance -= fee  # CORRIGIDO
            self.transaction_history.append(('withdraw', fee))  # CORRIGIDO
        else:
            raise ValueError("Insufficient funds for fee")


