import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
import seaborn as sns

load_dotenv()

DB_USER = os.getenv('DB_USER', 'fallback-user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'fallback-password')
DB_HOST = os.getenv('DB_HOST', 'fallback-host')
DB_NAME = os.getenv('DB_NAME', 'fallback-db-name')
DB_AUTH_PLUGIN = os.getenv('DB_AUTH_PLUGIN', 'fallback-auth-plugin')

def get_connection_to_db():
    try:
        connection = mysql.connector.connect(
        user = DB_USER,
        password = DB_PASSWORD,
        host = DB_HOST,
        database = DB_NAME,
        auth_plugin = DB_AUTH_PLUGIN)
        
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Połączono z bazą danych MySQL... Wersja: ", db_Info)
        return connection
    except Error as e:
        print("Błąd podczas łączenia z bazą danych", e)
        return None
    
weekdays_pl = {
    'Monday': 'Poniedziałek',
    'Tuesday': 'Wtorek',
    'Wednesday': 'Środa',
    'Thursday': 'Czwartek',
    'Friday': 'Piątek',
    'Saturday': 'Sobota',
    'Sunday': 'Niedziela'
}

class ExpenseTracker: 

    def __init__(self):
        self.create_expenses_table()

    def create_expenses_table(self):
        connection = get_connection_to_db()
        cursor = connection.cursor()
        create_table_query = """
            CREATE TABLE IF NOT EXISTS expenses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                expense_date DATE NOT NULL,
                day_of_week VARCHAR(10) NOT NULL,
                category VARCHAR(255) NOT NULL,
                amount DECIMAL(10, 2) NOT NULL
            )
        """
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        connection.close()

    def add_expense(self, category, amount, expense_date):
        day_of_week = expense_date.strftime('%A')
        day_of_week = weekdays_pl[day_of_week]
        connection = get_connection_to_db()
        if connection is not None:
            cursor = connection.cursor()

            data = {'expense_date': expense_date,
                    'day_of_week': day_of_week,
                    'category': category,
                    'amount': amount,
                    }

            add_expense_query = """INSERT INTO expenses (expense_date, day_of_week, category, amount) VALUES
                 (%(expense_date)s, %(day_of_week)s, %(category)s, %(amount)s)"""
            
            cursor.execute(add_expense_query, data)
            connection.commit()
            cursor.close()
            connection.close()
            return f"Dodano wydatek: {category} - {amount} Data: {expense_date}({day_of_week})"
        else:
            return 'Błąd podczas zbierania danych.'

    def show_expenses(self):
        try:
            connection = get_connection_to_db()
            if connection is not None:
                cursor = connection.cursor()
                query = 'SELECT * FROM expenses;'
                cursor.execute(query)
                display_lst = []
                for row in cursor.fetchall():
                    display_lst.append(f'Data: {row[1]}, Dzień: {row[2]}, Kategoria: {row[3]}, Kwota: {row[4]}')
                cursor.close()
                connection.close()
                return "\n".join(display_lst)
            else:
                return 'Błąd podczas zbierania danych.'
        except Error as e:
            return f"Błąd podczas łączenia z bazą danych: {e}"
            
    def sum_expenses(self):
        connection = get_connection_to_db()
        cursor = connection.cursor()
        query = 'SELECT amount FROM expenses;'

        cursor.execute(query)

        total = 0

        for i in cursor.fetchall():
            total += i[0]

        cursor.close()
        connection.close()

        return float(total)
            
    def show_categories(self):
        connection = get_connection_to_db()
        cursor = connection.cursor()
        query = 'SELECT category FROM expenses;'

        cursor.execute(query)

        categories = [category[0] for category in cursor.fetchall()]

        unique_categories = []

        for i in categories:
            if i not in unique_categories:
                unique_categories.append(i)


        cursor.close()
        connection.close()

        return ", ".join(unique_categories)

    def show_for_category(self, category):
        connection = get_connection_to_db()
        cursor = connection.cursor()
        query = 'SELECT amount, expense_date, day_of_week FROM expenses WHERE category = %(category)s;'

        data = {'category': category}

        cursor.execute(query,data)

        amounts_lst = []
        for row in cursor.fetchall():
            amounts_lst.append(f'{row[1]}, {row[2]}, Kwota: {row[0]}')

        return ",\n".join(amounts_lst)

    def sum_for_category(self, category):
        connection = get_connection_to_db()
        cursor = connection.cursor()
        query = 'SELECT amount FROM expenses WHERE category = %(category)s;'

        data = {'category': category}

        cursor.execute(query,data)

        total = 0

        for row in cursor.fetchall():
            total += row[0]

        return f'Suma wydatków dla kategorii {category}: {total}'
        
    def show_chart(self):
        connection = get_connection_to_db()
        if connection is not None:
            try:
                cursor = connection.cursor()
                query = 'SELECT category, SUM(amount) as total_amount FROM expenses GROUP BY category;'
                cursor.execute(query)
                
                categories = []
                amounts = []
                for (category, total_amount) in cursor:
                    categories.append(category)
                    amounts.append(total_amount)
                
                cursor.close()
                connection.close()
                plt.figure(figsize=(10, 6))
                sns.barplot(x=categories, y=amounts)
                plt.xlabel('Kategoria', fontsize=14)
                plt.ylabel('Łączna kwota', fontsize=14)
                plt.title('Wydatki dla kategorii', fontsize=16)
                plt.xticks(rotation=45)
                plt.grid(axis='y')
                plt.show()
            except Error as e:
                print(f"Błąd podczas łączenia z bazą danych: {e}")
        else:
            print("Błąd podczas łączenia z bazą danych")