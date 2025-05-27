from iebank_api.models import Account
import pytest

def test_create_account():
    """
    GIVEN a Account model
    WHEN a new Account is created
    THEN check the name, account_number, balance, currency, country, status and created_at fields are defined correctly
    """
    account = Account('John Doe', '€')
    assert account.name == 'John Doe'
    assert account.currency == '€'
    assert account.country == 'Spain'  # Default country
    assert account.account_number != None
    assert account.balance == 0.0
    assert account.status == 'Active'

def test_create_account_with_country():
    """
    GIVEN a Account model
    WHEN a new Account is created with a specific country
    THEN check the country field is set correctly
    """
    account = Account('Jane Smith', '$', 'United States')
    assert account.name == 'Jane Smith'
    assert account.currency == '$'
    assert account.country == 'United States'
    assert account.account_number != None
    assert account.balance == 0.0
    assert account.status == 'Active'

def test_create_account_default_country():
    """
    GIVEN a Account model
    WHEN a new Account is created without specifying country
    THEN check the country defaults to Spain
    """
    account = Account('Test User', '€')
    assert account.country == 'Spain'

def test_account_number_uniqueness():
    """
    GIVEN a Account model
    WHEN multiple accounts are created
    THEN check that account numbers are unique
    """
    account1 = Account('User One', '€')
    account2 = Account('User Two', '$')
    assert account1.account_number != account2.account_number

def test_account_number_length():
    """
    GIVEN a Account model
    WHEN a new Account is created
    THEN check the account number has the correct length (20 digits)
    """
    account = Account('Test User', '€')
    assert len(account.account_number) == 20
    assert account.account_number.isdigit()

def test_account_repr():
    """
    GIVEN a Account model
    WHEN a new Account is created
    THEN check the string representation contains the account number
    """
    account = Account('Test User', '€')
    assert account.account_number in repr(account)