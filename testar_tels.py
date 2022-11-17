import os.path
from datetime import timedelta
from time import sleep
from playsound import playsound 

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

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_SPREADSHEET_ID = "18YcWIfYXwLgQGr0Lsx5IcZYz_ab3ch-5d3uvsaNSoi0"
SAMPLE_RANGE_NAME = "BASE!B999:B1150"
invalidNumbers = []


def start(nav):
    nav.get("https://web.whatsapp.com/")
    while len(nav.find_elements(By.XPATH, '//*[@id="side"]')) < 1:
        sleep(1)
    sleep(1)
def continueProcess(nav, telefone):
    while len(nav.find_elements(By.ID, "side")) < 1:
        sleep(1)
    sleep(1)

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
    sleep(0.4)
    open_chat_button = wdw(nav, 10).until(
        ec.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div[2]/a[2]"))
    )
    open_chat_button.click()
    sleep(1)

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
            ec.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/div",
                )
            )
        )
        invalidNumbers.append(f"Erro: {telefone}")
        telefone = "Invalid"
        sleep(0.6)
        close_invalid_number_modal.click()
        return telefone

    header = wdw(nav, 10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[1]/div/div/div[4]/div/header",
            )
        )
    )
    sleep(1)
    return telefone

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
            options.add_argument(r"--profile-directory=Profile 4")
            nav = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )
            start(nav)
            new_values = []
            count = len(valores)
            secondsToFinish = round(count * 3.65)
            print("Tempo para conclusão: ", timedelta(seconds=secondsToFinish))

            for linha in valores:
                telefone = linha[0].replace(" ", "").strip()
                telefone = continueProcess(nav, telefone)
                print(
                    f"Restam {count} | Ultimo telefone testado: {telefone}"
                )
                new_values.append([telefone])
                count -= 1
            else:
                result = (
                    sheet.values()
                    .update(
                        spreadsheetId=SAMPLE_SPREADSHEET_ID,
                        range=SAMPLE_RANGE_NAME,
                        valueInputOption="USER_ENTERED",
                        body={"values": new_values},
                    )
                    .execute()
                )
                print(f"{len(invalidNumbers)} numeros inválidos!")
                playsound("D:/Github/WHATSAUTOMESSAGE/bip.mp3")
        except:
            playsound("D:/Github/WHATSAUTOMESSAGE/error.mp3")
if __name__ == "__main__":
    main()
