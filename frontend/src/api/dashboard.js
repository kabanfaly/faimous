import client from './client'

export function getSummary() {
  return client.get('dashboard/summary').then((r) => r.data)
}

export function getCharts() {
  return client.get('dashboard/charts').then((r) => r.data)
}
