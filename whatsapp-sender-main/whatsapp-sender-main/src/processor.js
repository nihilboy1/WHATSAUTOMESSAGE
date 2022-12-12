import { Transform } from 'node:stream'
import {
  removeOrNotThe9,
  removeSpecialCharacters,
  verifyIfHaveBrazilDDD
} from './utils.js'

const FIVE_SECONDS = 5000

export const dataProcessor = Transform({
  objectMode: true,
  transform(chunk, enc, callback) {
    let { phone, name } = JSON.parse(chunk.toString())
    const phoneWithOutSpecialCharacters = removeSpecialCharacters(phone)
    phone = removeOrNotThe9(phone)

    if (!verifyIfHaveBrazilDDD(phoneWithOutSpecialCharacters))
      return callback(null, JSON.stringfy({ name, phone: '55' + phone }))

    return callback(null, JSON.stringify({ name, phone }))
  }
})

export class Throttle extends Transform {
  #requestsPerSecond = 0
  #internalCounter = 0

  constructor({ objectMode, requestsPerSecond }) {
    super({ objectMode })
    this.#requestsPerSecond = requestsPerSecond
  }

  _transform(chunk, enc, callback) {
    this.#internalCounter++

    if (!(this.#internalCounter >= this.#requestsPerSecond)) {
      this.push(chunk)
      return callback()
    }

    setTimeout(() => {
      this.#internalCounter = 0
      this.push(chunk)
      return callback()
    }, FIVE_SECONDS)
  }
}
