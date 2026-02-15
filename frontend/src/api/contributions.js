import client from './client'

export function getShareholders() {
  return client.get('contributions/shareholders').then((r) => r.data)
}

export function createShareholder(data) {
  return client.post('contributions/shareholders', data).then((r) => r.data)
}

export function updateShareholder(id, data) {
  return client.patch(`contributions/shareholders/${id}`, data).then((r) => r.data)
}

export function deleteShareholder(id) {
  return client.delete(`contributions/shareholders/${id}`)
}

export function getContributions() {
  return client.get('contributions').then((r) => r.data)
}

export function createContribution(data) {
  return client.post('contributions', data).then((r) => r.data)
}

export function updateContribution(id, data) {
  return client.patch(`contributions/${id}`, data).then((r) => r.data)
}

export function deleteContribution(id) {
  return client.delete(`contributions/${id}`)
}
