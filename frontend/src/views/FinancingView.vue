<template>
  <div class="page">
    <PageHeader>
      {{ $t('financing.title') }}
      <template #subtitle>{{ $t('financing.contributions') }}</template>
    </PageHeader>
    <section class="card card-body" style="margin-bottom: var(--space-6);">
      <div class="section-header">
        <h2 class="section-title">{{ $t('financing.contributions') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAddShareholder">{{ $t('common.add') }} {{ $t('shareholders.title') }}</button>
      </div>
      <PaginatedTable
        :items="shareholders"
        :columns="shareholderColumns"
        :loading="loading"
        :empty-text="$t('financing.emptyShareholders')"
        :per-page="10"
      >
        <template #actions="{ item }">
          <IconButton type="edit" :title="$t('common.edit')" @click="startEditShareholder(item)" />
          <IconButton type="delete" :title="$t('common.delete')" @click="confirmDeleteShareholder(item)" />
        </template>
      </PaginatedTable>
    </section>
    <section class="card card-body" style="margin-bottom: var(--space-6);">
      <div class="section-header">
        <h2 class="section-title">{{ $t('financing.contributionsList') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAddContribution">{{ $t('common.add') }} {{ $t('financing.contribution') }}</button>
      </div>
      <PaginatedTable
        :items="contributions"
        :columns="contributionColumns"
        :loading="loading"
        :empty-text="$t('financing.emptyContributions')"
        :per-page="10"
      >
        <template #actions="{ item }">
          <IconButton type="edit" :title="$t('common.edit')" @click="startEditContribution(item)" />
          <IconButton type="delete" :title="$t('common.delete')" @click="confirmDeleteContribution(item)" />
        </template>
      </PaginatedTable>
    </section>

    <Modal v-model="shareholderModalOpen" :title="shareholderModalTitle">
      <form @submit.prevent="submitShareholder" class="form-fields">
        <div class="form-group">
          <label class="required">{{ $t('shareholders.firstName') }}</label>
          <input v-model="shareholderForm.first_name" type="text" class="input" required />
        </div>
        <div class="form-group">
          <label class="required">{{ $t('shareholders.lastName') }}</label>
          <input v-model="shareholderForm.last_name" type="text" class="input" required />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ $t('common.save') }}</button>
          <button type="button" class="btn btn-ghost" @click="closeShareholderModal">{{ $t('common.cancel') }}</button>
        </div>
      </form>
    </Modal>

    <Modal v-model="contributionModalOpen" :title="contributionModalTitle">
      <form @submit.prevent="submitContribution" class="form-fields">
        <div class="form-group">
          <label class="required">{{ $t('common.date') }}</label>
          <input v-model="contributionForm.date" type="date" class="input" required />
        </div>
        <div class="form-group">
          <label>{{ $t('financing.shareholderId') }}</label>
          <select v-model="contributionForm.shareholder_id" class="input">
            <option value="">{{ $t('financing.shareholderIdPlaceholder') }}</option>
            <option v-for="s in shareholders" :key="s.id" :value="s.id">{{ s.first_name }} {{ s.last_name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label class="required">{{ $t('common.amount') }}</label>
          <input v-model.number="contributionForm.amount" type="number" class="input" step="0.01" required />
        </div>
        <div class="form-group">
          <label>{{ $t('expenses.description') }}</label>
          <input v-model="contributionForm.description" type="text" class="input" />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ $t('common.save') }}</button>
          <button type="button" class="btn btn-ghost" @click="closeContributionModal">{{ $t('common.cancel') }}</button>
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
import { getShareholders, createShareholder, updateShareholder, deleteShareholder, getContributions, createContribution, updateContribution, deleteContribution } from '../api/contributions'

const { t } = useI18n()
const shareholders = ref([])
const contributions = ref([])
const loading = ref(false)
const shareholderModalOpen = ref(false)
const contributionModalOpen = ref(false)
const editingShareholder = ref(null)
const editingContribution = ref(null)

const shareholderModalTitle = computed(() =>
  editingShareholder.value ? `${t('common.edit')} ${t('shareholders.title')}` : `${t('common.add')} ${t('shareholders.title')}`
)
const contributionModalTitle = computed(() =>
  editingContribution.value ? `${t('common.edit')} ${t('financing.contribution')}` : `${t('common.add')} ${t('financing.contribution')}`
)

const shareholderColumns = computed(() => [
  { key: 'first_name', label: t('shareholders.firstName') },
  { key: 'last_name', label: t('shareholders.lastName') },
  { key: 'email', label: t('shareholders.email') },
])

const contributionColumns = computed(() => [
  { key: 'date', label: t('common.date') },
  { key: 'amount', label: t('financing.amount') },
  { key: 'description', label: t('expenses.description') },
  { key: 'shareholder_id', label: t('financing.shareholderId') },
])
const shareholderForm = ref({ first_name: '', last_name: '' })
const contributionForm = ref({
  date: new Date().toISOString().slice(0, 10),
  shareholder_id: '',
  amount: 0,
  description: '',
})

function openAddShareholder() {
  editingShareholder.value = null
  shareholderForm.value = { first_name: '', last_name: '' }
  shareholderModalOpen.value = true
}

function closeShareholderModal() {
  shareholderModalOpen.value = false
  editingShareholder.value = null
}

function startEditShareholder(item) {
  editingShareholder.value = item.id
  shareholderForm.value = { first_name: item.first_name, last_name: item.last_name }
  shareholderModalOpen.value = true
}

function confirmDeleteShareholder(item) {
  const name = `${item.first_name} ${item.last_name}`
  if (window.confirm(`${name} — ${t('financing.confirmDeleteShareholder')}`)) doDeleteShareholder(item.id)
}

async function doDeleteShareholder(id) {
  try {
    await deleteShareholder(id)
    await load()
  } catch (e) {
    console.error(e)
  }
}

function openAddContribution() {
  editingContribution.value = null
  contributionForm.value = { date: new Date().toISOString().slice(0, 10), shareholder_id: '', amount: 0, description: '' }
  contributionModalOpen.value = true
}

function closeContributionModal() {
  contributionModalOpen.value = false
  editingContribution.value = null
}

function startEditContribution(item) {
  editingContribution.value = item.id
  contributionForm.value = {
    date: item.date,
    shareholder_id: item.shareholder_id || '',
    amount: item.amount ?? 0,
    description: item.description || '',
  }
  contributionModalOpen.value = true
}

function confirmDeleteContribution(item) {
  if (window.confirm(`${item.date} — ${t('financing.confirmDeleteContribution')}`)) doDeleteContribution(item.id)
}

async function doDeleteContribution(id) {
  try {
    await deleteContribution(id)
    await load()
  } catch (e) {
    console.error(e)
  }
}

async function load() {
  loading.value = true
  try {
    shareholders.value = await getShareholders()
    contributions.value = await getContributions()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function submitShareholder() {
  try {
    if (editingShareholder.value) {
      await updateShareholder(editingShareholder.value, shareholderForm.value)
    } else {
      await createShareholder(shareholderForm.value)
    }
    closeShareholderModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

async function submitContribution() {
  try {
    if (editingContribution.value) {
      await updateContribution(editingContribution.value, contributionForm.value)
    } else {
      await createContribution(contributionForm.value)
    }
    closeContributionModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

