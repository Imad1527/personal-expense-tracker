from tabulate import tabulate
from database import (
    add_expense,
    view_all_expenses,
    filter_expenses_by_category,
    filter_expenses_by_date,
    get_total_spent,
    init_db
)

def main():
    init_db()  # ensure table exists before anything runs

    while True:
        print("\n== Personal Expense Tracker ==")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Filter by Category")
        print("4. Filter by Date")
        print("5. Show Total Spent")
        print("6. Exit")

        choice = input("Choose an option (1-6): ")

        if choice == "1":
            date = input("Enter the date (YYYY-MM-DD): ")
            category = input("Enter the category (e.g., Food, Travel): ")
            amount = input("Enter the amount: ")
            description = input("Enter a short description: ")

            try:
                amount = float(amount)
                add_expense(date, category, amount, description)
                print("✅ Expense added successfully!")
            except ValueError:
                print("❌ Amount must be a number. Please try again.")

        elif choice == "2":
            expenses = view_all_expenses()
            if not expenses:
                print("📭 No expenses recorded yet.")
            else:
                headers = ["Date", "Category", "Amount", "Description"]
                print("\n📒 Expense History:\n")
                print(tabulate(expenses, headers=headers, tablefmt="grid"))

        elif choice == "3":
            category = input("Enter category to filter by: ")
            filtered = filter_expenses_by_category(category)
            if not filtered:
                print(f"📭 No expenses found under category: {category}")
            else:
                headers = ["Date", "Category", "Amount", "Description"]
                print(f"\n📂 Expenses in Category: {category}\n")
                print(tabulate(filtered, headers=headers, tablefmt="grid"))

        elif choice == "4":
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            filtered = filter_expenses_by_date(start_date, end_date)
            if not filtered:
                print(f"📭 No expenses between {start_date} and {end_date}")
            else:
                headers = ["Date", "Category", "Amount", "Description"]
                print(f"\n📆 Expenses from {start_date} to {end_date}\n")
                print(tabulate(filtered, headers=headers, tablefmt="grid"))

        elif choice == "5":
            total = get_total_spent()
            print(f"\n💰 Total spent so far: ₹{total:.2f}")

        elif choice == "6":
            print("👋 Exiting... Goodbye!")
            break

        else:
            print("⚠️ Invalid choice. Please select a number between 1 and 6.")

if __name__ == "__main__":
    main()
