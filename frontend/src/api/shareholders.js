import client from './client'

export function getShareholders() {
  return client.get('shareholders').then((r) => r.data)
}

export function createShareholder(data) {
  return client.post('shareholders', data).then((r) => r.data)
}

export function updateShareholder(shareholderId, data) {
  return client.patch(`shareholders/${shareholderId}`, data).then((r) => r.data)
}

export function deleteShareholder(shareholderId) {
  return client.delete(`shareholders/${shareholderId}`)
}
