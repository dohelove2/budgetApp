"""Tests for budget core logic."""

import csv

from budget.core import (
    add_transaction,
    filter_by_category,
    get_balance,
    load_transactions_from_csv,
    monthly_summary,
)


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


def test_load_transactions_from_csv_raises_file_not_found_for_missing_file() -> None:
    try:
        load_transactions_from_csv("data/does_not_exist.csv")
    except FileNotFoundError:
        assert True
    else:
        raise AssertionError("Expected FileNotFoundError")


def test_load_transactions_from_csv_raises_value_error_for_bad_amount() -> None:
    with open("data/step1_transactions.csv", encoding="utf-8-sig") as source:
        rows = source.read()

    bad_csv_path = "data/_tmp_bad_amount.csv"
    with open(bad_csv_path, "w", encoding="utf-8-sig") as target:
        target.write(rows.replace("-12000", "not-a-number", 1))

    try:
        try:
            load_transactions_from_csv(bad_csv_path)
        except ValueError:
            assert True
        else:
            raise AssertionError("Expected ValueError")
    finally:
        import os

        if os.path.exists(bad_csv_path):
            os.remove(bad_csv_path)


def test_monthly_summary_returns_empty_dict_for_empty_list() -> None:
    assert monthly_summary([]) == {}


def test_monthly_summary_groups_income_expense_and_net() -> None:
    transactions = load_transactions_from_csv("data/step3_transactions.csv")

    result = monthly_summary(transactions)

    assert result["2025-01"] == {
        "income": 405037,
        "expense": -2886860,
        "net": -2481823,
    }
    assert result["2025-02"] == {
        "income": 12940804,
        "expense": -1832242,
        "net": 11108562,
    }
    assert result["2026-03"] == {
        "income": 489857,
        "expense": -3301374,
        "net": -2811517,
    }


def test_monthly_summary_handles_large_step4_data() -> None:
    transactions = load_transactions_from_csv("data/step4_large_transactions.csv")

    result = monthly_summary(transactions)

    assert len(transactions) == 5000
    assert len(result) == 78
    assert result["2020-01"] == {
        "income": 37502538,
        "expense": -11873710,
        "net": 25628828,
    }
    assert result["2026-06"] == {
        "income": 9692304,
        "expense": -6064940,
        "net": 3627364,
    }
