import gspread
import requests
import pandas as pd
from pathlib import Path
from oauth2client.service_account import ServiceAccountCredentials

SHEETS_API_CREDENTIALS_PATH = Path(
    Path.cwd(), "backend", "gerenciador_vm", "credentials", "bwabotplatform-a273c9585368.json"
)
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
SHEETS_API_AUTHORIZATION = ServiceAccountCredentials.from_json_keyfile_name(
    SHEETS_API_CREDENTIALS_PATH,
    SCOPE,
)

def get_worksheet_data(
    workbook_key: str,
    worksheet_title: str,
    has_header: bool = True,
    row_header: int = 0,
) -> pd.DataFrame:
    worksheet = (
        gspread.authorize(SHEETS_API_AUTHORIZATION)
        .open_by_key(workbook_key)
        .worksheet(worksheet_title)
    )
    raw_data = worksheet.get_all_values()
    header = raw_data.pop(row_header) if has_header else None
    return pd.DataFrame(raw_data, columns=header)

def adicionar_vm(dados_vm):
    url = 'http://127.0.0.1:8000/api/adicionar_vm/'
    response = requests.post(url, json=dados_vm)
    if response.status_code == 201:  # Verifica se a criação foi bem-sucedida
        print(f"VM adicionada com sucesso: {dados_vm['endereco_computador']}")
    else:
        print(f"Erro ao adicionar VM: {response.status_code} - {response.text}")

if __name__ == "__main__":

    planilha_vms = get_worksheet_data('1FqDy2CYzuEV0pslz0l4Z6CAacTW0w8p29GXvsDaGdj8', 'Robôs Diários')

    df_filtrado = pd.DataFrame(
        columns = [
            'endereco_computador',
            'nome_de_usuario', 
            'senha', 
            'resolucao', 
            'usar_todos_os_monitores', 
            'area_de_transferencia', 
            'area_de_trabalho'
        ]
    )

    for index, linha in planilha_vms.iterrows():

        dados_vm = {
            'endereco_computador': linha['IP'],
            'nome_de_usuario': linha['USUÁRIO'],
            'senha': linha['SENHA'],
            'resolucao': linha['Resolução'].replace(' ', ''),
            'usar_todos_os_monitores': False,
            'area_de_transferencia': True,
            'area_de_trabalho': linha['5']
        }

        adicionar_vm(dados_vm)