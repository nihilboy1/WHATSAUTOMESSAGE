name = str(input("Informe o nome do cliente: ")).capitalize()
margem = float(input("Informe a margem disponivel do cliente: "))

total = (margem * 27.5)
saque = total * 70 / 100
credito = total * 30 / 100
total = str(total).replace(".", ',')
saque = str(saque).replace(".", ",")
credito = str(credito).replace(".", ",")
margem = str(margem).replace(".", ",")

print(f"""
{name}, o valor total liberado é de R${total}! 70% desse valor será creditado direto na sua conta, liberando uma quantia liquida de cerca de R${saque}. Além disso, será enviado um cartão de crédito para o seu endereço cadastrado, com limite de R${credito}. 
O desconto no seu benefício será de apenas R${margem}.


Observações: O cartão benefício não é como um empréstimo consignado comum, que tem data para iniciar e acabar. Como o cartão de crédito fica ativo pelo tempo que você desejar, o desconto de R${margem} também continua todos os meses, com a fatura mensal ficando fixa no valor total contratado, aguardando pagamento. Vale lembrar que a cada três meses um novo saque fica disponível, mas claro, você pode optar por não sacar e efetuar a quitação total do cartão. Realizando o pagamento total do cartão, você pode solicitar o seu cancelamento e exclusão do desconto.
""")
