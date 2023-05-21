from django.contrib import admin
from core.models import User
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



@admin.register(User)
class UserAdminModel(BaseUserAdmin, ModelAdmin):
    list_display = ['username', 'name', 'email', 'user_type', 'is_active']
    list_editable = ['is_active']
    list_per_page = 20
    search_fields = ['username']
    date_hierarchy = 'date_joined'
    empty_value_display = '--'
    list_filter = ['user_type']
    save_as_continue = False
    show_full_result_count = True
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    readonly_fields = ["last_login", "updated_at", "date_joined"]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', )
        }),
        ('Personal Information', {
            'classes': ('wide',),
            'fields': ('name', 'contact', 'user_type', ),
        }),
        ('Permissions', {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_superuser' ),
        }),
        ('Account Status',{
            'classes': ('wide'),
            'fields': ['is_verified']
            }),
        ('Groups', {
            'classes': ('wide',),
            'fields': ('groups', 'user_permissions', ),
        }),
        (("Important dates"), {
            'classes': ('wide',),
            "fields": ("last_login", "updated_at", "date_joined")
        }),
    )
    fieldsets = (
        ('Account Information', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', )
        }),
        ('Personal Information', {
            'classes': ('wide',),
            'fields': ('name', 'contact', 'user_type', ),
        }),
        ('Permissions', {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_superuser', ),
        }),
        ('Account Status',{
            'classes': ('wide'),
            'fields': ['is_verified']
            }),
        ('Groups', {
            'classes': ('wide',),
            'fields': ('groups', 'user_permissions', ),
        }),
        (("Important dates"), {
            'classes': ('wide',),
            "fields": ("last_login", "updated_at", "date_joined")
        }),
    )

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
