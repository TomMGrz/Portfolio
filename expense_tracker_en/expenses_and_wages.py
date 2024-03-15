from expense_tracker.expense_calculator import ExpenseTracker
from expense_tracker.wage_calculator import Contract, MandateContract
import datetime


tracker = ExpenseTracker()

tracker = ExpenseTracker()

while True:
    print('1. Expense management.')
    print('2. Salary calculator.')
    print('3. Exit')
    user_choice = input("Select an option from the menu: ")
    ex_calculator = False
    tax_calculator = False

    if user_choice == '1':
        ex_calculator = True

    while ex_calculator:
        print('\nExpense management: ')
        print('')
        print('1. Add expense.')
        print('2. Show expenses')
        print('3. Sum expenses')
        print('4. Show expense categories')
        print('5. Show data for selected category')
        print('6. Sum expenses for selected category')
        print('7. Show expense chart.')
        print('8. Return.\n')
        user_choice = input('Select an option: ')

        if user_choice == '1':
            expense_date = datetime.date.today()
            category = input('Enter category: ')
            amount = float(input('Enter amount: '))
            print(tracker.add_expense(category, amount, expense_date))
        if user_choice == '2':
            print(tracker.show_expenses())
        if user_choice == '3':
            print(tracker.sum_expenses())
        if user_choice == '4':
            print(tracker.show_categories())
        if user_choice == '5':
            category = input('Select category: ')
            print(tracker.show_for_category(category))
        if user_choice == '6':
            category = input('Select category: ')
            print(tracker.sum_for_category(category))
        if user_choice == '7':
            print(tracker.show_chart())
        if user_choice == '8':
            break

    if user_choice == '2':
        tax_calculator = True

    while tax_calculator:
        print('\nSalary calculator: ')
        print('')
        print('1. Calculate salary for employment contract.')
        print('2. Calculate salary for mandate contract.')
        print('3. Return\n')

        user_choice = input('Select an option: ')

        if user_choice == '1':
            gross_income = float(input('Enter gross salary: '))
            work_place = input('Do you live in the same city you work? yes/no ')
            age = int(input('Enter age: '))
            contract = Contract(gross_income, work_place, age)
            contract.save_data()
            contract.display_chart()

        if user_choice == '2':
            gross_income = float(input('Enter gross salary: '))
            status = input('Do you pay social security contributions at this employer? yes/no ')
            student = input('Are you a student up to 26 years old: yes/no ')
            sickness_info = input('Do you pay voluntary sickness contribution? yes/no ')
            age = int(input('Enter age: '))
            man_contract = MandateContract(gross_income, status, student, sickness_info, age)
            man_contract.save_data()
            man_contract.display_chart()

        if user_choice == '3':
            break

    if user_choice == '3':
        exit()