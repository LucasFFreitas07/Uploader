def main():
    import os
    try:
        port = 5000
        print(f'Executando aplicação na porta {port}')
        os.system(f'python -m streamlit run dashboard.py --server.port {port}')

    except KeyboardInterrupt:
        print("Aplicação desligada pelo administrador")

    except ValueError:
        print('Valor inserido não é um número')

    except Exception as e:
        print(f"Erro: {e}")
        print("Contate o administrador")


if __name__ == '__main__':
    main()

