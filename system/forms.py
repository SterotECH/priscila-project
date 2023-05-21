from django.core.exceptions import ValidationError
from django import forms
from .models import Income, Category, Expenditure

class IncomeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit the choices to income categories only
        self.fields['category'].queryset = Category.objects.filter(type='I')

    class Meta:
        model = Income
        fields = ['date', 'amount', 'description', 'category']

class ExpenditureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit the choices to income categories only
        self.fields['category'].queryset = Category.objects.filter(type='E')

    class Meta:
        model = Expenditure
        fields = ['date', 'amount', 'description', 'category', 'recipient']
