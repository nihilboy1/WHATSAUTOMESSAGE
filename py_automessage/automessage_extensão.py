import os.path
import urllib
from random import randint
from time import sleep

import clipboard
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wdw
from webdriver_manager.chrome import ChromeDriverManager

from mensagens_disparo import generico1, generico2, generico3

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SAMPLE_SPREADSHEET_ID = "1haVj-tHFwIIEcASGykar6EuOI6tu1OiRvrHynU-afWM"
SAMPLE_RANGE_NAME = "Plan1!A128:D166"
successSend = []
failSend = []


def start(nav):
    nav.get("https://web.whatsapp.com/")
    while len(nav.find_elements(By.XPATH, '//*[@id="side"]')) < 1:
        sleep(1)
    sleep(1)


def continueProcess(nav, telefone, texto):
    while len(nav.find_elements(By.ID, "side")) < 1:
        sleep(1)
    sleep(randint(1, 3))

    start_new_conversation_button = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (By.XPATH, '//*[@id="startNonContactChat"]/div/span')
        )
    )
    start_new_conversation_button.click()

    input_number_area = wdw(nav, 10).until(
        ec.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div[1]/div/input"))
    )
    input_number_area.clear()
    input_number_area.send_keys(telefone)
    open_chat_button = wdw(nav, 10).until(
        ec.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div[2]/a[2]"))
    )
    open_chat_button.click()
    sleep(randint(1, 5))

    while not (
        len(
            nav.find_elements(
                By.XPATH,
                "/html/body/div[1]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/div",
            )
        )
        < 1
    ):
        close_invalid_number_modal = wdw(nav, 10).until(
            ec.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/div",
                )
            )
        )
        failSend.append(f"Erro: {telefone}")
        close_invalid_number_modal.click()
        return
    sleep(randint(1, 3))
    conversation_text_box = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p",
            )
        )
    )
    clipboard.copy(texto)
    conversation_text_box.clear()
    conversation_text_box.click()
    conversation_text_box.clear()
    conversation_text_box.send_keys(Keys.CONTROL, "v")
    sleep(randint(1, 5))
    send_message_button = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span",
            )
        )
    )
    send_message_button.click()
    successSend.append(f"Ok: {telefone}")
    sleep(randint(5, 10))


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

        options = webdriver.ChromeOptions()
        options.add_argument(
            r"--user-data-dir=C:/Users/samue/AppData/Local/Google/Chrome/User Data"
        )
        options.add_argument(r"--profile-directory=Profile 1")
        nav = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        start(nav)

        for linha in valores:
            if linha[3] == "*":
                sleep(randint(1, 2))
                nome = linha[0].title().strip().split(" ")
                nome = nome[0]
                telefone = linha[1].replace(" ", "").strip()
                atendente = "Roberta"
                randomMessage = randint(1, 3)
                if randomMessage == 1:
                    texto = generico1.strip()
                elif randomMessage == 2:
                    texto = generico2.strip()
                elif randomMessage == 3:
                    texto = generico3.strip()
                texto = texto.replace("CLIENTE", nome)
                texto = texto.replace("ATENDENTE", atendente)
                print(nome, telefone)
                continueProcess(nav, telefone, texto)
            else:
                print(linha)
        else:
            print(
                f"{len(successSend)} mensagens foram enviadas com sucesso, havendo falha em {len(failSend)} "
            )


if __name__ == "__main__":
    main()
