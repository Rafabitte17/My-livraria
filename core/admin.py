"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core.models import Autor, Categoria, Compra, Editora, ItensCompra, Livro, User


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email')
    search_fields = ('nome', 'email')
    list_filter = ('nome',)
    ordering = ('nome', 'email')
    list_per_page = 10


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    search_fields = ('descricao',)
    list_filter = ('descricao',)
    ordering = ('descricao',)
    list_per_page = 10


# class ItensCompraInline(admin.TabularInline):
class ItensCompraInline(admin.StackedInline):
    model = ItensCompra
    extra = 1  # Quantidade de itens adicionais


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'status', 'total_formatado')
    ordering = ('usuario', 'status')
    list_per_page = 10
    inlines = [ItensCompraInline]
    readonly_fields = ('total_formatado',)

    @admin.display(description='Total')
    def total_formatado(self, obj):
        """Exibe R$ 123,45 em vez de 123.45."""
        return f'R$ {obj.total:.2f}'


@admin.register(Editora)
class EditoraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'cidade')
    search_fields = ('nome', 'email', 'cidade')
    list_filter = ('nome', 'email', 'cidade')
    ordering = ('nome', 'email', 'cidade')
    list_per_page = 10


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'categoria',
        'editora',
    )
    search_fields = ('titulo', 'editora__nome', 'categoria__descricao', 'isbn')
    list_filter = ('editora', 'categoria')
    ordering = ('categoria', 'editora', 'titulo')
    list_per_page = 10


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Personal Info'),
            {
                'fields': (
                    'name',
                    'passage_id',
                    'foto',
                )
            },
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            },
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Groups'), {'fields': ('groups',)}),
        (_('User Permissions'), {'fields': ('user_permissions',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'name',
                    'foto',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
    )
