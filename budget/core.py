"""Core business logic for the budget CLI app."""

from typing import Any, Dict, List


def add_transaction(transactions: List[Dict[str, Any]], transaction: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Add a transaction to the list and return the updated list."""
    normalized_transaction = {
        "date": transaction["date"],
        "type": transaction["type"],
        "category": transaction["category"],
        "description": transaction["description"],
        "amount": transaction["amount"],
        "memo": transaction["memo"],
    }
    return transactions + [normalized_transaction]


def get_balance(transactions: List[Dict[str, Any]]) -> float:
    """Return the net balance for the given transactions."""
    return float(sum(transaction["amount"] for transaction in transactions))


def filter_by_category(transactions: List[Dict[str, Any]], category: str) -> List[Dict[str, Any]]:
    """Return transactions matching the given category."""
    normalized_category = category.casefold()
    return [
        transaction
        for transaction in transactions
        if transaction["category"].casefold() == normalized_category
    ]


def load_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Load transactions from a CSV file."""
    pass


def monthly_summary(transactions: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    """Return monthly income, expense, and net summaries."""
    pass
