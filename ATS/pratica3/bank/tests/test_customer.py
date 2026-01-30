import pytest
from bank.bank_account import BankAccount
from bank.customer import Customer

# Testar o método __str__
def test_customer_str():
    account = BankAccount("123", 100.0)
    customer = Customer("Carlos", account)
    assert str(customer) == "Customer(name=Carlos, balance=100.0)"

# Testar o método process_transaction para depósito
def test_customer_process_transaction_deposit():
    account = BankAccount("123", 100.0)
    customer = Customer("Carlos", account)
    customer.process_transaction(50.0, "deposit")
    assert customer.get_balance() == 150.0  # 100 + 50

def test_customer_process_transaction_deposit_with_fee():
    account = BankAccount("123", 100.0)
    customer = Customer("Carlos", account, transaction_fee=5.0)
    customer.process_transaction(50.0, "deposit")
    assert customer.get_balance() == 145.0  # 100 + 50 - 5 (taxa)


# Testar o método process_transaction para saque
def test_customer_process_transaction_withdraw():
    account = BankAccount("123", 100.0)
    customer = Customer("Carlos", account)
    customer.process_transaction(40.0, "withdraw")
    assert customer.get_balance() == 60.0  # 100 - 40

# Testar o método process_transaction para saque com taxa
def test_customer_process_transaction_withdraw_with_fee():
    account = BankAccount("123", 100.0)
    customer = Customer("Carlos", account, transaction_fee=5.0)
    customer.process_transaction(40.0, "withdraw")
    assert customer.get_balance() == 55.0  # 100 - 40 - 5 (taxa)

# Testar o método process_transaction para saque com taxa quando não há saldo suficiente
def test_customer_process_transaction_withdraw_insufficient_funds():
    account = BankAccount("123", 20.0)
    customer = Customer("Carlos", account, transaction_fee=5.0)
    with pytest.raises(ValueError, match="Insufficient funds"):
        customer.process_transaction(30.0, "withdraw")  # Deve falhar

# Testar o método get_transaction_history após um depósito
def test_get_transaction_history_after_deposit():
    account = BankAccount("123", 100.0)
    customer = Customer("Carlos", account)
    customer.process_transaction(50.0, "deposit")
    history = customer.get_transaction_history()
    assert len(history) == 1
    assert history[0] == ('deposit', 50.0)

# Testar o método get_transaction_history após um saque
def test_get_transaction_history_after_withdraw():
    account = BankAccount("123", 100.0)
    customer = Customer("Carlos", account)
    customer.process_transaction(40.0, "withdraw")
    history = customer.get_transaction_history()
    assert len(history) == 1
    assert history[0] == ('withdraw', 40.0)

# Testar o método get_transaction_history após depósito e saque
def test_get_transaction_history_after_deposit_and_withdraw():
    account = BankAccount("123", 100.0)
    customer = Customer("Carlos", account)
    customer.process_transaction(50.0, "deposit")
    customer.process_transaction(30.0, "withdraw")
    history = customer.get_transaction_history()
    assert len(history) == 2
    assert history[0] == ('deposit', 50.0)
    assert history[1] == ('withdraw', 30.0)

# Testar o método process_transaction com taxa igual a 0
def test_customer_process_transaction_with_zero_fee():
    account = BankAccount("123", 100.0)
    customer = Customer("Carlos", account, transaction_fee=0.0)
    customer.process_transaction(50.0, "deposit")
    assert customer.get_balance() == 150.0  # 100 + 50 (sem taxa)
