import requests
import pythoncom
import subprocess
from time import sleep
from pyvda.utils import Managers
import uiautomation as automation
from django.db.models import Count
from .models import Maquinas_Virtuais
from pyvda import VirtualDesktop, get_virtual_desktops

import win32api
import win32gui
import win32con

from settings_decouple import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID 

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
                if vm.Exists(3.0, 0):
                    vm.SetFocus()
                    vm.SetActive()
                    print(f"[GerenciadorVM][SUCESSO] Conexão de Área de Trabalho Remota identificada pelo UiAutomation")
                    return vm
                else:
                    print(f"[GerenciadorVM][ERRO] O SCI não foi aberto corretamente!")
                return None
            
            def _mostrar_mais_opcoes(vm):

                vm.SetFocus()

                botao_mais_opcoes = vm.ButtonControl(searchDepth=2, Name="Mostrar Opções ")
                if botao_mais_opcoes.Exists(2.0, 0):
                    botao_mais_opcoes.SetFocus()
                    botao_mais_opcoes.Click()
                    print(f"[GerenciadorVM] Mais opções foram exibidas na autenticação!")
                
                botao_ocultar_opcoes = vm.ButtonControl(searchDepth=2, Name="Ocultar Opções ")
                if botao_ocultar_opcoes.Exists(2.0, 0):
                    return True
                return False

            process_id = _abrir_app()
            if process_id is not None:
                sleep(1)
                vm = _verificar_se_janela_esta_ativa(process_id)

                sleep(1)

                if mais_opcoes and vm is not None:
                    _mostrar_mais_opcoes(vm)
                    
            return process_id
        
        finally:   
            pythoncom.CoUninitialize()
            
    def autenticar_na_vm(self, process_id, endereco, nome_usuario, senha, usar_todos_os_monitores = False):

        def _identificar_janela(autenticado = False):

            vm = automation.WindowControl(searchDepth=1, ProcessId=process_id, Name="Conexão de Área de Trabalho Remota")
            if vm.Exists(2, 0):
                if 'Conexão de Área de Trabalho Remota' not in vm.Name and not autenticado:
                    print(f"Janela diferente encontrada, PID possivelmente errado: {process_id}: {vm.Name}")
                    return None                
                vm.SetActive()
                vm.SetFocus()
                print(f"VM encontrada para o Process ID {process_id}: {vm.Name}")
                return vm
            
            elif autenticado:

                vm = automation.WindowControl(searchDepth=1, ProcessId=process_id)
                if vm.Exists(2, 0):
                    if 'Conexão de Área de Trabalho Remota' not in vm.Name and not autenticado:
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

            sleep(0.5)
    
        def _enviar_senha(vm):
            janela_seguranca_windows = vm.WindowControl(searchDepth=1, ClassName='Credential Dialog Xaml Host', Name='Segurança do Windows')
            if not janela_seguranca_windows.Exists(2, 0):
                print('[ERRO] Janela "Segurança do Windows" não encontrada dentro do objeto VM!')

                janela_seguranca_windows = automation.WindowControl(searchDepth=1, ClassName='Credential Dialog Xaml Host', Name='Segurança do Windows')
                if not janela_seguranca_windows.Exists(2, 0):
                    print('[ERRO] Janela "Segurança do Windows" não encontrada em AUTOMATION!')
                    return None
                
            janela_seguranca_windows.SetFocus()
            janela_seguranca_windows.SetActive()
            janela_seguranca_windows.Click()
            janela_seguranca_windows.SendKeys(senha, interval=0.05)

            botao_ok = janela_seguranca_windows.ButtonControl(searchDepth=1, ClassName='Button', Name='OK')
            if not botao_ok.Exists(1, 0):
                print('[ERRO] Botão "Ok" não encontrado!')
                return None
            botao_ok.SetFocus()
            botao_ok.MoveCursorToInnerPos()
            botao_ok.Click()

        vm = _identificar_janela()
        if vm is not None:
            _enviar_credenciais(vm)
            _gerenciar_monitores(vm)
            _conectar(vm)
            _enviar_senha(vm)

            sleep(2)
            
            vm = _identificar_janela(autenticado = True) # TODO Corrigir erro de logica
            if endereco in vm.Name:
                print('Máquina virtual aberta com sucesso')
            else:
                print('[ERRO] A máquina virtual não foi autenticada corretamente!')
        else:
            print("[ERRO] Falha ao identificar a janela da VM durante o processo de autenticação.")

    def gerenciar_area_de_trabalho(self, vm):

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

                   sleep(0.5)

                   continue
                
                break

        def _ir_para_area_de_trabalho(area_de_trabalho):

            areas_de_trabalho_ativas = get_virtual_desktops()
            desktop_destino = areas_de_trabalho_ativas[area_de_trabalho - 1]
            desktop_destino.rename(vm.nome_de_usuario)
            desktop_destino.go()
            print(f'Área de trabalho {area_de_trabalho - 1} aberta!')

        _ciar_area_de_trabalho(vm.area_de_trabalho)
        _ir_para_area_de_trabalho(vm.area_de_trabalho)

    def gerenciar_janelas(self, pid, total_de_vms, numero_do_app):

        window = automation.WindowControl(searchDepth=1, ProcessId=pid)
        
        if window.Exists(0, 0):
            hwnd = window.NativeWindowHandle
            print(f"Janela encontrada: PID {pid}, HWND {hwnd}")
            
            screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
            screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

            if total_de_vms == 1:
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, screen_width, screen_height, 0)

            elif total_de_vms == 2:
                # Dois aplicativos, divididos ao meio (um à esquerda e um à direita)
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, screen_width // 2, screen_height, 0)
                # Exemplo para a segunda janela, que ocuparia a outra metade
                # win32gui.SetWindowPos(hwnd_2, win32con.HWND_TOP, screen_width // 2, 0, screen_width // 2, screen_height, 0)
            elif total_de_vms == 3:
                # Três aplicativos, divididos em três colunas (esquerda, meio, direita)
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, screen_width // 3, screen_height, 0)
                # Similar para outras duas janelas
            elif total_de_vms == 4:
                # Quatro aplicativos, divididos em quadrantes (dois em cima, dois embaixo)
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, screen_width // 2, screen_height // 2, 0)
                # Outras três janelas para completar a disposição em quadrantes
        else:
            print(f"Janela com PID {pid} não encontrada.")

    def contar_vms_por_area_de_trabalho(request):

        vms_por_area = Maquinas_Virtuais.objects.values('area_de_trabalho').annotate(total=Count('id')).order_by('area_de_trabalho')
        resultado = {item['area_de_trabalho']: item['total'] for item in vms_por_area}
        return {"vms_por_area": resultado}   
    
    def abrir_vm_via_mstsc(self, host, usuario, senha, usar_todos_os_monitores, largura=1280, altura=720):
        
        try:

            remover_comando = ['cmdkey', f'/delete:{host}']
            subprocess.run(remover_comando, capture_output=True)

            comando_credenciais = ['cmdkey', f'/generic:{host}', f'/user:{usuario}', f'/pass:{senha}']
            result = subprocess.run(comando_credenciais, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(f"Credenciais adicionadas para {host}.")
            else:
                raise RuntimeError(f"Erro ao adicionar credenciais: {result.stderr}")

            if usar_todos_os_monitores:
                comando = ['mstsc', f'/v:{host}', '/multimon']
            else:
                comando = ['mstsc', f'/v:{host}', f'/w:{largura}', f'/h:{altura}']

            processo = subprocess.Popen(comando)
            process_id = processo.pid

            print(f"Conexão iniciada para {host} com PID: {process_id}")
            return process_id

        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar comando: {e}")
            raise

        except Exception as e:
            print(f"Erro inesperado: {e}")
            raise
        
class Utils:

    def __init__(self) -> None:

        self.token = TELEGRAM_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID

    def enviar_mensagem_telegram(self, message):

        try:

            data = {
                "chat_id": self.chat_id, 
                "text": message
            }
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            requests.post(url, data)

        except Exception as e:

            print("[TELEGRAM][ERRO] Erro ao enviar a mensagem:", e)

if __name__ == '__main__':

    conexao = ConexaoAreaDeTrabalhoRemota()
    # conexao.gerenciar_area_de_trabalho(2)


