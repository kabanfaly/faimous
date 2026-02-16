import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import client from '../api/client'
import { updateCurrentOrganisation } from '../api/organisations'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const organisation = ref(null)
  const token = ref(localStorage.getItem('token'))

  const isAuthenticated = computed(() => !!token.value)

  async function login(email, password) {
    const { data } = await client.post('auth/login', { email, password })
    token.value = data.access_token
    user.value = data.user
    organisation.value = data.organisation
    localStorage.setItem('token', data.access_token)
  }

  async function register({ organisationName, email, password, first_name = '', last_name = '' }) {
    const { data } = await client.post('auth/register', {
      organisation_name: organisationName,
      email,
      password,
      first_name,
      last_name,
    })
    token.value = data.access_token
    user.value = data.user
    organisation.value = data.organisation
    localStorage.setItem('token', data.access_token)
  }

  async function fetchMe() {
    const { data } = await client.get('auth/me')
    user.value = data.user
    organisation.value = data.organisation
  }

  async function updateProfile(payload) {
    const { data } = await client.patch('auth/me', payload)
    user.value = data.user
    organisation.value = data.organisation
    return data
  }

  async function changePassword(currentPassword, newPassword) {
    await client.post('auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    })
  }

  async function updateOrganisation(payload) {
    const updated = await updateCurrentOrganisation(payload)
    organisation.value = updated
    return updated
  }

  function logout() {
    token.value = null
    user.value = null
    organisation.value = null
    localStorage.removeItem('token')
  }

  return {
    user,
    organisation,
    token,
    isAuthenticated,
    login,
    register,
    fetchMe,
    updateProfile,
    updateOrganisation,
    changePassword,
    logout,
  }
})
