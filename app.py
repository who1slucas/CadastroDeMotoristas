from flask import Flask, render_template, request
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

# Credenciais e ID da Planilha
SERVICE_ACCOUNT_FILE = './token.json'
SPREADSHEET_ID = '1Dr-8PTKX_xZNJla0b44XADYCITtuG6fhyCtFXGyPocg'

# Configuração da API do Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

@app.route('/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        # Obtendo os dados do formulário
        nome = request.form['nome']
        cnpj_cpf = request.form['cnpj_cpf']
        endereco = request.form['endereco']
        numero = request.form['numero']
        bairro = request.form['bairro']
        complemento = request.form['complemento']
        estado = request.form['estado']
        cidade = request.form['cidade']
        cep = request.form['cep']
        ddd = request.form['ddd']
        telefone = request.form['telefone']
        chave_pix = request.form['chave_pix']

        # Adicionar dados à planilha
        adicionar_dados_a_planilha(nome, cnpj_cpf, endereco, numero, bairro, complemento, estado, cidade, cep, ddd, telefone, chave_pix)

        return "Dados enviados com sucesso!"
    
    return render_template('formulario.html')

def adicionar_dados_a_planilha(nome, cnpj_cpf, endereco, numero, bairro, complemento, estado, cidade, cep, ddd, telefone, chave_pix):
    range_ = 'Base!A2:A'
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=range_).execute()
    values = result.get('values', [])
    proxima_linha = len(values) + 2

    values_pagina_dois = [[nome, cnpj_cpf, endereco, numero, bairro, complemento, estado, cidade, 'Brasil', cep, ddd, telefone, chave_pix]]
    body_pagina_dois = {'values': values_pagina_dois}
    
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"'Base'!A{proxima_linha}",
        valueInputOption='RAW',
        body=body_pagina_dois
    ).execute()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
