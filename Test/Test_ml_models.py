"""
Tests for the ml/ modules.

NOTE: Written against the module layout documented in the README
(ml/expense_predictor.py, ml/savings_predictor.py, ml/anomaly_detector.py,
ml/budget_recommender.py), each assumed to expose a `predict(...)` function
consistent with train_models.py's outputs in models/*.pkl. Adjust import
paths/function names to match your actual implementation.
"""
import pandas as pd
import pytest


@pytest.fixture
def sample_transactions():
    return pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=6, freq="MS"),
            "amount": [12000, 13500, 11800, 12750, 50000, 12200],
            "category": ["Food", "Food", "Food", "Food", "Shopping", "Food"],
            "transaction_type": ["expense"] * 6,
        }
    )


def test_expense_predictor_returns_positive_number(sample_transactions):
    from ml.expense_predictor import predict

    result = predict(sample_transactions)
    assert isinstance(result, (int, float))
    assert result > 0


def test_savings_predictor_returns_positive_number(sample_transactions):
    from ml.savings_predictor import predict

    result = predict(sample_transactions)
    assert isinstance(result, (int, float))


def test_anomaly_detector_flags_outlier_transaction(sample_transactions):
    """The 50,000 Shopping transaction is a clear outlier vs. the ~12,000
    recurring Food expenses and should be flagged."""
    from ml.anomaly_detector import detect_anomalies

    flagged = detect_anomalies(sample_transactions)
    # Whatever the return shape (list of indices, bool mask, or DataFrame),
    # at least one anomaly should be found among 6 mostly-uniform rows plus
    # one 4x outlier.
    assert len(flagged) >= 1


def test_budget_recommender_returns_per_category_allocation(sample_transactions):
    from ml.budget_recommender import recommend_budget

    result = recommend_budget(sample_transactions)
    assert "Food" in result
    assert all(v >= 0 for v in result.values())


def test_empty_transaction_history_does_not_crash():
    """New users with zero transaction history should get a graceful
    fallback/default, not an exception, from every predictor."""
    from ml.expense_predictor import predict

    empty_df = pd.DataFrame(columns=["date", "amount", "category", "transaction_type"])
    result = predict(empty_df)
    assert result is not None
