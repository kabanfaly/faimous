import client from './client'

export function getExpenseCategories() {
  return client.get('expense-categories').then((r) => r.data)
}

export function createExpenseCategory(data) {
  return client.post('expense-categories', data).then((r) => r.data)
}

export function updateExpenseCategory(categoryId, data) {
  return client.patch(`expense-categories/${categoryId}`, data).then((r) => r.data)
}

export function deleteExpenseCategory(categoryId) {
  return client.delete(`expense-categories/${categoryId}`)
}
