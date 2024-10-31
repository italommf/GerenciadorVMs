from pandas import DataFrame
from django.urls import path

from .views import (
    listar_vms, 
    adicionar_vm, 
    adicionar_rpa, 
    listar_todas_as_robotizacoes, 
    listar_robotizacoes_vms, 
    abrir_vm,
    listar_vms_abertas,
    abrir_todas_as_vms,
    abrir_vms_favoritadas
)

urlpatterns = [
    path('adicionar_vm/', adicionar_vm, name = 'Adicionar Máquina Virtual'),
    path('adicionar_rpa/', adicionar_rpa, name = 'Adicionar Robotizações'),
    path('listar_vms_cadastradas/', listar_vms, name = 'Listar Máquinas Virtuais'),
    path('listar_todas_as_robotizacoes/', listar_todas_as_robotizacoes, name = 'Listar Todas as Robotizações'),
    path('listar_robotizacoes_vms/<int:id_da_vm>/', listar_robotizacoes_vms, name = 'Listar Todas as Robotizações de Uma VM'),
    path('abrir_vm/<int:vm_id>/', abrir_vm, name = 'Abrir uma Máquina Virtual'),
    path('listar_vms_abertas/', listar_vms_abertas, name = 'Listar Máquinas Virtuais Abertas'),
    path('abrir_todas_as_vms/', abrir_todas_as_vms, name = ' Abrir Todas as Máquinas Virtuais'),
    path('abrir_vms_favoritadas/', abrir_vms_favoritadas, name = ' Abrir Todas as Máquinas Virtuais Favoritadas')
]

