import client from './client'

export function createEggs(data) {
  return client.post('production/eggs', data).then((r) => r.data)
}

export function createFlock(data) {
  return client.post('production/flock', data).then((r) => r.data)
}

export function getKpis() {
  return client.get('production/kpis').then((r) => r.data)
}
