import client from './client'

export function getProductTypes() {
  return client.get('product-types').then((r) => r.data)
}

export function createProductType(data) {
  return client.post('product-types', data).then((r) => r.data)
}

export function updateProductType(productTypeId, data) {
  return client.patch(`product-types/${productTypeId}`, data).then((r) => r.data)
}

export function deleteProductType(productTypeId) {
  return client.delete(`product-types/${productTypeId}`)
}
