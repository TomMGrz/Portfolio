from pierwszy_projekt.expense_calculator import ExpenseTracker
from pierwszy_projekt.wage_calculator import Contract, MandateContract
import datetime


tracker = ExpenseTracker()

while True:
    print('1. Zarządzanie wydatkami.')
    print('2. Kalkulator wynagrodzeń.')
    print('3. Wyjdź')
    user_choice = input("Wybierz pozycję z menu: ")
    ex_calculator = False
    tax_calculator = False

    if user_choice =='1':
        ex_calculator = True
    
    while ex_calculator == True:
        print('\nZarządzanie wydatkami: ')
        print('')
        print('1. Dodaj wydatek.')
        print('2. Pokaż wydatki')
        print('3. Sumuj wydatki')
        print('4. Pokaż kategorie wydatków')
        print('5. Pokaż dane dla wybranej kategorii')
        print('6. Sumuj wydatki dla wybranej kategorii')
        print('7. Pokaż wykres wydatków.')
        print('8. Wróć.\n')
        user_choice = input('Wybierz opcję: ')

        if user_choice == '1':
            expense_date = datetime.date.today()
            category = str(input('Wpisz kategorię: '))
            amount = float(input('Wpisz kwotę: '))
            print(tracker.add_expense(category, amount, expense_date))
        if user_choice == '2':
            print(tracker.show_expenses())
        if user_choice == '3':
            print(tracker.sum_expenses())
        if user_choice == '4':
            print(tracker.show_categories())
        if user_choice == '5':
            category = str(input('Wybierz kategorię: '))
            print(tracker.show_for_category(category))
        if user_choice == '6':
            category = str(input('Wybierz kategorię: '))
            print(tracker.sum_for_category(category))
        if user_choice == '7':
            print(tracker.show_chart())
        if user_choice == '8':
            break

    if user_choice == '2':
        tax_calculator = True

    while tax_calculator == True:
        print('\nKalkulator wynagrodzeń: ')
        print('')
        print('1. Oblicz wynagrodzenie dla umowy o pracę. ')
        print('2. Oblicz wynagrodzenie dla umowy zlecenia. ')
        print('3. Wróć \n')

        user_choice = input('Wybierz opcję: ')
        
        if user_choice == '1':
            gross_income = float(input('Podaj wypłatę brutto: '))
            work_place = input('Czy mieszkasz w tej samej miejscowości, co pracujesz? tak/nie ')
            age = int(input('Podaj wiek: '))
            contract = Contract(gross_income, work_place, age)
            contract.save_data()
            contract.display_chart()

        if user_choice == '2':
            gross_income = float(input('Podaj wypłątę brutto: '))
            status = input('Czy odprowadzasz składki na ubezpieczenia społeczne u tego pracodawcy?: tak/nie ')
            student = input('Czy jesteś studentem do 26 roku życia: tak/nie ')
            sickness_info = input('Czy opłacasz dobrowolną składkę chorobową?: tak/nie ')
            age = int(input('Podaj wiek: '))
            man_contract = MandateContract(gross_income, status, student, sickness_info, age)
            man_contract.save_data()
            man_contract.display_chart()

        if user_choice == '3':
            break

    if user_choice == '3':
        exit()