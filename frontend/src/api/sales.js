import client from './client'

export function createSale(data) {
  return client.post('sales', data).then((r) => r.data)
}

export function addPayment(data) {
  return client.post('sales/payment', data).then((r) => r.data)
}

export function getUnpaid() {
  return client.get('sales/unpaid').then((r) => r.data)
}

export function getSale(id) {
  return client.get(`sales/${id}`).then((r) => r.data)
}

export function updateSale(id, data) {
  return client.patch(`sales/${id}`, data).then((r) => r.data)
}

export function deleteSale(id) {
  return client.delete(`sales/${id}`)
}
