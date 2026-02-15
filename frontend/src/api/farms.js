import client from './client'

export function getFarms() {
  return client.get('farms').then((r) => r.data)
}

export function createFarm(data) {
  return client.post('farms', data).then((r) => r.data)
}

export function updateFarm(farmId, data) {
  return client.patch(`farms/${farmId}`, data).then((r) => r.data)
}

export function deleteFarm(farmId) {
  return client.delete(`farms/${farmId}`)
}
