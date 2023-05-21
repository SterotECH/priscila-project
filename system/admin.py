import datetime
from django.contrib import admin
from django import forms
from django.db import models
from system.forms import ExpenditureForm, IncomeForm
from unfold.admin import ModelAdmin
from unfold.forms import UserChangeForm, UserCreationForm
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from import_export.admin import ImportExportModelAdmin
from django.contrib.humanize.templatetags.humanize import intcomma, naturaltime

from system.models import Member, Ministry, Tithe, Transaction, Category, Income, Expenditure, Account

class TransactionAdmin(ModelAdmin):
    list_display = ['amount_formatted', 'description', 'category', 'formatted_date']
    list_filter = ['date']
    date_hierarchy = 'date'
    search_fields = ['description']
    autocomplete_fields = ['category']

    def amount_formatted(self, obj):
        return f"GHC {intcomma(obj.amount)}"
    amount_formatted.short_description = 'Amount'


    def formatted_date(self, obj):
        datetime_obj = datetime.datetime.combine(obj.date, datetime.time())
        return naturaltime(datetime_obj)
    formatted_date.short_description = 'Created At'


@admin.register(Member)
class MemberAdminModel(ModelAdmin, ImportExportModelAdmin):
    list_display = ['name', 'email', 'ministry', 'is_active']
    list_editable = ['is_active']
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_per_page = 20
    search_fields = ['name']
    date_hierarchy = 'date_joined'
    list_filter = ['ministry']
    save_as_continue = True
    show_full_result_count = True
    form = UserChangeForm
    add_form = UserCreationForm
    readonly_fields = ["date_joined"]
    add_fieldsets = (
        ('Personal Information', {
            'classes': ('wide',),
            'fields': ('name', 'telephone','ministry', 'email', 'location' ),
        }),
          ('Guardian Information', {
            'classes': ('wide',),
            'fields': ('fathers_name', 'mothers_name', 'guardians_name' ),
        }),
        ('Status', {
            'classes': ('wide',),
            'fields': ('is_active','is_schooling','is_working','pays_tithe'),
        }),
        (("Important dates"), {
            'classes': ('wide',),
            "fields": ["date_joined"]
        }),
    )
    fieldsets = (
      ('Personal Information', {
            'classes': ('wide',),
            'fields': ('name', 'telephone','ministry', 'email', 'location' ),
        }),
          ('Guardian Information', {
            'classes': ('wide',),
            'fields': ('fathers_name', 'mothers_name', 'guardians_name' ),
        }),
        ('Status', {
            'classes': ('wide',),
            'fields': ('is_active','is_schooling','is_working','pays_tithe'),
        }),
        (("Important dates"), {
            'classes': ('wide',),
            "fields": ["date_joined"]
        }),
    )

@admin.register(Ministry)
class MinistryAdminModel(ModelAdmin, ImportExportModelAdmin):
    list_display = ['name', 'leader']
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_editable = ['leader']


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['description']
    ordering = ['name']

@admin.register(Income)
class IncomeAdmin(TransactionAdmin):
    pass



@admin.register(Expenditure)
class ExpenditureAdmin(TransactionAdmin):
    list_display = TransactionAdmin.list_display + ['recipient']


@admin.register(Account)
class AccountAdmin(ModelAdmin):
    list_display = ['balance_formatted', 'total_incomes', 'total_expenditures', 'formatted_date']
    readonly_fields = ['balance']

    def balance_formatted(self, obj):
        return f"GHC {intcomma(obj.balance)}"
    balance_formatted.short_description = 'Balance'

    def formatted_date(self, obj):
        return naturaltime(obj.created_at)
    formatted_date.short_description = 'Created At'

    def total_incomes(self, obj):
        incomes = Income.objects.all()
        tithes = Tithe.objects.all()
        total = sum(income.amount for income in incomes) + sum(tithe.amount for tithe in tithes)
        return f"GHC {intcomma(total)}"
    total_incomes.short_description = 'Total Income'

    def total_expenditures(self, obj):
        expenditures = Expenditure.objects.all()
        total = sum(expenditure.amount for expenditure in expenditures)
        return f"GHC {intcomma(total)}"
    total_expenditures.short_description = 'Total Expenditure'




@admin.register(Tithe)
class TitheAdmin(ModelAdmin):
    autocomplete_fields = ['member']
    list_display = ['member', 'amount', 'formatted_date']
    list_filter = ['date']
    date_hierarchy = 'date'
    search_fields = ['member__name']

    def formatted_date(self, obj):
        datetime_obj = datetime.datetime.combine(obj.date, datetime.time())
        return naturaltime(datetime_obj)
    formatted_date.short_description = 'Time'
