import client from './client'

export function getProducts() {
  return client.get('products').then((r) => r.data)
}

export function createProduct(data) {
  return client.post('products', data).then((r) => r.data)
}

export function updateProduct(productId, data) {
  return client.patch(`products/${productId}`, data).then((r) => r.data)
}

export function deleteProduct(productId) {
  return client.delete(`products/${productId}`)
}

export function getProductUnits() {
  return client.get('products/units').then((r) => r.data)
}
