import client from './client'

export function getProducts() {
  return client.get('stock/products').then((r) => r.data)
}

export function createProduct(data) {
  return client.post('stock/products', data).then((r) => r.data)
}

export function updateProduct(id, data) {
  return client.patch(`stock/products/${id}`, data).then((r) => r.data)
}

export function deleteProduct(id) {
  return client.delete(`stock/products/${id}`)
}

export function getMovements(productId) {
  const params = productId ? { product_id: productId } : {}
  return client.get('stock/movements', { params }).then((r) => r.data)
}

export function createMovement(data) {
  return client.post('stock/movements', data).then((r) => r.data)
}

export function updateMovement(id, data) {
  return client.patch(`stock/movements/${id}`, data).then((r) => r.data)
}

export function deleteMovement(id) {
  return client.delete(`stock/movements/${id}`)
}

export function getAlerts(threshold = 0) {
  return client.get('stock/alerts', { params: { threshold } }).then((r) => r.data)
}
