from django.contrib import admin
from .models import Client, ClientContact, ClientFile



class ClientContactAdmin(admin.TabularInline):
    model= ClientContact
    extra=1
    classes= ['collapse']
    fields=(
        'first_name',
        'last_name',
        'cargo',
        't_number',
        'email',
    )

class ClientFileAdmin(admin.TabularInline):
    model=ClientFile
    extra=1
    classes= ['collapse']
    fields=(
        'file',
        'descripcion',
        'created_at',
    )
    readonly_fields= (
        'created_at',
    )

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        'tipo',
        't_number',
        'email',
        'direccion',
        'cif_nif',
        'other',
        'created_at',
    ]

    search_fields=(
        "name",
        't_number',
        'email',
        'cif_nif',
    )

    list_filter = [
        'tipo',
        'created_at',
        ]    
    ordering = [
        'name',
        'tipo',
        'created_at',
        
    ]

    inlines= [
        ClientContactAdmin,
        ClientFileAdmin,
    ]

    fieldsets=(
        'Información del Cliente', {
            'fields' :("name",
        'tipo',
        't_number',
        'email',
        'direccion',
        'other',
        'created_at',)
        }
    ),
    (
        'Notas internas', {
            'fields': (
                'cargo',
            ),
            'classes':(
                'collapse',
            )
        }
    )