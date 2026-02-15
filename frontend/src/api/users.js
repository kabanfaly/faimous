import client from './client'

export function getUsers() {
  return client.get('users').then((r) => r.data)
}

export function createUser(data) {
  return client.post('users', data).then((r) => r.data)
}

export function updateUser(userId, data) {
  return client.patch(`users/${userId}`, data).then((r) => r.data)
}
