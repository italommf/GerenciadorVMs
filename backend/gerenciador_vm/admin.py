from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Maquinas_Virtuais

class Maquinas_VirtuaisAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_de_usuario', 'abrir_vm', 'favoritada', 'usar_todos_os_monitores', 'area_de_trabalho', )
    list_editable = ('favoritada', 'usar_todos_os_monitores', 'area_de_trabalho')
    list_display_links = ('nome_de_usuario',)

    def abrir_vm(self, obj):
        return format_html(
            '<a class="button" href="{}" target="_blank">Abrir VM</a>',
            reverse('Abrir uma Máquina Virtual', args=[obj.id])
        )
    abrir_vm.short_description = 'Ações'
    abrir_vm.allow_tags = True

admin.site.register(Maquinas_Virtuais, Maquinas_VirtuaisAdmin)
