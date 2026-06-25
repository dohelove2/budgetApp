"""Tests for budget core logic."""

from budget.core import add_transaction


def test_add_transaction_increases_length() -> None:
    transactions = []
    transaction = {
        "date": "2026-01-01",
        "type": "income",
        "category": "salary",
        "description": "January salary",
        "amount": 3000000,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert len(result) == 1

