import pytest
from bank.bank_account import BankAccount

# Teste de __init__ (Construtor)
def test_init():
    account = BankAccount("123", 100.0)
    assert account.account_number == "123"  # Verifica se o número da conta foi definido corretamente
    assert account.get_balance() == 100.0  # Verifica se o saldo inicial é 100.0
    assert account.get_transaction_history() == []  # Verifica se o histórico de transações começa vazio

# Teste de __str__ (Representação em string)
def test_str():
    account = BankAccount("123", 100.0)
    assert str(account) == "BankAccount(account_number=123, balance=100.0)"  # Verifica se a representação em string está correta

def test_deposit_positive_amount():
    account = BankAccount("123", 100.0)
    account.deposit(50.0)
    assert account.get_balance() == 150.0  # Esperado: saldo = 100 + 50

def test_deposit_negative_amount():
    account = BankAccount("123", 100.0)
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(-50.0)

# Teste de retirada
def test_withdraw_sufficient_balance():
    account = BankAccount("123", 100.0)
    account.withdraw(50.0)
    assert account.get_balance() == 50.0  # Esperado: saldo = 100 - 50

def test_withdraw_insufficient_balance():
    account = BankAccount("123", 50.0)
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(100.0)

# Teste de cálculo de juros
def test_calculate_interest_positive_rate():
    account = BankAccount("123", 100.0)
    account.calculate_interest(10.0)  # 10% de juros
    assert account.get_balance() == 110.0  # Esperado: saldo = 100 + (10% de 100)

def test_calculate_interest_negative_rate():
    account = BankAccount("123", 100.0)
    with pytest.raises(ValueError, match="Interest rate must be positive"):
        account.calculate_interest(-5.0)

# Teste de aplicação de taxa
def test_apply_fee_sufficient_balance():
    account = BankAccount("123", 100.0)
    account.apply_fee(5.0)
    assert account.get_balance() == 95.0  # Esperado: saldo = 100 - 5

def test_apply_fee_insufficient_balance():
    account = BankAccount("123", 4.0)
    with pytest.raises(ValueError, match="Insufficient funds for fee"):
        account.apply_fee(5.0)

