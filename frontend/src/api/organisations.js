import client from './client'

export function getCurrentOrganisation() {
  return client.get('organisations/current').then((r) => r.data)
}

export function updateCurrentOrganisation(data) {
  return client.patch('organisations/current', data).then((r) => r.data)
}
