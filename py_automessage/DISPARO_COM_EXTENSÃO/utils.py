import os
from random import randint
import re
from time import sleep
from typing import List

from selenium.webdriver.support.wait import WebDriverWait as wdw
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from google.auth.transport.requests import Request
from selenium.webdriver.remote.webdriver import WebDriver

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import clipboard


def getNumbers(string: str) -> str:
    numeros = re.findall(r"\d+", string)
    return "".join(numeros)


def format_cpf(cpf: str) -> str:
    cpf = cpf.zfill(11)
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def startProcess(webDriver: WebDriver) -> None:
    webDriver.get("https://web.whatsapp.com/")
    while len(webDriver.find_elements(By.XPATH, '//*[@id="side"]')) < 1:
        sleep(1)
    sleep(1)


def continueProcess(
    webDriver: WebDriver,
    phoneNumber: str,
    copy: str,
    successSend: List[str],
    failSend: List[str],
):
    while len(webDriver.find_elements(By.ID, "side")) < 1:
        sleep(1)
    sleep(randint(1, 3))

    start_new_conversation_button = wdw(webDriver, 10).until(
        ec.element_to_be_clickable(
            (By.XPATH, '//*[@id="startNonContactChat"]/div/span')
        )
    )
    start_new_conversation_button.click()

    input_number_area = wdw(webDriver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div[1]/div/input"))
    )
    input_number_area.clear()
    input_number_area.send_keys(phoneNumber)
    open_chat_button = wdw(webDriver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div[2]/a[2]"))
    )
    open_chat_button.click()
    sleep(randint(1, 5))

    while not (
        len(
            webDriver.find_elements(
                By.XPATH,
                "/html/body/div[1]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/div",
            )
        )
        < 1
    ):
        close_invalid_number_modal = wdw(webDriver, 10).until(
            ec.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/div",
                )
            )
        )
        failSend.append(f"Erro: {phoneNumber}")
        close_invalid_number_modal.click()
        return
    sleep(randint(1, 3))
    conversation_text_box = wdw(webDriver, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p",
            )
        )
    )
    clipboard.copy(copy)
    conversation_text_box.clear()
    conversation_text_box.click()
    conversation_text_box.clear()
    conversation_text_box.send_keys(Keys.CONTROL, "v")
    sleep(randint(1, 5))
    send_message_button = wdw(webDriver, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span",
            )
        )
    )
    send_message_button.click()
    successSend.append(f"Ok: {phoneNumber}")
    sleep(randint(5, 10))


def googleAPICredentialsCheck(SCOPES, SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME):
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
        return
