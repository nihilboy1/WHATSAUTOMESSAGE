import os.path
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SAMPLE_SPREADSHEET_ID = "1lDTr455ktYVXiL4wPjQe2LdqduLrToanuYqFf0EBam8"
SAMPLE_RANGE_NAME = "FGTS JEFFERSON!A2:C101"


def getNumbers(string: str) -> str:
    numeros = re.findall(r"\d+", string)
    return "".join(numeros)


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
            nome = linha[0].title().strip()
            telefone = getNumbers(linha[1])
            cpf = getNumbers(linha[2])

            if len(cpf) < 11:
                cpf = "0" + cpf
            cpf = f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
            new_values.append([nome, telefone, cpf])
            print(nome, telefone, cpf)

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


"""
            nome = linha[0].title().strip()
            telefone = linha[1].replace(" ", "").replace("-", "").strip()
            cpf = linha[2].strip().replace(" ", "")
            if len(cpf) < 11:
                cpf = "0" + cpf
            cpf = cpf.replace(".", "")
            cpf = cpf.replace("-", "")
            cpf = f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
            new_values.append([nome, telefone, cpf])
            print(nome, telefone, cpf)

"""

# LIMPAR TELEFONES
"""
phone = linha[0]
            if phone != "*":
                if len(phone) > 11:
                    print(f"Maior que 11: {phone} ")
                    phone = "*"
                elif len(phone) < 11:
                    print(f"Menor que 11: {phone} ")
                    phone = "*"
                elif phone[2] != "9":
                    print(f"Sem o 9: {phone} ")
                    phone = "*"
                elif int(phone[3]) < 6:
                    print(f"Fixo: {phone} ")
                    phone = "*"


            
            

            if len(telefone) > 10:
                if telefone[2] != "9":
                    telefone = "-"

            if len(telefone) < 10:
                   telefone = f"-"
            
            new_values.append([phone])

"""
