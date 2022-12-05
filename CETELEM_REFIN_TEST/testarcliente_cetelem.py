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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wdw
from webdriver_manager.chrome import ChromeDriverManager

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_SPREADSHEET_ID = "1u5MlHBMgNRyF7HXFC4tHmuh90KrByK1y1hMlRk3jYWA"
SAMPLE_RANGE_NAME = "cetelem_new!A6:C9"
invalidNumbers = []


def getNumbers(str):
    array = re.findall(r"[0-9]+", str)
    return array


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
    try:
        wdw(nav, 3).until(
            ec.alert_is_present(),
            "Timed out waiting for PA creation " + "confirmation popup to appear.",
        )

        alert = nav.switch_to.alert
        alert.accept()
        print("alert accepted")
    except Exception:
        print("no alert")
    cadastro_button = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (By.XPATH, '//*[@id="navbar-collapse-funcao"]/ul/li[1]/a')
        )
    )
    actions = ActionChains(nav)
    actions.move_to_element(cadastro_button).perform()
    sleep(0.3)
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
    sleep(1)
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
    sleep(1)


def process(nav, cpf):
    nav.refresh()
    clipboard.copy("171795")
    operador = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="ctl00_Cph_UcR_jn_jOC_UcOrg_txtOrg3O_CAMPO"]',
            )
        )
    )
    operador.send_keys(Keys.CONTROL, "v")
    area = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="ctl00_Cph_Upd"]',
            )
        )
    )
    area.click()
    sleep(2)
    cpf_cliente = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="ctl00_Cph_UcR_jn_jCl_UcCl_txtCpf_CAMPO"]',
            )
        )
    )
    clipboard.copy(cpf)
    sleep(2)
    cpf_cliente.send_keys(Keys.CONTROL, "v")
    sleep(1)
    area = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="ctl00_Cph_Upd"]',
            )
        )
    )
    area.click()
    try:
        sleep(1)
        listar_contratos = wdw(nav, 3).until(
            ec.element_to_be_clickable((By.XPATH('//*[@id="btnLstCtt_txt"]'),))
        )
        return
    except Exception:
        sleep(1.5)
        actions = ActionChains(nav)
        actions.send_keys(Keys.RETURN)
        actions.perform()
        sleep(2)
        nascimento = (
            wdw(nav, 5).until(
                ec.element_to_be_clickable(
                    (By.XPATH('//*[@id="ctl00_Cph_UcR_jn_jCl_UcCl_txtDtNasc_CAMPO"]'),)
                )
            )
        ).get_attribute("value")
        print(nascimento)
        benef = (
            wdw(nav, 5).until(
                ec.element_to_be_clickable(
                    (By.XPATH('//*[@id="ctl00_Cph_UcR_jn_jCl_UcCl_txtCodBnf_CAMPO"]'),)
                )
            )
        ).get_attribute("value")
        print(benef)
        actions.send_keys(Keys.PAGE_DOWN)
        actions.perform()
        listar_contratos = wdw(nav, 5).until(
            ec.element_to_be_clickable((By.XPATH('//*[@id="btnLstCtt_txt"]'),))
        )
        listar_contratos.click()


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
        except Exception as error:
            print(error)


if __name__ == "__main__":
    main()
