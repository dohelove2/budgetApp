"""Tests for budget core logic."""

import csv

from budget.core import add_transaction, filter_by_category, get_balance, load_transactions_from_csv


def test_add_transaction_increases_length() -> None:
    transactions = [
        {
            "date": "2026-01-05",
            "type": "지출",
            "category": "식비",
            "description": "점심식사",
            "amount": -12000,
            "memo": "",
        }
    ]
    transaction = {
        "date": "2026-01-07",
        "type": "수입",
        "category": "급여",
        "description": "월급",
        "amount": 3500000,
        "memo": "1월급여",
    }

    result = add_transaction(transactions, transaction)

    assert len(result) == 2


def test_add_transaction_keeps_negative_amount_for_expense() -> None:
    transactions = []
    transaction = {
        "date": "2026-01-10",
        "type": "지출",
        "category": "교통",
        "description": "지하철",
        "amount": -1500,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert result[-1]["amount"] == -1500


def test_add_transaction_keeps_positive_amount_for_income() -> None:
    transactions = []
    transaction = {
        "date": "2026-01-28",
        "type": "기타수입",
        "category": "기타수입",
        "description": "중고 판매",
        "amount": 25000,
        "memo": "중고마켓",
    }

    result = add_transaction(transactions, transaction)

    assert result[-1]["amount"] == 25000


def test_add_transaction_accepts_empty_description() -> None:
    transactions = []
    transaction = {
        "date": "2026-01-12",
        "type": "지출",
        "category": "식비",
        "description": "",
        "amount": -5800,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert result[-1]["description"] == ""


def test_get_balance_returns_zero_for_empty_list() -> None:
    assert get_balance([]) == 0.0


def test_get_balance_sums_step2_transactions() -> None:
    with open("data/step2_transactions.csv", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        transactions = [
            {
                "date": row["date"],
                "type": row["type"],
                "category": row["category"],
                "description": row["description"],
                "amount": int(row["amount"]),
                "memo": row["memo"],
            }
            for row in reader
        ]

    assert get_balance(transactions) == 24285027


def test_filter_by_category_matches_case_insensitively() -> None:
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        },
        {
            "date": "2026-01-29",
            "type": "지출",
            "category": "식비",
            "description": "편의점",
            "amount": -33021,
            "memo": "",
        },
        {
            "date": "2026-02-24",
            "type": "수입",
            "category": "기타수입",
            "description": "중고 판매",
            "amount": 199790,
            "memo": "",
        },
    ]

    result = filter_by_category(transactions, "sHoPpInG")

    assert [transaction["category"] for transaction in result] == []


def test_filter_by_category_returns_matching_transactions() -> None:
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        },
        {
            "date": "2026-01-29",
            "type": "지출",
            "category": "식비",
            "description": "편의점",
            "amount": -33021,
            "memo": "",
        },
        {
            "date": "2026-02-24",
            "type": "수입",
            "category": "기타수입",
            "description": "중고 판매",
            "amount": 199790,
            "memo": "",
        },
    ]

    result = filter_by_category(transactions, "식비")

    assert len(result) == 1
    assert result[0]["category"] == "식비"


def test_filter_by_category_returns_empty_list_for_missing_category() -> None:
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        }
    ]

    result = filter_by_category(transactions, "없는카테고리")

    assert result == []


def test_filter_by_category_returns_independent_list() -> None:
    transactions = [
        {
            "date": "2026-01-29",
            "type": "지출",
            "category": "식비",
            "description": "편의점",
            "amount": -33021,
            "memo": "",
        }
    ]

    result = filter_by_category(transactions, "식비")
    result.append(
        {
            "date": "2026-02-01",
            "type": "지출",
            "category": "식비",
            "description": "추가",
            "amount": -1000,
            "memo": "",
        }
    )

    assert len(transactions) == 1
    assert len(result) == 2


def test_load_transactions_from_csv_loads_step1_data() -> None:
    transactions = load_transactions_from_csv("data/step1_transactions.csv")

    assert len(transactions) == 10
    assert transactions[0]["date"] == "2026-01-05"
    assert transactions[0]["amount"] == -12000
    assert transactions[-1]["date"] == "2026-01-28"
    assert transactions[-1]["amount"] == 25000


def test_load_transactions_from_csv_converts_amount_to_int() -> None:
    transactions = load_transactions_from_csv("data/step1_transactions.csv")

    assert isinstance(transactions[0]["amount"], int)
    assert isinstance(transactions[-1]["amount"], int)


def test_load_transactions_from_csv_preserves_balance() -> None:
    transactions = load_transactions_from_csv("data/step1_transactions.csv")

    assert get_balance(transactions) == 3366700
