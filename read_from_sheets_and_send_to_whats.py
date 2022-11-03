import os.path
import time
import urllib
from tkinter import X

import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec

from texts import saque_complementar

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SAMPLE_SPREADSHEET_ID = "1QvAcypOFnuagAVPV9IsVmBChw1fQiKaAyfavDChf5k0"
SAMPLE_RANGE_NAME = "saque_filtered!A122:D254"
# D2725
successSend = []
failSend = []


def openWhats(nav):
    nav.get("https://web.whatsapp.com/")

    while len(nav.find_elements(By.XPATH, '//*[@id="side"]')) < 1:
        time.sleep(2)
    time.sleep(2)

def continueProcess(nav, telefone, texto):
    link = f"https://web.whatsapp.com/send?phone={telefone}&text={texto}"
    nav.get(link)
    while len(nav.find_elements(By.ID, "side")) < 1:
        time.sleep(2.2)
    time.sleep(2)

    if (
        len(
            nav.find_elements(
                By.XPATH,
                '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]',
            )
        )
        < 1
    ):
        nav.find_element(
            By.XPATH,
            '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span',
        ).click()
        time.sleep(2)

        successSend.append(f"OK: {telefone}")
        print(f"OK: {telefone}")
    else:
        failSend.append(f"Erro: {telefone}")
        print(f"Erro: {telefone}")


def main():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            .execute()
        )
        valores = result["values"]
    except HttpError as err:
        print(err)
    finally:
        # nav = webdriver.Chrome()
        # openWhats(nav)

        for linha in valores:
            if linha[3] == "*":
                nome = linha[0].title().strip().split(" ")
                nome = nome[0]
                valor_saque = linha[2]

                telefone = linha[1].replace(" ", "").strip()
                atendente = "Roberta"
                texto = saque_complementar
                texto = texto.replace("FULANO", nome)
                texto = texto.replace("ATENDENTE", atendente)
                texto = texto.replace("VALOR_PROPOSTA", valor_saque)
                texto = urllib.parse.quote(texto)
                print(nome, telefone, valor_saque)
                # continueProcess(nav, telefone, texto)
            else:
                print(linha)
        else:
            print(
                f"{len(successSend)} mensagens foram enviadas com sucesso, havendo falha em {len(failSend)} "
            )
            for i in failSend:
                print(i)


if __name__ == "__main__":
    main()
