"""Core business logic for the budget CLI app."""

from typing import Any, Dict, List


def add_transaction(transactions: List[Dict[str, Any]], transaction: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Add a transaction to the list and return the updated list."""
    pass


def get_balance(transactions: List[Dict[str, Any]]) -> float:
    """Return the net balance for the given transactions."""
    pass


def filter_by_category(transactions: List[Dict[str, Any]], category: str) -> List[Dict[str, Any]]:
    """Return transactions matching the given category."""
    pass


def load_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Load transactions from a CSV file."""
    pass


def monthly_summary(transactions: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    """Return monthly income, expense, and net summaries."""
    pass

