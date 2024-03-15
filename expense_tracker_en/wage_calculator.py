import pandas as pd
import matplotlib.pyplot as plt


tax_related_variables = {
    'Contract':{
        'Pension_rate': 0.0976,
        'Rent_insurance_rate': 0.015,
        'Sickness_insurance_rate': 0.0245,
        'Healthcare_insurance_rate': 0.09,
        'Tax_lowering_rate': 300,
        'Work_cost_rate1': 250,
        'Work_cost_rate2': 300,
        'Income_tax_rate': 0.12,
        },
    'Mandate':{
        'Pension_rate': 0.0976,
        'Rent_insurance_rate': 0.015,
        'Sickness_insurance_rate': 0.0245,
        'Healthcare_insurance_rate': 0.09,
        'Work_cost_rate': 0.2,
        'Income_tax_rate': 0.12,
    }
}

class Contract:
    def __init__(self, gross_income, work_place, age=None):
        self.age = age
        self.work_place = work_place
        self.gross_income = gross_income
        self.data = []

    def calculate_pension(self):
        pension_insurance = self.gross_income * 0.0976
        return float('%.2f' % pension_insurance)
        
    def calculate_rent(self):
        rent_insurance = self.gross_income * 0.015
        return float('%.2f' % rent_insurance)
        
    def calculate_sickness(self):
        sickness_insurance = self.gross_income * 0.0245
        return float('%.2f' % sickness_insurance)

    def calculate_healthcare(self):
        base = self.gross_income - self.calculate_pension() - self.calculate_rent() - self.calculate_sickness()
        healthcare_tax = base * 0.09
        return float('%.2f' % healthcare_tax)

    def calculate_income_tax(self):
        if self.age <= 26:
            return 0
        else:
            base = self.gross_income - self.calculate_pension() - self.calculate_rent() - self.calculate_sickness()
            tax_lowering_rate = 300

            if self.work_place == 'yes':
                work_cost = 250
            else:
                work_cost = 300

            income_tax_base = base - work_cost
        
            income_tax = 0.12 * round(income_tax_base) - tax_lowering_rate

            return round(income_tax)

    def calculate_net_income(self):
        net_income = self.gross_income - self.calculate_pension() - self.calculate_rent() - self.calculate_sickness() - self.calculate_healthcare()- self.calculate_income_tax()
        return net_income

    def save_data(self):
        tax_data = {}
        tax_data['Pension'] = [self.calculate_pension()]
        tax_data['Rent'] = [self.calculate_rent()]
        tax_data['Sickness'] = [self.calculate_sickness()]
        tax_data['Healthcare'] = [self.calculate_healthcare()]
        tax_data['PIT advance'] = [self.calculate_income_tax()]
        tax_data['Net'] = [self.calculate_net_income()]

        self.data.append(tax_data)
        df = pd.concat([pd.DataFrame(i) for i in self.data], ignore_index=True)
        df.to_csv('tax_data.csv', index=False)

    def display_chart(self):
        df = pd.read_csv('tax_data.csv')
        fig, ax = plt.subplots(figsize=(8, 4))
        labels = df.columns.tolist()
        sizes = df.iloc[-1].tolist()
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6']
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.set_title('')
        ax.legend(labels, loc='best')

        for i, label in enumerate(labels):
            ax.text(-3.1, 0.7-i*0.2, f"{label}: {sizes[i]:.2f}", fontsize=9)
        plt.show()

class MandateContract:
    def __init__(self, gross_income, status, student, sickness_info, age=None):
        self.gross_income = gross_income
        self.age = age
        self.status = status
        self.student = student
        self.sickness_info = sickness_info
        self.data = []

    def calculate_pension(self):
        if self.status == 'yes':
            pension_insurance = self.gross_income * 0.0976
            return float('%.2f' % pension_insurance)
        else:
            return 0
        
    def calculate_rent(self):
        if self.status == 'yes':
            rent_insurance = self.gross_income * 0.015
            return float('%.2f' % rent_insurance)
        else:
            return 0
        
    def calculate_sickness(self):
        if self.status == 'yes' and self.sickness_info == 'yes':
            sickness_insurance = self.gross_income * 0.0245
            return float('%.2f' % sickness_insurance)
        else:
            return 0
        
    def calculate_healthcare(self):
        if self.student == 'yes':
            return 0
        else:
            base = self.gross_income - self.calculate_pension() - self.calculate_rent() - self.calculate_sickness()
            healthcare_tax = base * 0.09
            return float('%.2f' % healthcare_tax)
        
    def calculate_income_tax(self):
        if self.age <= 26:
            return 0
        if self.student == 'yes':
            return 0
        else:
            base = self.gross_income - self.calculate_pension() - self.calculate_rent() - self.calculate_sickness()
            work_cost = base * 0.2
            tax_base = base - work_cost
            income_tax = 0.12 * round(tax_base)
            return round(income_tax)

    def calculate_net_income(self):
        net_income = self.gross_income - self.calculate_pension() - self.calculate_rent() - self.calculate_sickness() - self.calculate_healthcare()- self.calculate_income_tax()
        return net_income

    def save_data(self):
        tax_data = {}
        tax_data['Pension'] = [self.calculate_pension()]
        tax_data['Rent'] = [self.calculate_rent()]
        tax_data['Sickness'] = [self.calculate_sickness()]
        tax_data['Healthcare'] = [self.calculate_healthcare()]
        tax_data['PIT advance'] = [self.calculate_income_tax()]
        tax_data['Net'] = [self.calculate_net_income()]

        self.data.append(tax_data)
        df = pd.concat([pd.DataFrame(i) for i in self.data], ignore_index=True)
        df.to_csv('tax_data.csv', index=False)

    def display_chart(self):
        df = pd.read_csv('tax_data.csv')
        fig, ax = plt.subplots(figsize=(8, 4))
        labels = df.columns.tolist()
        sizes = df.iloc[-1].tolist()
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6']
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.set_title('')
        ax.legend(labels, loc='best')

        for i, label in enumerate(labels):
            ax.text(-3.1, 0.7-i*0.2, f"{label}: {sizes[i]:.2f}", fontsize=9)
        plt.show()