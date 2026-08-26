import sys
from pathlib import Path

import streamlit as st
import pandas as pd


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# PROJECT IMPORTS
# ============================================================

from src.data_processing.data_loader import (
    load_dashboard_data,
)

from src.inventory.risk_analysis import (
    prepare_inventory_risk,
)

from src.inventory.recommendations import (
    prepare_recommendations,
)

from src.dashboard.dashboard_utils import (
    get_inventory_summary,
    get_recommendation_metrics,
    get_model_metrics,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FORESIGHT",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    data = load_dashboard_data()

    data["inventory_risk"] = prepare_inventory_risk(
        data["inventory_risk"]
    )

    data["recommendations"] = prepare_recommendations(
        data["recommendations"]
    )

    return data


try:

    data = load_data()

except Exception as e:

    st.error("Unable to load FORESIGHT data.")

    st.exception(e)

    st.stop()


feature_engineered = data["feature_engineered"]
inventory_risk = data["inventory_risk"]
recommendations = data["recommendations"]
evaluation_summary = data["evaluation_summary"]
evaluation_details = data["evaluation_details"]


# ============================================================
# HEADER
# ============================================================

st.title("📊 Project FORESIGHT")

st.subheader(
    "Demand Forecasting & Inventory Intelligence Dashboard"
)

st.markdown(
    """
    FORESIGHT combines demand analysis, inventory risk analysis,
    forecasting evaluation and inventory recommendations into
    a single decision-support dashboard.
    """
)


# ============================================================
# SIDEBAR FILTER
# ============================================================

st.sidebar.header("Filters")

if "sku_id" in inventory_risk.columns:

    sku_options = sorted(
        inventory_risk["sku_id"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_skus = st.sidebar.multiselect(
        "Select SKU",
        sku_options,
    )

else:

    selected_skus = []


filtered_risk = inventory_risk.copy()

if selected_skus:

    filtered_risk = filtered_risk[
        filtered_risk["sku_id"]
        .astype(str)
        .isin(selected_skus)
    ]


filtered_recommendations = recommendations.copy()

if selected_skus:

    filtered_recommendations = (
        filtered_recommendations[
            filtered_recommendations["sku_id"]
            .astype(str)
            .isin(selected_skus)
        ]
    )


# ============================================================
# SUMMARY METRICS
# ============================================================

inventory_summary = get_inventory_summary(
    filtered_risk
)

recommendation_metrics = get_recommendation_metrics(
    filtered_recommendations
)

model_metrics = get_model_metrics(
    evaluation_summary
)


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total SKUs",
        inventory_summary["total_skus"],
    )

with col2:

    st.metric(
        "Stockout Records",
        inventory_summary["stockout_records"],
    )

with col3:

    st.metric(
        "High Risk Records",
        inventory_summary["high_risk_records"],
    )

with col4:

    st.metric(
        "Recommended Units",
        f"{recommendation_metrics['total_recommended_units']:,.0f}",
    )


# ============================================================
# INVENTORY RISK
# ============================================================

st.header("Inventory Risk Analysis")

if "risk_category" in filtered_risk.columns:

    risk_counts = (
        filtered_risk["risk_category"]
        .value_counts()
        .reset_index()
    )

    risk_counts.columns = [
        "Risk Category",
        "Records",
    ]

    st.bar_chart(
        risk_counts.set_index("Risk Category")
    )


# ============================================================
# RECOMMENDATIONS
# ============================================================

st.header("Inventory Recommendations")

if not filtered_recommendations.empty:

    display_columns = [
        "date",
        "sku_id",
        "category",
        "subcategory",
        "inventory_risk",
        "recommendation_priority",
        "recommended_order_qty",
        "recommendation",
    ]

    display_columns = [
        col
        for col in display_columns
        if col in filtered_recommendations.columns
    ]

    st.dataframe(
        filtered_recommendations[
            display_columns
        ],
        use_container_width=True,
    )

else:

    st.info("No recommendation records available.")


# ============================================================
# MODEL PERFORMANCE
# ============================================================

st.header("Model Performance")

if model_metrics:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "MAE",
            f"{model_metrics['mae']:.2f}",
        )

    with col2:
        st.metric(
            "RMSE",
            f"{model_metrics['rmse']:.2f}",
        )

    with col3:
        st.metric(
            "MAPE",
            f"{model_metrics['mape']:.2f}%",
        )

    with col4:
        st.metric(
            "Forecast Accuracy",
            f"{model_metrics['forecast_accuracy']:.2f}%",
        )


# ============================================================
# FORECAST EVALUATION DETAILS
# ============================================================

st.header("Forecast Evaluation Details")

if not evaluation_details.empty:

    st.dataframe(
        evaluation_details,
        use_container_width=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Project FORESIGHT | Demand Forecasting & Inventory Intelligence"
)