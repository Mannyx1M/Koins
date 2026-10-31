
import streamlit as st
import pandas as pd
import os
import datetime
import calendar

# Page settings
st.set_page_config(
    page_title="Koins Budget Tracker",
    page_icon="💰",
    layout="wide"
)

# CSV file
expense_file_path = "expenses.csv"

# Create CSV file if it doesn't exist
if not os.path.exists(expense_file_path):
    df = pd.DataFrame(columns=["Name", "Amount", "Category", "Date"])
    df.to_csv(expense_file_path, index=False)


# Function to read expenses
def load_expenses():
    return pd.read_csv(expense_file_path)


# Function to save expenses
def save_expense(name, amount, category):

    new_expense = pd.DataFrame([{
        "Name": name,
        "Amount": amount,
        "Category": category,
        "Date": datetime.date.today()
    }])

    new_expense.to_csv(
        expense_file_path,
        mode="a",
        header=False,
        index=False
    )


# App title
st.title("💰 Koins Budget Tracker")
st.write("Welcome to your personal budget dashboard!")

# Sidebar
st.sidebar.title("Budget Settings")

budget_period = st.sidebar.selectbox(
    "Choose your budget period",
    ["Daily", "Weekly", "Monthly"]
)

budget = st.sidebar.number_input(
    "Enter your budget (£)",
    min_value=0.0,
    value=1000.0,
    step=50.0
)

# Work out budget dates
today = datetime.date.today()

if budget_period == "Daily":
    start_date = today

elif budget_period == "Weekly":
    start_date = today - datetime.timedelta(days=today.weekday())

else:
    start_date = today.replace(day=1)

# Load expenses
expenses = load_expenses()

# Convert dates
expenses["Date"] = pd.to_datetime(expenses["Date"]).dt.date

# Filter expenses for selected period
period_expenses = expenses[
    expenses["Date"] >= start_date
]

# Calculate spending
total_spent = period_expenses["Amount"].sum()

remaining_budget = budget - total_spent

# Dashboard
st.subheader(f"{budget_period} Budget Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Budget", f"£{budget:.2f}")

with col2:
    st.metric("Total Spent", f"£{total_spent:.2f}")

with col3:
    st.metric("Remaining Budget", f"£{remaining_budget:.2f}")

st.divider()

# Add expense section
st.subheader("➕ Add a New Expense")

with st.form("expense_form"):

    expense_name = st.text_input("Expense name")

    expense_amount = st.number_input(
        "Expense amount (£)",
        min_value=0.0,
        step=1.0
    )

    expense_category = st.selectbox(
        "Choose a category",
        ["Food", "Home", "Work", "Fun", "Misc"]
    )

    submitted = st.form_submit_button("Add Expense")

    if submitted:

        if expense_name and expense_amount > 0:

            save_expense(
                expense_name,
                expense_amount,
                expense_category
            )

            st.success("Expense saved successfully!")
            st.rerun()

        else:
            st.error("Please enter an expense name and amount.")

st.divider()

# Spending by category
st.subheader("📊 Spending by Category")

if not period_expenses.empty:

    category_totals = period_expenses.groupby(
        "Category"
    )["Amount"].sum()

    st.bar_chart(category_totals)

else:
    st.info("No expenses recorded for this period yet.")

st.divider()

# All expenses
st.subheader("📋 Your Expenses")

if not expenses.empty:

    st.dataframe(
        expenses.sort_values("Date", ascending=False),
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("You haven't added any expenses yet.")

