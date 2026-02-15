import client from './client'

export function getCategories() {
  return client.get('expenses/categories').then((r) => r.data)
}

export function createCategory(data) {
  return client.post('expenses/categories', data).then((r) => r.data)
}

export function getExpenses() {
  return client.get('expenses').then((r) => r.data)
}

export function createExpense(data) {
  return client.post('expenses', data).then((r) => r.data)
}

export function updateExpense(id, data) {
  return client.patch(`expenses/${id}`, data).then((r) => r.data)
}

export function deleteExpense(id) {
  return client.delete(`expenses/${id}`)
}
