import pytest
import pandas as pd
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))


def test_executive_data_generation():
    """Test that executive data is generated correctly"""
    from dashboard import generate_executive_data

    df = generate_executive_data()

    # Check basic structure
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0

    # Check required columns
    required_columns = [
        "Name",
        "Title",
        "Company",
        "Relationship_Score",
        "Last_Meeting",
        "Next_Meeting",
        "Strategic_Initiatives",
        "Influence_Level",
        "Decision_Maker",
    ]

    for col in required_columns:
        assert col in df.columns

    # Check data types
    assert df["Relationship_Score"].dtype in ["int64", "float64"]
    assert df["Strategic_Initiatives"].dtype in ["int64", "float64"]
    assert df["Decision_Maker"].dtype == "bool"


def test_account_planning_data_generation():
    """Test that account planning data is generated correctly"""
    from dashboard import generate_account_planning_data

    df = generate_account_planning_data()

    # Check basic structure
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0

    # Check required columns
    required_columns = [
        "Account",
        "Health_Score",
        "API_Usage",
        "Growth_Rate",
        "Expansion_Opportunities",
        "Risk_Level",
        "Next_Quarter_Goal",
        "Strategic_Initiatives",
        "Key_Stakeholders",
        "Last_QBR",
        "Next_QBR",
    ]

    for col in required_columns:
        assert col in df.columns

    # Check data types
    assert df["Health_Score"].dtype in ["int64", "float64"]
    assert df["API_Usage"].dtype in ["int64", "float64"]
    assert df["Growth_Rate"].dtype in ["int64", "float64"]


def test_usage_trends_generation():
    """Test that usage trends data is generated correctly"""
    from dashboard import generate_usage_trends

    df = generate_usage_trends()

    # Check basic structure
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0

    # Check required columns
    required_columns = ["Date", "Company", "API_Calls"]

    for col in required_columns:
        assert col in df.columns

    # Check that API calls are non-negative
    assert (df["API_Calls"] >= 0).all()


def test_relationship_score_range():
    """Test that relationship scores are within valid range"""
    from dashboard import generate_executive_data

    df = generate_executive_data()

    # Relationship scores should be between 0 and 100
    assert (df["Relationship_Score"] >= 0).all()
    assert (df["Relationship_Score"] <= 100).all()


def test_account_health_range():
    """Test that account health scores are within valid range"""
    from dashboard import generate_account_planning_data

    df = generate_account_planning_data()

    # Health scores should be between 0 and 100
    assert (df["Health_Score"] >= 0).all()
    assert (df["Health_Score"] <= 100).all()


if __name__ == "__main__":
    pytest.main([__file__])
