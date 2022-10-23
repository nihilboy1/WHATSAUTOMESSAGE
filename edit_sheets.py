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

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SAMPLE_SPREADSHEET_ID = "1H6GUuOZ4jaSdwxj7AkKW5OPOetSTM2FCibxLs9dW01o"
SAMPLE_RANGE_NAME = "LOAS_E_BPC!A2:B140"


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
        new_values = []

        for linha in valores:
            nome = linha[0].title().strip().split(" ")
            nome = nome[0]
            telefone = linha[1].replace(" ", "").strip()

            # cpf = linha[2]
            # while len(cpf) < 11:
            #     cpf = "0" + cpf
            # if not "." or "-" in cpf:
            #     cpf = cpf.replace(".", "")
            #     cpf = cpf.replace("-", "")
            #     cpf = f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
            new_values.append([nome, telefone])

        # result = (
        #     sheet.values()
        #     .update(
        #         spreadsheetId=SAMPLE_SPREADSHEET_ID,
        #         range="LOAS_E_BPC_CARTÃO!A2",
        #         valueInputOption="USER_ENTERED",
        #         body={"values": new_values},
        #     )
        #     .execute()
        # )

    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()


"""Não tem o 55 e nem o 9"""
# telefone = f"55{telefone[0:2]}9{telefone[2:]}".strip()


"""Do 55 pra frente """
# telefone = f"{telefone[2:]}".strip()

"""Retirar um 9 errado após o 55"""
# telefone = f"{telefone[0:2]}" + f"{telefone[3:]}"
