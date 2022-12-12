export const removeSpecialCharacters = number => {
  const regex = /[^a-zA-Z0-9 ]? ?/g
  return number.replace(regex, '')
}

export const removeOrNotThe9 = number => {
  if (parseInt(number.slice(2, 4)) <= 28) {
    console.log('1', number)
    return number
  }
  const numberWithout9 = `${number.slice(0, 4)}${number.slice(5)}`
  console.log('2', numberWithout9)
  return numberWithout9
}

export const verifyIfHaveBrazilDDD = number => {
  const numberSliced = number.slice(0, 2)
  if (numberSliced === '55') return true

  return false
}

export const getMessage = name => {
  name = name[0].toUpperCase() + name.substring(1)
  return `Olá, *${name}*, tudo bem? Meu nome é *Roberta*, eu sou análista da *Confiance*. \n\nVamos consultar sua margem para empréstimo e cartão para descobrir as propostas disponiveis para você no momento?\n\nEnvie *1* pra a gente realizar a sua simulação sem compromisso 😃.\nEnvie *2* caso não tenha interesse no momento 😶\n\n*Estou a disposição para tirar qualquer dúvida 😉.*`
}
