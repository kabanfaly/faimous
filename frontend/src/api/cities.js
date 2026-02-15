import client from './client'

export function getCities() {
  return client.get('cities').then((r) => r.data)
}

export function createCity(data) {
  return client.post('cities', data).then((r) => r.data)
}

export function updateCity(cityId, data) {
  return client.patch(`cities/${cityId}`, data).then((r) => r.data)
}

export function deleteCity(cityId) {
  return client.delete(`cities/${cityId}`)
}
