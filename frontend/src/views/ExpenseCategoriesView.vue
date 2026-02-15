<template>
  <div class="page">
    <PageHeader>
      {{ $t('expenseCategories.title') }}
      <template #subtitle>{{ $t('expenseCategories.subtitle') }}</template>
    </PageHeader>
    <section class="card card-body" style="margin-bottom: var(--space-6);">
      <div class="section-header">
        <h2 class="section-title">{{ $t('expenseCategories.title') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAdd">{{ $t('common.add') }}</button>
      </div>
      <PaginatedTable
        :items="items"
        :columns="columns"
        :loading="loading"
        :empty-text="$t('expenseCategories.empty')"
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
          <label class="required">{{ $t('expenseCategories.name') }}</label>
          <input v-model="form.name" type="text" class="input" required />
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
import { getExpenseCategories, createExpenseCategory, updateExpenseCategory, deleteExpenseCategory } from '../api/expenseCategories'

const { t } = useI18n()
const items = ref([])
const loading = ref(false)
const modalOpen = ref(false)
const editing = ref(null)
const form = ref({ name: '' })

const columns = computed(() => [
  { key: 'name', label: t('expenseCategories.name') },
])

const modalTitle = computed(() =>
  editing.value ? `${t('common.edit')} ${t('expenseCategories.title')}` : `${t('common.add')} ${t('expenseCategories.title')}`
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
  form.value = { name: '' }
}

async function load() {
  loading.value = true
  try {
    items.value = await getExpenseCategories()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function startEdit(item) {
  editing.value = item.id
  form.value = { name: item.name }
  modalOpen.value = true
}

function confirmDelete(item) {
  if (window.confirm(`${item.name} — ${t('expenseCategories.confirmDelete')}`)) doDelete(item.id)
}

async function doDelete(id) {
  try {
    await deleteExpenseCategory(id)
    await load()
  } catch (e) {
    console.error(e)
  }
}

async function submit() {
  try {
    if (editing.value) await updateExpenseCategory(editing.value, form.value)
    else await createExpenseCategory(form.value)
    closeModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

