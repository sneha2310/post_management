import pytest
from app.calculations import BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


def test_bank_account_inititalize(bank_account):
    assert bank_account.balance == 50


def test_back_account_deposits(bank_account):
    bank_account.deposit(50)
    assert bank_account.balance == 100


def test_back_account_withdraw(bank_account):
    bank_account.deposit(100)
    bank_account.withdraw(50)
    assert bank_account.balance == 100


def test_back_account_deposits(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance) == 55

@pytest.mark.parametrize("num1, num2, expected", [
    (100, 50, 50),
    (200, 50, 150)
])
def test_bank_transactions(zero_bank_account, num1, num2, expected):
    zero_bank_account.deposit(num1)
    zero_bank_account.withdraw(num2)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)