import os.path
from datetime import timedelta
from time import sleep

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wdw
from webdriver_manager.chrome import ChromeDriverManager

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_SPREADSHEET_ID = "1x3dWpvyQ2A2Cpf2QLcSj_yU1dgxCzEvbToh4R0WpFK0"
SAMPLE_RANGE_NAME = "contacts!B2:B57"
invalidNumbers = []


def start(nav):
    nav.get("https://autorizador.cetelem.com.br/Login")
    sleep(1)

    token_validate = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (By.XPATH, "/html/body/div[1]/div[1]/form/div[3]/table[2]/tbody/tr/td[8]/a")
        )
    )
    token_validate.click()
    enter_button = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (By.XPATH, "/html/body/form/div[3]/table[2]/tbody/tr/td[16]/a")
        )
    )
    enter_button.click()
    sleep(1.5)
    Alert(nav).accept()

    cadastro_button = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (By.XPATH, '//*[@id="navbar-collapse-funcao"]/ul/li[1]/a')
        )
    )
    cadastro_button.click()
    sleep(0.3)
    cadastro_button.click()
    refin_cp_button = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (By.XPATH, "/html/body/div[3]/nav/div/ul/li[1]/ul/li[2]/a")
        )
    )
    refin_cp_button.click()
    products_button = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/form/div[3]/table/tbody/tr/td/div[1]/table/tbody/tr[2]/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[2]/select",
            )
        )
    )
    products_button.click()
    object_refin = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/form/div[3]/table/tbody/tr/td/div[1]/table/tbody/tr[2]/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[2]/select/option[4]",
            )
        )
    )
    object_refin.click()
    sleep(0.3)
    continuar = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/form/div[3]/table/tbody/tr/td/div[1]/table/tbody/tr[2]/td/div/table/tbody/tr[5]/td/table/tbody/tr/td[1]/span/div[1]/div[2]/div[2]/table/tbody/tr/td/a",
            )
        )
    )
    continuar.click()
    sleep(10)


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
            count = len(valores)
            absoluteCount = len(valores)
            secondsToFinish = round(count * 3.65)
            print("Tempo para conclusão: ", timedelta(seconds=secondsToFinish))

            for linha in valores:
                count -= 1
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
                failPerc = (len(invalidNumbers) / absoluteCount) * 100
                success = absoluteCount - len(invalidNumbers)
                fails = len(invalidNumbers)
                print(
                    f"{fails} Numeros inválidos! | {success} Numeros corretos | {failPerc:.2f}% de falha"
                )
        except:
            print("Houve um erro...")


if __name__ == "__main__":
    main()
