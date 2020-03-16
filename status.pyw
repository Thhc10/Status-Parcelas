import requests
from datetime import datetime
import PySimpleGUI as sg


def delta_dias(data_alvo):
    date_format = "%Y-%m-%d"
    a = datetime.today()
    b = datetime.strptime(data_alvo, date_format)
    delta = (b - a).days
    return delta


def parcelas_pendentes(data):
    vetor = []
    max = len(data["quotaSettlement"])

    parcela = 0
    while parcela < max:

        if not data["quotaSettlement"][parcela]["paid"]:
            cont_paga = False
            for verifica in range(max):
                if data["quotaSettlement"][verifica]["quotaNumber"] == data["quotaSettlement"][parcela]["quotaNumber"] \
                        and data["quotaSettlement"][verifica]["paid"] and verifica != parcela:
                    parcela += 1
                    cont_paga = True
                    break

            if not cont_paga:
                vetor.append(str(data["quotaSettlement"][parcela]["dueDate"]))
                parcela += 1

        else:
            parcela += 1

    return vetor


# Inicio GUI

sg.theme('Dark2')
# Layout
layout = [
    [sg.Text('CCB', size=(5, 0)), sg.Input(size=(15, 0), key='ccb')],
    [sg.Button('Enviar Dados')],
    [sg.Output(size=(88, 20))]
]
# Janela
janela = sg.Window("Parcelas Pendendes - meBanq", layout)


while True:  # Loop
    button, values = janela.Read()
    read_ccb = values['ccb']

    parametros = {"ccbNumber": read_ccb}
    # Inserir link API
    dados = requests.get('link_api1', params=parametros)
    status_api = dados.status_code

    if status_api != 200:  # CCB inválida
        print("Valor inválido!\n")
        continue

    dados_json = dados.json()

    parcelas_atraso = []
    vetor_pendentes = parcelas_pendentes(dados_json)

    for i in range(len(vetor_pendentes)):
        if delta_dias(vetor_pendentes[i]) < 0:
            parcelas_atraso.append(vetor_pendentes[i])

    if not parcelas_atraso:
        print("A empresa com a CCB: " + read_ccb + ", está em dia.")

    else:
        print("A empresa com a CCB: " + read_ccb + ", está com as seguintes parcelas em atraso:")
        print(parcelas_atraso)

    print()
