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
SAMPLE_SPREADSHEET_ID = "1u5MlHBMgNRyF7HXFC4tHmuh90KrByK1y1hMlRk3jYWA"
SAMPLE_RANGE_NAME = "cetelem_new!A2:C17"
invalidNumbers = []


def start(nav):
    nav.get("https://vendamaisbevi.com.br/acesso/login")
    sleep(0.3)

    entrar = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[1]/div[3]/div[1]/div[2]/div/div[2]/form/div/div[3]/button",
            )
        )
    )
    entrar.click()
    sleep(1)
    nb_ou_cpf = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[1]/div[8]/div/div/div[2]/div/div[2]/div/div[1]/div/a[2]",
            )
        )
    )
    nb_ou_cpf.click()
    sleep(1.5)


def process(nav, cpf):
    clipboard.copy(cpf)
    cpf_input = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[1]/div[8]/div/div/div[2]/div[2]/div/div/div/form/div[2]/p[3]/input",
            )
        )
    )
    cpf_input.clear()
    cpf_input.send_keys(Keys.CONTROL, "v")
    sleep(0.3)
    consultar = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[1]/div[8]/div/div/div[2]/div[2]/div/div/div/form/div[2]/p[4]/button",
            )
        )
    )
    consultar.click()
    sleep(0.3)
    selectnb = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[6]/div/select",
            )
        )
    )
    selectnb.click()
    selectNB_option = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[6]/div/select/option[2]",
            )
        )
    )
    selectNB_option.click()
    ok = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[6]/div/div[6]/button[1]",
            )
        )
    )
    ok.click()
    sleep(1)
    idade = nav.find_element(
        By.XPATH,
        '//*[@id="section_C1beb8f7d20"]/article/div/div/div[1]/div/div[2]/div/span',
    ).get_attribute("innerText")
    sleep(0.1)
    margemlivre = nav.find_element(
        By.XPATH,
        '//*[@id="section_C1beb8f7d20"]/article/div/div/div[1]/div/div[3]/div/span',
    ).get_attribute("innerText")
    sleep(0.1)
    salario = nav.find_element(
        By.XPATH,
        '//*[@id="section_C1beb8f7d20"]/article/div/div/div[1]/div/div[4]/div/span',
    ).get_attribute("innerText")
    sleep(0.1)
    especie = nav.find_element(
        By.XPATH,
        '//*[@id="section_C1beb8f7d20"]/article/div/div/div[1]/div/div[7]/div/span',
    ).get_attribute("innerText")
    sleep(0.1)
    return idade, margemlivre, salario, especie


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
                idade, margemlivre, salario, especie = process(nav, cpf)
                print(nome, cpf, margemlivre, salario, especie, idade)

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
