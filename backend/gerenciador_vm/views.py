import psutil
from time import sleep
import pyvda 
from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Maquinas_Virtuais, VMProcesso, VMProcesso
from .serializers import MaquinasVirtuaisSerializer

from django.http import JsonResponse
from .services import ConexaoAreaDeTrabalhoRemota, Utils

@api_view(['GET'])
def listar_vms(request):

    vms = Maquinas_Virtuais.objects.all()

    serializer = MaquinasVirtuaisSerializer(
        vms,
        many = True
    )

    return Response(serializer.data)

@api_view(['POST'])
def adicionar_vm(request):

    if request.method == 'POST':
        serializer = MaquinasVirtuaisSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def abrir_vm(request, vm_id):

    try:
        utils = Utils()
        vm = get_object_or_404(Maquinas_Virtuais, id=vm_id)
        conexao = ConexaoAreaDeTrabalhoRemota()

        # conexao.gerenciar_area_de_trabalho(vm)

        process_id = conexao.abrir_janela_conexao_remota(mais_opcoes=True)
        if process_id is not None:            
            conexao.autenticar_na_vm(
                process_id=process_id,
                endereco=vm.endereco_computador,  
                nome_usuario=vm.nome_de_usuario,   
                senha=vm.senha,                  
                usar_todos_os_monitores=vm.usar_todos_os_monitores  
            )

            VMProcesso.objects.create(
                maquina_virtual = vm, 
                process_id = process_id,
                nome_usuario = vm.nome_de_usuario
            )

            # conexao.gerenciar_janelas(process_id, 1)

            utils.enviar_mensagem_telegram(
                f"*VM Aberta*\n\n"
                f"*VM:* {vm.nome_de_usuario}\n"
                f"*IP:* {vm.endereco_computador}\n"
                f"*Área de trabalho:* {vm.area_de_trabalho}\n"
            )

            return JsonResponse({"message": "VM aberta com sucesso", "process_id": process_id})
        else:
            return JsonResponse({"error": "Falha ao abrir a VM"}, status = 500)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
def listar_vms_abertas(request):

    vm_processos = VMProcesso.objects.all()
    data = []
    processos_para_remover = []


    for vm_processo in vm_processos:
        process_id = vm_processo.process_id

        if psutil.pid_exists(process_id):
            data.append(
                {
                    'vm_id': vm_processo.maquina_virtual.id,
                    'nome_usuario': vm_processo.maquina_virtual.nome_de_usuario,
                    'area_de_trabalho': vm_processo.maquina_virtual.area_de_trabalho,
                    'endereco_computador': vm_processo.maquina_virtual.endereco_computador,
                    'process_id': process_id,
                    'criado_em': vm_processo.criado_em,
                }
        )
        else:
            processos_para_remover.append(vm_processo.id)

    if processos_para_remover:
        VMProcesso.objects.filter(id__in=processos_para_remover).delete()

    return JsonResponse({'VMs Abertas': data})

@api_view(['GET'])
def abrir_todas_as_vms(request):

    try:

        utils = Utils()
        vms = Maquinas_Virtuais.objects.all()
        
        resultado_abertura = []

        conexao = ConexaoAreaDeTrabalhoRemota()

        for vm in vms:

            conexao.gerenciar_area_de_trabalho(vm)
            process_id = conexao.abrir_janela_conexao_remota(mais_opcoes=True)

            if process_id is not None:
                conexao.autenticar_na_vm(
                    process_id=process_id,
                    endereco=vm.endereco_computador,
                    nome_usuario=vm.nome_de_usuario,
                    senha=vm.senha,
                    usar_todos_os_monitores=vm.usar_todos_os_monitores
                )

                sleep(1)

                VMProcesso.objects.create(
                    maquina_virtual = vm, 
                    process_id = process_id,
                    nome_usuario = vm.nome_de_usuario
                )

                resultado_abertura.append(
                    {
                        'vm_id': vm.id,
                        'nome_usuario': vm.nome_de_usuario,
                        'process_id': process_id,
                        'status': 'VM aberta com sucesso'
                    }
                )
                utils.enviar_mensagem_telegram(
                    f"*VM Aberta*\n\n"
                    f"*VM:* {vm.nome_de_usuario}\n"
                    f"*IP:* {vm.endereco_computador}\n"
                    f"*Área de trabalho:* {vm.area_de_trabalho}\n"
                )

            else:
                resultado_abertura.append(
                    {
                        'vm_id': vm.id,
                        'nome_usuario': vm.nome_de_usuario,
                        'status': 'Erro ao abrir a VM'
                    }
                )
                utils.enviar_mensagem_telegram(
                    f'''
                    Erro na abertura de uma VM\n\n
                    
                    [PROCESSO ID]: None\n

                    Usuário: {vm.nome_de_usuario}\n
                    Endereço: {vm.endereco_computador}\n
                    Área de trabalho: {vm.area_de_trabalho}\n
                    '''
                )

        return JsonResponse({"resultado": resultado_abertura})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@api_view(['GET'])
def abrir_vms_favoritadas(request):

    try:

        utils = Utils()
        vms = Maquinas_Virtuais.objects.filter(
            favoritada = True
        )

        resultado_abertura = []

        conexao = ConexaoAreaDeTrabalhoRemota()

        for vm in vms:

            conexao.gerenciar_area_de_trabalho(vm)
            process_id = conexao.abrir_janela_conexao_remota(mais_opcoes=True)

            if process_id is not None:
                conexao.autenticar_na_vm(
                    process_id=process_id,
                    endereco=vm.endereco_computador,
                    nome_usuario=vm.nome_de_usuario,
                    senha=vm.senha,
                    usar_todos_os_monitores=vm.usar_todos_os_monitores
                )

                sleep(1)

                VMProcesso.objects.create(
                    maquina_virtual = vm, 
                    process_id = process_id,
                    nome_usuario = vm.nome_de_usuario
                )

                resultado_abertura.append(
                    {
                        'vm_id': vm.id,
                        'nome_usuario': vm.nome_de_usuario,
                        'process_id': process_id,
                        'status': 'VM favorita aberta com sucesso'
                    }
                )
                utils.enviar_mensagem_telegram(
                    f"*VM favorita Aberta*\n\n"
                    f"*VM:* {vm.nome_de_usuario}\n"
                    f"*IP:* {vm.endereco_computador}\n"
                    f"*Área de trabalho:* {vm.area_de_trabalho}\n"
                )

            else:
                resultado_abertura.append(
                    {
                        'vm_id': vm.id,
                        'nome_usuario': vm.nome_de_usuario,
                        'status': 'Erro ao abrir a VM favoritada'
                    }
                )
                utils.enviar_mensagem_telegram(
                    f'''
                    Erro na abertura de uma VM favoritada\n\n
                    
                    [PROCESSO ID]: None\n

                    Usuário: {vm.nome_de_usuario}\n
                    Endereço: {vm.endereco_computador}\n
                    Área de trabalho: {vm.area_de_trabalho}\n
                    '''
                )

        return JsonResponse({"resultado": resultado_abertura})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)