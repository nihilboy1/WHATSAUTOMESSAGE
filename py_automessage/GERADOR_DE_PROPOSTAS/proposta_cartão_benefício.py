coef = 25
margem = str(input("Informe a margem que será utilizada: ")).replace(",", ".")
banco = str(input("Informe o banco: ")).strip().upper()


if len(margem) > 6:
    print("O valor máximo para calculo é de até 999,99")
else:
    margem = float(margem)
print("\n")
print("////////////////////////////")

valor_total = margem * coef
valor_saque = valor_total * 70 / 100
valor_credito = valor_total * 30 / 100

valor_total = f"{valor_total:.2f}".replace(".", ",")
valor_saque = f"{valor_saque:.2f}".replace(".", ",")
valor_credito = f"{valor_credito:.2f}".replace(".", ",")
margem = f"{margem:.2f}".replace(".", ",")


proposta1 = f"""O valor total disponível para o cartão é de R${valor_total}, onde 70% desse valor será creditado direto na sua conta, liberando uma quantia liquida de cerca de R${valor_saque}. Além disso, será enviado um cartão de crédito para o seu endereço cadastrado, com limite de R${valor_credito}. O desconto no seu benefício será de apenas R${margem}

É importante ressaltar que o cartão benefício não é como um empréstimo consignado comum, que tem data para iniciar e acabar. Como o cartão de crédito fica ativo pelo tempo que você desejar, o desconto de R${margem} também continua todos os meses. Contudo, você pode realizar a quitação ou amortização dessas parcelas a qualquer momento para diminuir o tempo de desconto!"""


proposta2 = f"""Segue a simulação da nossa Proposta:

*Banco {banco}:*
O valor total de limite em seu cartão será de *R${valor_total}*, onde 70% desse valor será creditado direto na sua conta, liberando uma quantia liquida de cerca de *R${valor_saque}*.

O cartão de crédito será enviado para o seu endereço cadastrado, com limite de *R${valor_credito}*. O desconto no seu benefício será de apenas *R${margem}*, até que seja quitado o valor do saque efetuado de *R${valor_saque}*.

*OBSERVAÇÕES:*
✅ ZERO de anuidade
✅ Descontos em farmácias
✅ Válido em qualquer estabelecimento
✅ Valor de saque disponível em até 24 horas
✅ Pagamento mínimo da fatura direto na folha

----------------------------------------------------------
*CONFIANCE - MAIS CRÉDITO PARA VOCÊ!*
----------------------------------------------------------
*Nosso CNPJ para a sua segurança: 48.248.145/0001-32*

*É importante ressaltar que o cartão benefício não é como um empréstimo consignado comum, que tem data para iniciar e acabar. Como o cartão de crédito fica ativo pelo tempo que você desejar, o desconto de R${margem} também continua todos os meses, até um prazo máximo de 84x. Contudo, você pode realizar a quitação ou amortização dessas parcelas a qualquer momento para encerrar o desconto!*
"""


print(proposta2)
