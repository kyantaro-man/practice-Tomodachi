from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from friendslist.models import User, Friend, Category, Memo
from friendslist.forms import UserCreationForm

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
            )
        }),
        (None, {
            'fields': (
                'is_active',
                'is_admin',
            )
        })
    )

    list_display = ('email', 'is_active')
    list_filter = ()
    ordering = ()
    filter_horizontal = ()

    add_fieldsets = (
        (None, {
            'fields': ('email', 'password',),
        }),
    )

    add_form = UserCreationForm

admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Friend)
admin.site.register(Category)
admin.site.register(Memo)