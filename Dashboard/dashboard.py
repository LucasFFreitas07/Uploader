import streamlit as st
import pandas as pd
from conversor import converter
import pyarrow as pa
from pathlib import Path

def main():
    bases = Path('/app/media')
    st.title("Análise Diária")
    st.divider()
    st.write(bases)
    with st.sidebar:
        with st.expander("Conversor"):
            conversor = st.button("Converter planilhas")
            if conversor:
                converter()
                st.toast("Conversão completa", icon=':material/check:')
        data = st.date_input("Análise de qual dia?")
        hoje = data.strftime("%d-%m")
        filtros = st.selectbox('Filtro', ['Todos', 'Aplicação ou Serviço de TI', 'Status', 'Chamado'], placeholder="Filtro")
        if filtros == 'Aplicação ou Serviço de TI':
            filter_system = st.text_input("Filtro de Aplicação", placeholder='Ex.: SIES/SAP')
            filter_system = filter_system.upper()

        elif filtros == 'Status':
            STATUS = ['Todos', 'Resolvido', 'Pausado', 'Em tratativa', 'Fechado', 'Suspenso', 'Designado']
            filter_status = st.selectbox('Filtro de Status', options=STATUS, placeholder="Filtro")

        elif filtros == 'Chamado':
            filter_num = st.text_input("Filtro de Chamado", placeholder="Ex.: SD0000001")

    def load_base() -> None:
        dados = f'{bases}/Base_Geral_{hoje}.xlsx'
        df = pd.read_excel(dados)
        st.metric('Total de Chamados', df.sum(axis=1, skipna=False,min_count=0).size)

        try:
            filter_base = df.copy()

            match filtros:
                case 'Todos':
                    table = pa.Table.from_pandas(filter_base)
                    st.dataframe(table, hide_index=True)

                case 'Aplicação ou Serviço de TI':
                    df_filtrado = filter_base[filter_base['Aplicação ou Serviço de TI'] == filter_system]
                    table_filtrado = pa.Table.from_pandas(df_filtrado)
                    st.dataframe(table_filtrado, hide_index=True)

                case 'Todos':
                    df_filtrado = filter_base[filter_base['Todos'] == filter_system]
                    table_filtrado = pa.Table.from_pandas(df_filtrado)
                    st.dataframe(table_filtrado, hide_index=True)

                case 'Status':
                    df_filtrado = filter_base[filter_base['Status'] == filter_status]
                    table_filtrado = pa.Table.from_pandas(df_filtrado)
                    st.dataframe(table_filtrado, hide_index=True)

                case 'Chamado':
                    df_filtrado = filter_base[filter_base['ID da Interação'] == filter_num]
                    table_filtrado = pa.Table.from_pandas(df_filtrado)
                    st.dataframe(table_filtrado, hide_index=True)

        except NameError:
             st.warning('Erro para carregar a base', icon=':material/warning:')
        except Exception as e:
            st.error(f'Erro: {e}')

    def load_nums() -> None:
        dados = f"{bases}/Quantidade_Chamados_{hoje}.xlsx"
        df = pd.read_excel(dados)

        try:
            table = pa.Table.from_pandas(df)
            st.dataframe(table, hide_index=True)

        except FileNotFoundError:
            st.error('Arquivo não encontrado', icon=':material/error:')

    OPCOES = ['Total de Chamados', 'Base']
    choice = st.selectbox('Qual base analisar?', options=OPCOES)

    match choice:
        case 'Total de Chamados':
            load_nums()
        case 'Base':
            load_base()

    st.divider()

if __name__ == '__main__':
    main()