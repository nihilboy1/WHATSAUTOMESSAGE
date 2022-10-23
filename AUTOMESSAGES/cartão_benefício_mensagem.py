coef = 25
dot_list = 0


name = str(input("Informe o nome do cliente: ")).title().strip()
margem = str(input("Informe a margem que será utilizada: ")).replace(",", ".")
if len(margem) > 6:
  print("O valor máximo para calculo é de até 999,99")
else:
  margem = float(margem)
  print(margem)

valor_total = (margem * coef)
valor_saque = valor_total * 70 / 100
valor_credito = valor_total * 30 / 100


print(f"""{name}, o valor total disponível para o cartão é de R${valor_total:.2f}, onde 70% desse valor será creditado direto na sua conta, liberando uma quantia liquida de cerca de R${valor_saque:.2f}. Além disso, será enviado um cartão de crédito para o seu endereço cadastrado, com limite de R${valor_credito:.2f}. O desconto no seu benefício será de apenas R${margem:.2f}


Observações: O cartão benefício não é como um empréstimo consignado comum, que tem data para iniciar e acabar. Como o cartão de crédito fica ativo pelo tempo que você desejar, o desconto de R${margem:.2f} também continua todos os meses, com a fatura mensal permanecendo fixa no valor total contratado, que pode ser quitado por você a qualquer momento. Vale lembrar que a cada três meses um novo saque fica a sua disposição, mas claro, você pode optar por não sacar e efetuar a quitação total do cartão. Realizando o pagamento total do débito, você pode solicitar a exclusão do desconto.""")
