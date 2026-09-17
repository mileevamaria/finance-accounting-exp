from enum import Enum


class Currency(str, Enum):
    AMD = 'amd'
    USD = 'usd'
    EUR = 'eur'
    RUB = 'rub'


class AccountType(str, Enum):
    BANK = 'bank'
    CASH = 'cash'


class TransactionType(str, Enum):
    INCOME = 'income'
    EXPENSE = 'expense'
    TRANSFER = 'transfer'
