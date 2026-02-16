<template>
  <div class="page">
    <PageHeader>
      {{ $t('suppliers.title') }}
      <template #subtitle>{{ $t('suppliers.subtitle') }}</template>
    </PageHeader>
    <section class="card card-body" style="margin-bottom: var(--space-6);">
      <div class="section-header">
        <h2 class="section-title">{{ $t('suppliers.title') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAdd">{{ $t('common.add') }}</button>
      </div>
      <PaginatedTable
        :items="suppliers"
        :columns="columns"
        :loading="loading"
        :empty-text="$t('suppliers.empty')"
        :per-page="10"
      >
        <template #actions="{ item }">
          <IconButton type="edit" :title="$t('common.edit')" @click="startEdit(item)" />
          <IconButton type="delete" :title="$t('common.delete')" @click="confirmDelete(item)" />
        </template>
      </PaginatedTable>
    </section>

    <Modal v-model="modalOpen" :title="modalTitle">
      <form @submit.prevent="submitSupplier" class="form-fields">
        <div class="form-group">
          <label class="required">{{ $t('suppliers.name') }}</label>
          <input v-model="form.name" type="text" class="input" required />
        </div>
        <div class="form-group">
          <label>{{ $t('suppliers.phone') }}</label>
          <input v-model="form.phone" type="text" class="input" />
        </div>
        <div class="form-group">
          <label>{{ $t('suppliers.email') }}</label>
          <input v-model="form.email" type="email" class="input" />
        </div>
        <div class="form-group">
          <label>{{ $t('suppliers.city') }}</label>
          <select v-model="form.city_id" class="input">
            <option value="">{{ $t('common.selectCity') }}</option>
            <option v-for="c in cities" :key="c.id" :value="c.id">{{ c.name }}</option>
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
import { getSuppliers, createSupplier, updateSupplier, deleteSupplier } from '../api/suppliers'
import { getCities } from '../api/cities'

const { t } = useI18n()

const suppliers = ref([])
const cities = ref([])
const loading = ref(false)
const modalOpen = ref(false)
const editing = ref(null)
const form = ref({ name: '', phone: '', email: '', city_id: '' })

const columns = computed(() => [
  { key: 'name', label: t('suppliers.name') },
  { key: 'phone', label: t('suppliers.phone') },
  { key: 'email', label: t('suppliers.email') },
  { key: 'city_id', label: t('suppliers.city') },
])

const modalTitle = computed(() =>
  editing.value ? `${t('common.edit')} ${t('suppliers.title')}` : `${t('common.add')} ${t('suppliers.title')}`
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
  form.value = { name: '', phone: '', email: '', city_id: '' }
}

async function load() {
  loading.value = true
  try {
    const [suppliersData, citiesData] = await Promise.all([getSuppliers(), getCities()])
    suppliers.value = suppliersData
    cities.value = citiesData
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function startEdit(s) {
  editing.value = s.id
  form.value = { name: s.name, phone: s.phone || '', email: s.email || '', city_id: s.city_id || '' }
  modalOpen.value = true
}

function confirmDelete(s) {
  if (window.confirm(`${s.name} — ${t('suppliers.confirmDelete')}`)) doDelete(s.id)
}

async function doDelete(id) {
  try {
    await deleteSupplier(id)
    await load()
  } catch (e) {
    console.error(e)
  }
}

async function submitSupplier() {
  try {
    if (editing.value) {
      await updateSupplier(editing.value, form.value)
    } else {
      await createSupplier(form.value)
    }
    closeModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

