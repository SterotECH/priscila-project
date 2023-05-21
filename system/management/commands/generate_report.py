from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from system.models import Income, Expenditure, Tithe
from django.db import models


class Command(BaseCommand):
    help = 'Generate a report of net balance, incomes, tithes, and expenditures for a specified period'

    def add_arguments(self, parser):
        parser.add_argument('period', type=str, help='The period for which to generate the report (week/month)')

    def handle(self, *args, **options):
        period = options['period']
        start_date, end_date = self.get_period_dates(period)

        # Fetch transactions for the specified period
        incomes = Income.objects.filter(date__range=(start_date, end_date))
        tithes = Tithe.objects.filter(date__range=(start_date, end_date))
        expenditures = Expenditure.objects.filter(date__range=(start_date, end_date))

        # Calculate net balance, debit, and credit amounts
        net_balance = self.calculate_net_balance(incomes, tithes, expenditures)
        debit_amount = self.calculate_debit_amount(incomes, tithes)
        credit_amount = self.calculate_credit_amount(expenditures)

        # Generate the report
        report = self.generate_report(period, start_date, end_date, net_balance, debit_amount, credit_amount)

        # Display or save the report as desired
        print(report)

    def get_period_dates(self, period):
        today = datetime.today().date()
        if period == 'week':
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        elif period == 'month':
            start_date = today.replace(day=1)
            end_date = start_date.replace(day=1, month=start_date.month+1) - timedelta(days=1)
        else:
            raise ValueError("Invalid period. Please specify 'week' or 'month'.")

        return start_date, end_date

    def calculate_net_balance(self, incomes, tithes, expenditures):
        total_income = incomes.aggregate(total=models.Sum('amount'))['total'] or 0
        total_tithe = tithes.aggregate(total=models.Sum('amount'))['total'] or 0
        total_expenditure = expenditures.aggregate(total=models.Sum('amount'))['total'] or 0

        net_balance = total_income + total_tithe - total_expenditure
        return net_balance

    def calculate_debit_amount(self, incomes, tithes):
        total_income = incomes.aggregate(total=models.Sum('amount'))['total'] or 0
        total_tithe = tithes.aggregate(total=models.Sum('amount'))['total'] or 0

        debit_amount = total_income + total_tithe
        return debit_amount

    def calculate_credit_amount(self, expenditures):
        total_expenditure = expenditures.aggregate(total=models.Sum('amount'))['total'] or 0

        credit_amount = total_expenditure
        return credit_amount

    def generate_report(self, period, start_date, end_date, net_balance, debit_amount, credit_amount):
        report = f"Report for {period.capitalize()} ({start_date} - {end_date}):\n"
        report += f"Net Balance: {net_balance}\n"
        report += f"Debit Amount (Incomes and Tithes): {debit_amount}\n"
        report += f"Credit Amount (Expenditures): {credit_amount}\n"

        return report
