export const removeSpecialCharacters = number => {
  const regex = /[^a-zA-Z0-9 ]? ?/g
  return number.replace(regex, '')
}

export const removeOrNotThe9 = number => {
  if (parseInt(number.slice(2, 4)) <= 28) {
    console.log('', number)
    return number
  }
  const numberWithout9 = `${number.slice(0, 4)}${number.slice(5)}`
  console.log('"9" retirado: ', numberWithout9)
  return numberWithout9
}

export const verifyIfHaveBrazilDDD = number => {
  const numberSliced = number.slice(0, 2)
  if (numberSliced === '55') return true

  return false
}

export const getMessage = name => {
  const myArray = name.split(' ')
  name = myArray[0]
  const nameCap = name[0].toUpperCase() + name.substring(1)

  return `Bom dia, *${nameCap}*, tudo bem? Meu nome é *Roberta*, eu sou análista de crédito da *Confiance*. \n\nQue tal consultar sua margem para empréstimo e cartão e descobrir as propostas disponiveis para você no momento?\n\nEnvie *1* pra a gente realizar a sua simulação sem compromisso 😃.\nEnvie *2* caso não tenha interesse no momento 😶\n\n*Estou a disposição para tirar qualquer dúvida 😉.*`
}
