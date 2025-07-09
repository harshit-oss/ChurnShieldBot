import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="ChurnShield Chatbot", layout="centered")
st.title("🤖 ChurnShield - Smart Churn Chatbot")

# Load dataset
try:
    df = pd.read_csv(r"C:\Users\pande\OneDrive\Documents\Euro Truck Simulator 2\mod\churnshield dataset\chatbot\Churn_predictions.csv")
except FileNotFoundError:
    st.error("❌ File 'churn_predictions.csv' not found!")
    st.stop()

# Clean column names
df.columns = df.columns.str.strip()

# Fix missing Risk Level column if needed
if "Risk Level" not in df.columns or df["Risk Level"].isnull().all():
    df["Risk Level"] = df["Predicted Churn Risk"].apply(
        lambda x: "High" if x > 0.75 else "Medium" if x > 0.5 else "Low"
    )

# Show sample questions as dropdown hint
sample_questions = [
    "Who are the high risk customers?",
    "Who are the low risk customers?",
    "Who are the medium risk customers?",
    "What is the average churn probability?",
    "What is the churn count by contract?",
    "How many customers are at high risk?",
    "How many customers are currently active?",
    "Which gender has more churned customers?",
    "Churn by internet service",
    "Churn by payment method",
    "Top 5 customers by churn probability",
    "Tenure distribution of churned customers",
    "Show churn count by Senior Citizen"
]

selected = st.selectbox("🧠 Need suggestions? Pick a question or type your own:", sample_questions)

query = st.text_input("💬 Ask your churn-related question:", value=selected)

if query:
    query = query.lower()

    if "high risk" in query:
        st.subheader("🚨 High Risk Customers (Top 10)")
        st.dataframe(df[df["Risk Level"] == "High"].head(10))

    elif "low risk" in query and "count" in query:
        count = (df["Risk Level"] == "Low").sum()
        st.success(f"🟢 Total Low-Risk Customers: {count}")

    elif "medium risk" in query and "count" in query:
        count = (df["Risk Level"] == "Medium").sum()
        st.success(f"🟡 Total Medium-Risk Customers: {count}")

    elif "low risk" in query:
        st.subheader("🟢 Low-Risk Customers (Top 10)")
        st.dataframe(df[df["Risk Level"] == "Low"].head(10))

    elif "medium risk" in query:
        st.subheader("🟡 Medium-Risk Customers (Top 10)")
        st.dataframe(df[df["Risk Level"] == "Medium"].head(10))

    elif "average" in query and "churn" in query:
        avg = df["Predicted Churn Risk"].mean()
        st.success(f"📊 Average Churn Probability: {avg:.2f}")

    elif "contract" in query and "churn" in query:
        chart = df[df["Actual Churn(Yes/No)"] == "Yes"].groupby("Contract").size()
        st.subheader("📉 Churn Count by Contract")
        st.bar_chart(chart)

    elif "how many" in query and "high risk" in query:
        count = (df["Risk Level"] == "High").sum()
        st.success(f"🔢 Total High-Risk Customers: {count}")

    elif "active" in query or "not churned" in query:
        count = (df["Actual Churn(Yes/No)"] == "No").sum()
        st.success(f"✅ Active (Non-Churned) Customers: {count}")

    elif "gender" in query:
        if "gender" in df.columns:
            chart = df[df["Actual Churn(Yes/No)"] == "Yes"].groupby("gender").size()
            st.subheader("👩‍🦱 Churn by Gender")
            st.bar_chart(chart)
        else:
            st.warning("⚠️ 'gender' column not found in your data.")

    elif "internet" in query:
        chart = df[df["Actual Churn(Yes/No)"] == "Yes"].groupby("InternetService").size()
        st.subheader("🌐 Churn by Internet Service")
        st.bar_chart(chart)

    elif "payment" in query:
        total = df.groupby("PaymentMethod").size()
        churn = df[df["Actual Churn(Yes/No)"] == "Yes"].groupby("PaymentMethod").size()
        rate = (churn / total).fillna(0)
        st.subheader("💳 Churn Rate by Payment Method")
        st.bar_chart(rate)

    elif "top 5" in query:
        top5 = df.sort_values(by="Predicted Churn Risk", ascending=False).head(5)
        st.subheader("🔝 Top 5 Customers by Churn Probability")
        st.dataframe(top5)

    elif "tenure" in query:
        st.subheader("📈 Tenure Distribution of Churned Customers")
        st.bar_chart(df[df["Actual Churn(Yes/No)"] == "Yes"]["tenure"].value_counts().sort_index())

    elif "senior" in query:
        if "SeniorCitizen" in df.columns:
            chart = df[df["Actual Churn(Yes/No)"] == "Yes"].groupby("SeniorCitizen").size()
            st.subheader("👴 Churn by Senior Citizen Status")
            st.bar_chart(chart)
        else:
            st.warning("⚠️ 'SeniorCitizen' column not found.")

    else:
        st.warning("🤖 Sorry, I didn’t understand that. Try selecting a question above.")

