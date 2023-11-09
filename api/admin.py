from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserKey, VaultItem, VaultCollection


class UserKeyInline(admin.TabularInline):
    model = UserKey
    readonly_fields = ('created_at', 'modified_at')


class VaultCollectionInline(admin.TabularInline):
    model = VaultCollection
    readonly_fields = ('uuid',)
    show_change_link = True
    extra = 0


class VaultItemInline(admin.TabularInline):
    model = VaultItem
    readonly_fields = ('uuid', 'created_at', 'modified_at',)
    extra = 0


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
            }
         ),
    )
    list_display = ('email', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    inlines = (UserKeyInline, VaultCollectionInline,)


class UserKeyAdmin(admin.ModelAdmin):
    ordering = ('user',)
    search_fields = ('user',)
    list_display = ('user', 'encrypted_symmetric_key', 'created_at', 'modified_at',)


class VaultCollectionAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)
    list_display = ('name', 'uuid',)
    inlines = (VaultItemInline,)


class VaultItemAdmin(admin.ModelAdmin):
    ordering = ('modified_at',)
    list_display = ('encrypted_data', 'uuid', 'created_at', 'modified_at',)


admin.site.register(User, UserAdmin)
admin.site.register(UserKey, UserKeyAdmin)
admin.site.register(VaultCollection, VaultCollectionAdmin)
admin.site.register(VaultItem, VaultItemAdmin)
