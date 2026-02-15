<template>
  <div class="page">
    <PageHeader>
      {{ $t('users.title') }}
      <template #subtitle>{{ $t('users.role') }}</template>
    </PageHeader>
    <section class="card card-body" style="margin-bottom: var(--space-6);">
      <div class="section-header">
        <h2 class="section-title">{{ $t('users.title') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAdd">{{ $t('common.add') }}</button>
      </div>
      <PaginatedTable
        :items="users"
        :columns="columns"
        :loading="loading"
        :empty-text="$t('users.empty')"
        :per-page="10"
      >
        <template #actions="{ item }">
          <IconButton type="edit" :title="$t('common.edit')" @click="startEdit(item)" />
        </template>
      </PaginatedTable>
    </section>

    <Modal v-model="modalOpen" :title="modalTitle">
      <form @submit.prevent="submitUser" class="form-fields">
        <div class="form-group">
          <label class="required">{{ $t('users.firstName') }}</label>
          <input v-model="form.first_name" type="text" class="input" required />
        </div>
        <div class="form-group">
          <label class="required">{{ $t('users.lastName') }}</label>
          <input v-model="form.last_name" type="text" class="input" required />
        </div>
        <div class="form-group">
          <label class="required">{{ $t('auth.email') }}</label>
          <input v-model="form.email" type="email" class="input" :readonly="!!editing" required />
        </div>
        <div v-if="!editing" class="form-group">
          <label class="required">{{ $t('auth.password') }}</label>
          <input v-model="form.password" type="password" class="input" required />
        </div>
        <div class="form-group">
          <label>{{ $t('users.role') }}</label>
          <select v-model="form.role" class="input">
            <option value="user">{{ $t('users.user') }}</option>
            <option value="worker">{{ $t('users.worker') }}</option>
            <option value="manager">{{ $t('users.manager') }}</option>
            <option value="admin">{{ $t('users.admin') }}</option>
          </select>
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ $t('common.save') }}</button>
          <button type="button" class="btn btn-ghost" @click="closeModal">{{ $t('common.cancel') }}</button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import PaginatedTable from '../components/PaginatedTable.vue'
import Modal from '../components/Modal.vue'
import IconButton from '../components/IconButton.vue'
import PageHeader from '../components/PageHeader.vue'
import { getUsers, createUser, updateUser } from '../api/users'

const { t } = useI18n()
const users = ref([])
const loading = ref(false)
const modalOpen = ref(false)
const editing = ref(null)

const modalTitle = computed(() =>
  editing.value ? `${t('common.edit')} ${t('users.title')}` : `${t('common.add')} ${t('users.title')}`
)

const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  role: 'user',
})

const columns = computed(() => [
  { key: 'first_name', label: t('users.firstName') },
  { key: 'last_name', label: t('users.lastName') },
  { key: 'email', label: t('auth.email') },
  { key: 'role', label: t('users.role') },
])

function openAdd() {
  editing.value = null
  form.value = { first_name: '', last_name: '', email: '', password: '', role: 'user' }
  modalOpen.value = true
}

function closeModal() {
  modalOpen.value = false
  editing.value = null
  form.value = { first_name: '', last_name: '', email: '', password: '', role: 'user' }
}

function startEdit(item) {
  editing.value = item.id
  form.value = {
    first_name: item.first_name,
    last_name: item.last_name,
    email: item.email,
    password: '',
    role: item.role || 'user',
  }
  modalOpen.value = true
}

async function load() {
  loading.value = true
  try {
    users.value = await getUsers()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function submitUser() {
  try {
    if (editing.value) {
      await updateUser(editing.value, { first_name: form.value.first_name, last_name: form.value.last_name, role: form.value.role })
    } else {
      await createUser(form.value)
    }
    closeModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

