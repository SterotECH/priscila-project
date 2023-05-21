from django.shortcuts import render
from .models import Balance, Member, Ministry, Tithe, User, Income

def index(request):
    # Fetch the required data from the database or other sources
    current_balance = Balance.objects.get(pk=1).amount
    total_active_members = Member.objects.filter(is_active=True).count()
    total_ministries = Ministry.objects.count()
    total_users = User.objects.count()

    # Retrieve recent income and tithes
    recent_incomes_tithes = Income.objects.order_by('-date')[:5]
    recent_incomes_tithes |= Tithe.objects.order_by('-date')[:5]

    context = {
        'current_balance': current_balance,
        'total_active_members': total_active_members,
        'total_ministries': total_ministries,
        'total_users': total_users,
        'recent_incomes_tithes': recent_incomes_tithes,
    }

    return render(request, 'admin/index.html', context)
