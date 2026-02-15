<template>
  <div class="page">
    <PageHeader>
      {{ $t('shareholders.title') }}
      <template #subtitle>{{ $t('shareholders.subtitle') }}</template>
    </PageHeader>
    <section class="card card-body" style="margin-bottom: var(--space-6);">
      <div class="section-header">
        <h2 class="section-title">{{ $t('shareholders.title') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAdd">{{ $t('common.add') }}</button>
      </div>
      <PaginatedTable
        :items="items"
        :columns="columns"
        :loading="loading"
        :empty-text="$t('shareholders.empty')"
        :per-page="10"
      >
        <template #actions="{ item }">
          <IconButton type="edit" :title="$t('common.edit')" @click="startEdit(item)" />
          <IconButton type="delete" :title="$t('common.delete')" @click="confirmDelete(item)" />
        </template>
      </PaginatedTable>
    </section>

    <Modal v-model="modalOpen" :title="modalTitle">
      <form @submit.prevent="submit" class="form-fields">
        <div class="form-group">
          <label class="required">{{ $t('shareholders.firstName') }}</label>
          <input v-model="form.first_name" type="text" class="input" required />
        </div>
        <div class="form-group">
          <label class="required">{{ $t('shareholders.lastName') }}</label>
          <input v-model="form.last_name" type="text" class="input" required />
        </div>
        <div class="form-group">
          <label>{{ $t('shareholders.phone') }}</label>
          <input v-model="form.phone" type="text" class="input" />
        </div>
        <div class="form-group">
          <label>{{ $t('shareholders.email') }}</label>
          <input v-model="form.email" type="email" class="input" />
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
import { getShareholders, createShareholder, updateShareholder, deleteShareholder } from '../api/shareholders'

const { t } = useI18n()
const items = ref([])
const loading = ref(false)
const modalOpen = ref(false)
const editing = ref(null)
const form = ref({ first_name: '', last_name: '', phone: '', email: '' })

const columns = computed(() => [
  { key: 'first_name', label: t('shareholders.firstName') },
  { key: 'last_name', label: t('shareholders.lastName') },
  { key: 'phone', label: t('shareholders.phone') },
  { key: 'email', label: t('shareholders.email') },
])

const modalTitle = computed(() =>
  editing.value ? `${t('common.edit')} ${t('shareholders.title')}` : `${t('common.add')} ${t('shareholders.title')}`
)

function openAdd() {
  resetForm()
  modalOpen.value = true
}

function closeModal() {
  modalOpen.value = false
  resetForm()
}

function resetForm() {
  editing.value = null
  form.value = { first_name: '', last_name: '', phone: '', email: '' }
}

async function load() {
  loading.value = true
  try {
    items.value = await getShareholders()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function startEdit(item) {
  editing.value = item.id
  form.value = { first_name: item.first_name, last_name: item.last_name, phone: item.phone || '', email: item.email || '' }
  modalOpen.value = true
}

function confirmDelete(item) {
  const name = `${item.first_name} ${item.last_name}`
  if (window.confirm(`${name} — ${t('shareholders.confirmDelete')}`)) doDelete(item.id)
}

async function doDelete(id) {
  try {
    await deleteShareholder(id)
    await load()
  } catch (e) {
    console.error(e)
  }
}

async function submit() {
  try {
    if (editing.value) await updateShareholder(editing.value, form.value)
    else await createShareholder(form.value)
    closeModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

