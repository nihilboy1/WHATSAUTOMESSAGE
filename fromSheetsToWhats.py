
import os.path
import time
import urllib

import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SAMPLE_SPREADSHEET_ID = '1H6GUuOZ4jaSdwxj7AkKW5OPOetSTM2FCibxLs9dW01o'
SAMPLE_RANGE_NAME = 'AUTOMESSAGE_LIST!A100:B152'

message = """ Bom dia, fulano! Meu nome é Roberta e eu sou Analista de Crédito da empresa Confiance, tudo bem contigo?
O motivo do meu contato é a recente liberação da nova margem de +5% para cartão consignado, da qual você pode ser um dos beneficiários...
Esse produto tem diversas vantagens sobre os demais cartões e, além disso, o valor já entra na sua conta em até 12 horas!

Escolha uma das opções abaixo:
1 - Simular para descobrir os valores disponíveis
2 - Mais informações
3 - Não tenho interesse  
"""
successSend =[]
failSend = []

def main():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        valores = result["values"]
    except HttpError as err:
        print(err)
    finally:
        # nav = webdriver.Chrome()
        # nav.get("https://web.whatsapp.com/")

        # while len(nav.find_elements(By.XPATH, '//*[@id="side"]')) <1:
        #     time.sleep(1)
        # time.sleep(1.5)

        for linha in valores:
            nome = linha[0].title().strip()
            texto = message
            telefone = linha[1].replace(" ", "")
            if len(telefone) != 13:
                print("Quantidade de numeros inválida no telefone abaixo:")
            
            texto = texto.replace("fulano", nome.capitalize().strip())
            texto = urllib.parse.quote(texto)
            print(nome, telefone)

        #     link = f"https://web.whatsapp.com/send?phone={telefone}&text={texto}"
        #     nav.get(link)

        #     while len(nav.find_elements(By.ID, 'side')) < 1:
        #         time.sleep(1)
        #     time.sleep(1.5)

        #     if len(nav.find_elements(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]' )) < 1:
        #         nav.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span' ).click()
        #         time.sleep(1.5)
        #         successSend.append(f"Esse numero foi encontrado e enviou a mensagem: {telefone}")
        #         print(f"Esse numero foi encontrado e enviou a mensagem: {telefone}")
        #     else:
        #         failSend.append(f"Esse numero NÃO foi encontrado e NÃO enviou a mensagem: {telefone}")
        #         print(f"Esse numero NÃO foi encontrado e NÃO enviou a mensagem: {telefone}")
        # else:
        #     print(f"Foi enviado um total de {len(successSend)} mensagens, enquanto houve falha em {len(failSend)} ")

                



if __name__ == '__main__':
    main()
