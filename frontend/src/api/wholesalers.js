import client from './client'

export function getWholesalers() {
  return client.get('wholesalers').then((r) => r.data)
}

export function createWholesaler(data) {
  return client.post('wholesalers', data).then((r) => r.data)
}

export function updateWholesaler(wholesalerId, data) {
  return client.patch(`wholesalers/${wholesalerId}`, data).then((r) => r.data)
}

export function deleteWholesaler(wholesalerId) {
  return client.delete(`wholesalers/${wholesalerId}`)
}
