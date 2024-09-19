import os
import pythoncom
import subprocess
from time import sleep
from pathlib import Path
import uiautomation as automation

from pyvda.utils import Managers
from pyvda import AppView, get_apps_by_z_order, VirtualDesktop, get_virtual_desktops

class ConexaoAreaDeTrabalhoRemota:

    def abrir_janela_conexao_remota(self, mais_opcoes=True):

        pythoncom.CoInitialize()

        try:
            def _abrir_app():
                try:
                    command = ["mstsc"]
                    process = subprocess.Popen(command)
                    print("Aplicativo de Conexão de Área de Trabalho Remota aberto.")
                    return process.pid
                except subprocess.CalledProcessError as e:
                    print(f"Erro ao abrir o aplicativo de conexão remota: {e}")
                    return None
                
            def _verificar_se_janela_esta_ativa(pid):
                vm = automation.WindowControl(searchDepth=1, ProcessId=pid, Name="Conexão de Área de Trabalho Remota")
                if vm.Exists(10.0, 0):
                    vm.SetActive()
                    vm.SetFocus()
                    print(f"[GerenciadorVM][SUCESSO] Conexão de Área de Trabalho Remota identificada pelo UiAutomation")
                    return vm
                else:
                    print(f"[GerenciadorVM][ERRO] O SCI não foi aberto corretamente!")
                return None
            
            def _mostrar_mais_opcoes(vm):
                botao_mais_opcoes = vm.ButtonControl(searchDepth=2, Name="Mostrar Opções ")
                if botao_mais_opcoes.Exists(2.0, 0):
                    botao_mais_opcoes.SetFocus()
                    botao_mais_opcoes.Click()
                
                botao_ocultar_opcoes = vm.ButtonControl(searchDepth=2, Name="Ocultar Opções ")
                if botao_ocultar_opcoes.Exists(2.0, 0):
                    return True
                return False

            process_id = _abrir_app()
            if process_id is not None:
                sleep(1)
                vm = _verificar_se_janela_esta_ativa(process_id)

                if mais_opcoes and vm is not None:
                    _mostrar_mais_opcoes(vm)
                    
            return process_id
        
        finally:   
            pythoncom.CoUninitialize()
            
    def autenticar_na_vm(self, process_id, endereco, nome_usuario, senha, usar_todos_os_monitores = False):

        def _identificar_janela():
            vm = automation.WindowControl(searchDepth=1, ProcessId=process_id)
            if vm.Exists(2, 0):
                if 'Conexão de Área de Trabalho Remota' not in vm.Name:
                    print(f"Janela diferente encontrada, PID possivelmente errado: {process_id}: {vm.Name}")
                    return None
                
                vm.SetActive()
                vm.SetFocus()
                print(f"VM encontrada para o Process ID {process_id}: {vm.Name}")
                return vm
            else:
                print(f"[ERRO] Janela não encontrada para o PID {process_id}")
                return None

        def _enviar_credenciais(vm):
            campo_computador = vm.EditControl(searchDepth=4, ClassName='Edit', Name='Computador:')
            if not campo_computador.Exists(1, 0):
                print('[ERRO] Campo "Computador" não encontrado!')
                return None
            
            campo_computador.SetFocus()
            campo_computador.SendKeys("{Ctrl}a{Delete}")
            campo_computador.SendKeys(endereco)

            campo_nome_de_usuario = vm.EditControl(searchDepth=4, ClassName='Edit', Name='Nome de usuário:')
            if not campo_nome_de_usuario.Exists(1, 0):
                print('[ERRO] Campo "Nome de usuário" não encontrado!')
                return None
            campo_nome_de_usuario.SetFocus()
            campo_nome_de_usuario.SendKeys("{Ctrl}a{Delete}")
            campo_nome_de_usuario.SendKeys(nome_usuario)

        def _gerenciar_monitores(vm):
            janela_exibicao = vm.TabItemControl(searchDepth=3, Name='Exibição')
            if not janela_exibicao.Exists(1, 0):
                print('[ERRO] Aba "Exibição" não encontrada!')
                return None  
            janela_exibicao.Click()      

            checkbox_usar_todos_os_monitores = vm.CheckBoxControl(searchDepth=3, ClassName='Button', Name='Usar todos os meus monitores para a sessão remota')
            if not checkbox_usar_todos_os_monitores.Exists(1, 0):
                print('[ERRO] Checkbox "Usar todos os meus monitores para a sessão remota" não encontrado!')
                return None
            
            acao = checkbox_usar_todos_os_monitores.GetLegacyIAccessiblePattern().DefaultAction

            if usar_todos_os_monitores:
                if acao == 'Selecionar':
                    checkbox_usar_todos_os_monitores.Click()
                    print('[SUCESSO] O Checkbox foi marcado para usar todos os monitores!')
                     
            elif not usar_todos_os_monitores:
                acao = checkbox_usar_todos_os_monitores.GetLegacyIAccessiblePattern().DefaultAction
                if acao == 'Desmarcar':
                    checkbox_usar_todos_os_monitores.Click()
                    print('[SUCESSO] O Checkbox foi desmarcado. Não usará todos os monitores!')


        def _conectar(vm):
            botao_conectar = vm.ButtonControl(searchDepth=1, ClassName='Button', Name='Conectar')
            if not botao_conectar.Exists(1, 0):
                print('[ERRO] Botão "Conectar" não encontrado!')
                return None
            botao_conectar.SetFocus()
            botao_conectar.Click()
    
        def _enviar_senha(vm):
            janela_seguranca_windows = vm.WindowControl(searchDepth=1, ClassName='Credential Dialog Xaml Host', Name='Segurança do Windows')
            if not janela_seguranca_windows.Exists(3, 0):
                print('[ERRO] Janela "Segurança do Windows" não encontrada!')
                return None
            janela_seguranca_windows.SetFocus()
            janela_seguranca_windows.Click()
            janela_seguranca_windows.SendKeys(senha, interval=0.05)

            botao_ok = janela_seguranca_windows.ButtonControl(searchDepth=1, ClassName='Button', Name='OK')
            if not botao_ok.Exists(1, 0):
                print('[ERRO] Botão "Ok" não encontrado!')
                return None
            botao_ok.SetFocus()
            botao_ok.Click()

        vm = _identificar_janela()
        if vm is not None:
            _enviar_credenciais(vm)
            _gerenciar_monitores(vm)
            _conectar(vm)
            _enviar_senha(vm)

            sleep(5)
            
            vm = _identificar_janela()
            if endereco in vm.Name:
                print('Máquina virtual aberta com sucesso')
            else:
                print('[ERRO] A máquina virtual não foi autenticada corretamente!')
        else:
            print("[ERRO] Falha ao identificar a janela da VM durante o processo de autenticação.")

    def gerenciar_area_de_trabalho(self, area_de_trabalho):

        def _verificar_numero_de_desktops():

            quantidade_desktops_ativos = len(get_virtual_desktops())
            return quantidade_desktops_ativos

        def _ciar_area_de_trabalho(area_de_trabalho):

            managers = Managers()

            while True:

                quantidade_areas_de_trabalho = _verificar_numero_de_desktops()

                if quantidade_areas_de_trabalho < area_de_trabalho:
                   
                   nova_area_de_trabalho = managers.manager_internal.create_desktop()
                   virtual_desktop = VirtualDesktop(desktop = nova_area_de_trabalho)
                   print(f'Área de trabalho {quantidade_areas_de_trabalho + 1} criada')

                   continue
                
                break

        def _ir_para_area_de_trabalho(area_de_trabalho):

            areas_de_trabalho_ativas = get_virtual_desktops()
            desktop_destino = areas_de_trabalho_ativas[area_de_trabalho - 1]
            desktop_destino.go()
            print(f'Área de trabalho {area_de_trabalho - 1} aberta!')

        _ciar_area_de_trabalho(area_de_trabalho)
        _ir_para_area_de_trabalho(area_de_trabalho)

if __name__ == '__main__':

    conexao = ConexaoAreaDeTrabalhoRemota()

    # pid = conexao.abrir_janela_conexao_remota()

#     conexao.autenticar_na_vm(
#         pid,
#         '192.168.1.38',
#         r'contauditoria\devrobot.consultaopt',
#         r'DBeWxrni8Ux6gnRjKY6k',
#         usar_todos_os_monitores = False
#     )

    conexao.gerenciar_area_de_trabalho(2)