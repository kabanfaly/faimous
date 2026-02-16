import client from './client'

/**
 * @returns {Promise<Array<{ code: string, symbol: string, name: string }>>}
 */
export function getCurrencies() {
  return client.get('currencies').then((r) => r.data)
}
