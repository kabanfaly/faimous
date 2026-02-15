import client from './client'

export function getSuppliers() {
  return client.get('suppliers').then((r) => r.data)
}

export function createSupplier(data) {
  return client.post('suppliers', data).then((r) => r.data)
}

export function updateSupplier(supplierId, data) {
  return client.patch(`suppliers/${supplierId}`, data).then((r) => r.data)
}

export function deleteSupplier(supplierId) {
  return client.delete(`suppliers/${supplierId}`)
}
