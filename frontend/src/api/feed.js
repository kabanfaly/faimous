import client from './client'

export function getPreparations() {
  return client.get('feed/preparations').then((r) => r.data)
}

export function createPreparation(data) {
  return client.post('feed/preparations', data).then((r) => r.data)
}

export function updatePreparation(id, data) {
  return client.patch(`feed/preparations/${id}`, data).then((r) => r.data)
}

export function deletePreparation(id) {
  return client.delete(`feed/preparations/${id}`)
}
