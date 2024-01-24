import json
from datetime import datetime

class BudgetTracker:
    def __init__(self, filename='transactions.json'):
        self.filename = filename
        self.transactions = self.load_transactions()

    def load_transactions(self):
        try:
            with open(self.filename, 'r') as file:
                transactions = json.load(file)
            return transactions
        except (FileNotFoundError, json.JSONDecodeError):
            return {'income': [], 'expenses': []}

    def save_transactions(self):
        with open(self.filename, 'w') as file:
            json.dump(self.transactions, file, indent=2)

    def add_income(self, amount, category):
        transaction = {'type': 'income', 'amount': amount, 'category': category, 'timestamp': str(datetime.now())}
        self.transactions['income'].append(transaction)
        self.save_transactions()
        print(f'Income entry of ${amount} in category "{category}" recorded successfully.')

    def add_expense(self, amount, category):
        transaction = {'type': 'expense', 'amount': amount, 'category': category, 'timestamp': str(datetime.now())}
        self.transactions['expenses'].append(transaction)
        self.save_transactions()
        print(f'Expense entry of ${amount} in category "{category}" recorded successfully.')

    def calculate_budget(self):
        total_income = sum(item['amount'] for item in self.transactions['income'])
        total_expenses = sum(item['amount'] for item in self.transactions['expenses'])
        remaining_budget = total_income - total_expenses
        return remaining_budget

    def analyze_expenses(self):
        expense_categories = {}
        for expense in self.transactions['expenses']:
            category = expense['category']
            amount = expense['amount']
            if category not in expense_categories:
                expense_categories[category] = amount
            else:
                expense_categories[category] += amount

        if not expense_categories:
            print('No expenses recorded for analysis.')
        else:
            print('Expense Analysis:')
            for category, amount in expense_categories.items():
                print(f'{category}: ${amount}')

def main():
    budget_tracker = BudgetTracker()

    while True:
        print('\nBudget Tracker Menu:')
        print('1. Add Income')
        print('2. Add Expense')
        print('3. Calculate Remaining Budget')
        print('4. Analyze Expenses')
        print('5. Exit')

        choice = input('Enter your choice (1-5): ')

        if choice == '1':
            amount = float(input('Enter income amount: $'))
            category = input('Enter income category: ')
            budget_tracker.add_income(amount, category)
        elif choice == '2':
            amount = float(input('Enter expense amount: $'))
            category = input('Enter expense category: ')
            budget_tracker.add_expense(amount, category)
        elif choice == '3':
            remaining_budget = budget_tracker.calculate_budget()
            print(f'Remaining Budget: ${remaining_budget}')
        elif choice == '4':
            budget_tracker.analyze_expenses()
        elif choice == '5':
            print('Exiting the Budget Tracker. Goodbye!')
            break
        else:
            print('Invalid choice. Please enter a number between 1 and 5.')

if __name__ == '__main__':
    main()
