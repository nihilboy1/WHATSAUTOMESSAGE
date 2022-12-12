import os.path
import re
from datetime import timedelta
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


def getNumbers(str):
    array = re.findall(r"[0-9]+", str)
    return array


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_SPREADSHEET_ID = "1haVj-tHFwIIEcASGykar6EuOI6tu1OiRvrHynU-afWM"
SAMPLE_RANGE_NAME = "Plan1!A7:C12"
invalidNumbers = []


def start(nav):
    nav.get("https://sistema.oabsoluto.com.br/login.do?action=inicio&relogin=1")
    sleep(0.3)
    a = str(input("SEND ANY KEY TO CONTINUE \n"))


def process(nav, cpf):
    clipboard.copy(cpf)
    cpf_input = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[3]/nav/div[1]/div/input",
            )
        )
    )
    cpf_input.clear()
    cpf_input.send_keys(Keys.CONTROL, "v")
    sleep(1)
    cpf_input.send_keys(Keys.RETURN)
    tel = wdw(nav, 10).until(
        ec.visibility_of_element_located(
            (
                By.CSS_SELECTOR,
                "#aba_link_simular",
            )
        )
    )
    tel.click()
    sleep(50)


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
        try:
            options = webdriver.ChromeOptions()
            options.add_argument(
                r"--user-data-dir=C:/Users/samue/AppData/Local/Google/Chrome/User Data"
            )
            options.add_argument(r"--profile-directory=Profile 1")
            nav = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )
            start(nav)
            new_values = []

            for linha in valores:
                nome = linha[0].title().strip()
                cpf = getNumbers(linha[2])
                cpf = "".join(cpf)
                process(nav, cpf)
                print(nome, cpf)

            else:
                # result = (
                #     sheet.values()
                #     .update(
                #         spreadsheetId=SAMPLE_SPREADSHEET_ID,
                #         range=SAMPLE_RANGE_NAME,
                #         valueInputOption="USER_ENTERED",
                #         body={"values": new_values},
                #     )
                #     .execute()
                # )
                a = 1
        except:
            print("Houve um erro...")


if __name__ == "__main__":
    main()
