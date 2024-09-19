from django.contrib import admin
from .models import Maquinas_Virtuais, Robotizacoes

class RobotizacoesAdmin(admin.ModelAdmin):

    list_display = ('nome_do_robo', 'get_nome_de_usuario_vm')

    def get_nome_de_usuario_vm(self, obj):
        return obj.maquina_virtual.nome_de_usuario
    
    get_nome_de_usuario_vm.short_description = 'Nome de Usuário (VM)'

class Maquinas_VirtuaisAdmin(admin.ModelAdmin):
    list_display = ('nome_de_usuario', 'area_de_trabalho', 'id', 'endereco_computador')

admin.site.register(Maquinas_Virtuais, Maquinas_VirtuaisAdmin)
admin.site.register(Robotizacoes, RobotizacoesAdmin)