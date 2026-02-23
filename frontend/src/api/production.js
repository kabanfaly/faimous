import client from './client'

export function getEggs() {
  return client.get('production/eggs').then((r) => r.data)
}

export function createEggs(data) {
  return client.post('production/eggs', data).then((r) => r.data)
}

export function updateEggs(id, data) {
  return client.patch(`production/eggs/${id}`, data).then((r) => r.data)
}

export function deleteEggs(id) {
  return client.delete(`production/eggs/${id}`)
}

export function getFlock() {
  return client.get('production/flock').then((r) => r.data)
}

export function createFlock(data) {
  return client.post('production/flock', data).then((r) => r.data)
}

export function updateFlock(id, data) {
  return client.patch(`production/flock/${id}`, data).then((r) => r.data)
}

export function deleteFlock(id) {
  return client.delete(`production/flock/${id}`)
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
