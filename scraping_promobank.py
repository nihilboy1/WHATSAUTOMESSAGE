import os.path
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
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wdw
from webdriver_manager.chrome import ChromeDriverManager

from variaveis import companyCode, login, senha

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SAMPLE_SPREADSHEET_ID = "1yZKE3jhvbVEx934rD8QehEnlz2g7t1uKZWEq628VwO0"
SAMPLE_RANGE_NAME = "PROMOSCRAPING!A2:F13"


def start(nav):
    nav.get("https://www.promobank.com.br/")
    nav.maximize_window()

    while (
        len(nav.find_elements(By.XPATH, "/html/body/div[3]/div[2]/div[1]/div/span[2]"))
        < 1
    ):
        print("Aguardando...")
        sleep(4)

    search_button = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[3]/div[2]/div[1]/div/span[2]",
            )
        )
    )
    search_button.click()
    sleep(1)
    phones = nav.find_element(By.XPATH, '//*[@id="consultaTab"]/li[4]')
    sleep(3)
    phones.click()


def process(nav, cpf):
    phones_input = wdw(nav, 18).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="tab_buscamais"]/div[1]/div/div[1]/div/div/form/div/div[1]/input',
            )
        )
    )
    phones_input.click()
    phones_input.send_keys(cpf)
    sleep(20)


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
        nav = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        start(nav)

        for linha in valores:
            print(linha)
            cpf = linha[0].strip()
            print(cpf)

            process(nav, cpf)


if __name__ == "__main__":
    main()
