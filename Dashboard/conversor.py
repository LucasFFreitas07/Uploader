import pandas as pd
from datetime import datetime
from pathlib import Path

date = datetime.now()
hoje = date.strftime("%d-%m")

def converter():
    bases = Path("/app/media")
    if not bases.exists():
        bases.mkdir(parents=True)

    try:

        export_im = (bases / f'{hoje}_export.csv')
        export_rf = (bases / f'{hoje}_export (1).csv')

        dados_im = pd.read_csv(export_im, sep=';')
        dados_rf = pd.read_csv(export_rf, sep=';')
        dados = pd.merge(dados_im, dados_rf, how='outer', on=None, validate=None)
        dados['Total'] = dados['ID da Interação'].count()
        dados.rename({'Nível 4': 'Módulo'}, axis='columns', errors='raise')
        dados.rename({'Nível 5': 'Sintoma'}, axis='columns', errors='raise')
        dados['Sintoma'] = dados['Nível 5']
        dados['Módulo'] = dados['Nível 4']
        dados.pop('Nível 4')
        dados.pop('Nível 5')

        SUBSTITUIR = {
            'Cliente Pendente': 'Pausado',
            'Resolved': 'Resolvido',
            'Dispatched': 'Em tratativa',
            'Closed': 'Fechado',
            'Suspended': 'Suspenso',
            'Assign': 'Designado'
        }
        dados['Status'] = dados['Estado'].replace(SUBSTITUIR)
        dados.pop('Estado')

        group = dados.groupby(['Total', 'Status']).size()
        group.to_excel(excel_writer=f"{bases}/Quantidade_Chamados_{hoje}.xlsx")

        dados.pop('Total')
        dados.to_excel(excel_writer=f"{bases}/Base_Geral_{hoje}.xlsx" ,index=False)
        #print('Conversão concluída com sucesso!')

    except FileNotFoundError:
        print('Arquivos não encontrados, favor verificar')

    except Exception as e:
        print(f'Erro: {e}')

if __name__ == '__main__':
    converter()