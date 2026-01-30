from bank.bank_account import BankAccount


class Customer:
    def __init__(self, name, account, transaction_fee=0.0):
        self.name = name
        self.account = account
        self.transaction_fee = transaction_fee  # CORRIGIDO

    def __str__(self):
        return f"Customer(name={self.name}, balance={self.get_balance()})"

    def process_transaction(self, amount, transaction_type):
        if transaction_type == 'deposit':
            self.account.deposit(amount)
            if self.transaction_fee > 0:
                self.account.apply_fee(self.transaction_fee)  # Aplica a taxa após o depósito
        elif transaction_type == 'withdraw':
            self.account.withdraw(amount)
            if self.transaction_fee > 0:
                self.account.apply_fee(self.transaction_fee)  # Aplica a taxa após o saque

    def get_balance(self):
        return self.account.get_balance()

    def get_transaction_history(self):
        return self.account.get_transaction_history()