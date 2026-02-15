import client from './client'

export function createPurchase(data) {
  return client.post('purchases', data).then((r) => r.data)
}

export function addPayment(data) {
  return client.post('purchases/payment', data).then((r) => r.data)
}

export function getUnpaid() {
  return client.get('purchases/unpaid').then((r) => r.data)
}

export function getPurchase(id) {
  return client.get(`purchases/${id}`).then((r) => r.data)
}

export function updatePurchase(id, data) {
  return client.patch(`purchases/${id}`, data).then((r) => r.data)
}

export function deletePurchase(id) {
  return client.delete(`purchases/${id}`)
}
