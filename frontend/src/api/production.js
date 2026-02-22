import client from './client'

export function createEggs(data) {
  return client.post('production/eggs', data).then((r) => r.data)
}

export function createFlock(data) {
  return client.post('production/flock', data).then((r) => r.data)
}

export function getKpis() {
  return client.get('production/kpis').then((r) => r.data)
}

export function getDailyOperations() {
  return client.get('production/daily').then((r) => r.data)
}

export function getDailyOperation(id) {
  return client.get(`production/daily/${id}`).then((r) => r.data)
}

export function createDailyOperation(data) {
  return client.post('production/daily', data).then((r) => r.data)
}

export function updateDailyOperation(id, data) {
  return client.patch(`production/daily/${id}`, data).then((r) => r.data)
}

export function deleteDailyOperation(id) {
  return client.delete(`production/daily/${id}`)
}
