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
from selenium.webdriver.support.wait import WebDriverWait as wdw
from webdriver_manager.chrome import ChromeDriverManager
from utils import getNumbers, continueProcess, googleAPICredentialsCheck, startProcess
from copys import aumento, generico1, generico2, generico3, fgts

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SAMPLE_SPREADSHEET_ID = "1lDTr455ktYVXiL4wPjQe2LdqduLrToanuYqFf0EBam8"
SAMPLE_RANGE_NAME = "FGTS JEFFERSON!A2:C50"
successSend = []
failSend = []


def main():
    googleAPICredentialsCheck(SCOPES, SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME)
    options = webdriver.ChromeOptions()
    options.add_argument(
        r"--user-data-dir=C:/Users/samue/AppData/Local/Google/Chrome/User Data"
    )
    options.add_argument(r"--profile-directory=Profile 1")
    webDriver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    startProcess(webDriver)

    for linha in valores:  # type: ignore
        nome = linha[0].title().strip().split(" ")
        nome = nome[0]
        telefone = getNumbers(linha[1])
        copy = fgts.strip()
        continueProcess(webDriver, telefone, copy, successSend, failSend)

    else:
        print(
            f"{len(successSend)} mensagens foram enviadas com sucesso, havendo falha em {len(failSend)} "
        )


if __name__ == "__main__":
    main()
