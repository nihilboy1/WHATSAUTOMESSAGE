import time
import urllib

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#lê a tabela do xlsx
tabela = pd.read_excel("fakedata.xlsx")

#abre o chrome e acessa o site
nav = webdriver.Chrome()
nav.get("https://web.whatsapp.com/")

#espera pelo elemento da barra lateral ser carregado
while len(nav.find_elements(By.XPATH, '//*[@id="side"]')) <1:
    time.sleep(1)
time.sleep(2)


#roda 1x pra cada linha da tabela
for linha in tabela.index:

  #coleta as informações dos campos
  nome = tabela.loc[linha, "nome"]
  telefone = tabela.loc[linha, "numero"]
  msg = tabela.loc[linha, "msg"]

  #transforma o texto para o formato válido pra url
  texto = msg.replace("fulano", nome)
  texto = urllib.parse.quote(texto)

  # edita o link para envio de mensagem e acessa ele
  link = f"https://web.whatsapp.com/send?phone={telefone}&text={texto}"
  nav.get(link)


  #espera pelo elemento da barra lateral ser carregado
  while len(nav.find_elements(By.ID, 'side')) < 1:
    time.sleep(1)
  time.sleep(2)

  #confere se o elemento de "numero inválido" apareceu na tela
  if len(nav.find_elements(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]' )) < 1:
    # se o elemento de erro não tiver aparecido, ele tenta enviar a mensagem.
    nav.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span' ).click()
    time.sleep(2)
    print(f"O ultimo numero utilizado foi: {telefone}")




