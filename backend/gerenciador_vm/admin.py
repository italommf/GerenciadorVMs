from django.contrib import admin
from .models import Maquinas_Virtuais

class Maquinas_VirtuaisAdmin(admin.ModelAdmin):
    
    list_display = ('nome_de_usuario', 'favoritada', 'area_de_trabalho', 'id', 'endereco_computador')
    list_editable = ('favoritada',)

class Maquinas_VirtuaisAdmin(admin.ModelAdmin):
    pass

admin.site.register(Maquinas_Virtuais, Maquinas_VirtuaisAdmin)