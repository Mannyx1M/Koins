from expense import Expense
import datetime
import calendar
import csv
import os

expense_file_path = "expenses.csv"


def main():
    print("Welcome to Koins Expense Tracker!")

    # Choose budget period
    print("\nChoose your budget period:")
    print("1. Daily")
    print("2. Weekly")
    print("3. Monthly")

    budget_choice = input("Enter your choice (1-3): ")

    if budget_choice == "1":
        budget_period = "Daily"
    elif budget_choice == "2":
        budget_period = "Weekly"
    elif budget_choice == "3":
        budget_period = "Monthly"
    else:
        print("Invalid choice!")
        return

    # Enter budget
    budget = float(input(f"\nEnter your {budget_period.lower()} budget £: "))

    # Enter expenses
    while True:
        expense = get_user_expense()
        save_expense_to_file(expense, expense_file_path)

        another_expense = input("\nDo you want to add another expense? (yes/no): ")

        if another_expense.lower() != "yes":
            break

    # Summarise expenses
    summarize_expenses(expense_file_path, budget, budget_period)


def get_user_expense():

    print("\nGetting User Expense")

    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount £: "))

    expense_categories = [
        "Food",
        "Home",
        "Work",
        "Fun",
        "Misc"
    ]

    while True:
        print("\nSelect a category:")

        for i, category_name in enumerate(expense_categories):
            print(f"{i + 1}. {category_name}")

        selected_index = int(input("Enter category number: ")) - 1

        if selected_index in range(len(expense_categories)):

            selected_category = expense_categories[selected_index]

            new_expense = Expense(
                name=expense_name,
                category=selected_category,
                amount=expense_amount
            )

            return new_expense

        else:
            print("Invalid category. Please try again!")


def save_expense_to_file(expense: Expense, expense_file_path):

    file_exists = os.path.exists(expense_file_path)

    with open(expense_file_path, "a", newline="") as file:

        writer = csv.writer(file)

        # Add column headings if the file is new or empty
        if not file_exists or os.path.getsize(expense_file_path) == 0:
            writer.writerow(["Name", "Amount", "Category", "Date"])

        writer.writerow([
            expense.name,
            expense.amount,
            expense.category,
            datetime.date.today()
        ])

    print("Expense saved successfully!")


def summarize_expenses(expense_file_path, budget, budget_period):

    expenses = []

    today = datetime.date.today()

    # Work out the start and end of the selected period
    if budget_period == "Daily":
        start_date = today
        end_date = today

    elif budget_period == "Weekly":
        start_date = today - datetime.timedelta(days=today.weekday())
        end_date = start_date + datetime.timedelta(days=6)

    else:
        start_date = today.replace(day=1)

        last_day = calendar.monthrange(today.year, today.month)[1]
        end_date = today.replace(day=last_day)

    # Read expenses from CSV file
    with open(expense_file_path, "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            expense_date = datetime.date.fromisoformat(row["Date"])

            if start_date <= expense_date <= end_date:

                expense = Expense(
                    name=row["Name"],
                    amount=float(row["Amount"]),
                    category=row["Category"]
                )

                expenses.append(expense)

    # Calculate spending by category
    amount_by_category = {}

    for expense in expenses:

        if expense.category in amount_by_category:
            amount_by_category[expense.category] += expense.amount

        else:
            amount_by_category[expense.category] = expense.amount

    print("\n========== EXPENSE SUMMARY ==========")

    for category, amount in amount_by_category.items():
        print(f"{category}: £{amount:.2f}")

    # Calculate total spending
    total_spent = sum(expense.amount for expense in expenses)

    remaining_budget = budget - total_spent

    print("-------------------------------------")
    print(f"{budget_period} Budget: £{budget:.2f}")
    print(f"Total Spent: £{total_spent:.2f}")
    print(f"Budget Remaining: £{remaining_budget:.2f}")

    # Calculate daily spending allowance
    remaining_days = (end_date - today).days + 1

    daily_budget = remaining_budget / remaining_days

    print(f"Daily Budget Available: £{daily_budget:.2f}")
    print("=====================================")


if __name__ == "__main__":
    main()